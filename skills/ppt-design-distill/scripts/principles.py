"""Search the project's design questions and create unanswered worksheets (stdlib)."""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def catalog():
    return json.loads((ROOT/'references/method/principles.json').read_text(encoding='utf-8'))

def select(items, query='', scene=None, adoption=None, ids=None):
    terms = re.findall(r'[^\s,]+', query.casefold().replace(chr(0xFF0C), ','))
    results=[]
    for item in items:
        if scene and scene not in item['scenes']:
            continue
        if adoption and item['adoption'] != adoption:
            continue
        if ids and item['id'] not in ids:
            continue
        haystack=' '.join(str(item[k]) for k in ['id','name','keywords','group','ask']).casefold()
        score=sum(term in haystack for term in terms)
        if terms and not score:
            continue
        results.append((score,item))
    return [item for _,item in sorted(results,key=lambda x:(-x[0],x[1]['id']))]

def worksheet(items, scene):
    return {'schema_version':2,'kind':'principle_application_worksheet',
      'scene':scene,'status':'unreviewed','quality_certified':False,
      'brief':{'audience':None,'purpose':None,'context':None,'expression_direction':None},
      'source_note':'Project questions in our own words. Scope labels are project annotations; no observed current-reference rules.',
      'questions':[{'principle_id':i['id'],'name':i['name'],'adoption':i['adoption'],
        'ask':i['ask'],'limit':i['limit'],
        'selected_for_task':None,'why_applicable_or_not':None,
        'subject_parts':[],'context':None,'hypothesis':None,'reject_if':None,
        'method':None,'baseline_artifact':None,'candidate_artifact':None,
        'evidence_ids':[],'observation':None,'decision':None,'remaining_unknowns':[]}
        for i in items],
      'handoff':'Select only applicable questions. Bind actual questions/evidence to the existing LOOP review_plan and challenge tests. This worksheet cannot emit PASS.'}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    subs=parser.add_subparsers(dest='command',required=True)
    search=subs.add_parser('search')
    search.add_argument('query',nargs='?',default='')
    search.add_argument('--scene',choices=['ppt','ui','web'])
    search.add_argument('--adoption',choices=['conditional','hypothesis','context_only','research_only'])
    search.add_argument('--limit',type=int,default=8)
    show=subs.add_parser('show')
    show.add_argument('ids',nargs='+')
    sheet=subs.add_parser('worksheet')
    sheet.add_argument('--ids',nargs='+',required=True)
    sheet.add_argument('--scene',choices=['ppt','ui','web'],required=True)
    sheet.add_argument('--out',type=Path,required=True)
    args=parser.parse_args(argv)
    data=catalog()
    if args.command=='search':
        if args.limit<1:
            parser.error('--limit must be positive')
        found=select(data['items'],args.query,args.scene,args.adoption)[:args.limit]
    else:
        known={i['id'] for i in data['items']}
        missing=set(args.ids)-known
        if missing:
            parser.error('Unknown principle IDs: '+', '.join(sorted(missing)))
        found=select(data['items'],scene=getattr(args,'scene',None),ids=set(args.ids))
        if len(found)!=len(set(args.ids)):
            parser.error('Some selected principles are outside the requested scene')
    if args.command=='worksheet':
        args.out.parent.mkdir(parents=True,exist_ok=True)
        try:
            with args.out.open('x',encoding='utf-8') as f:
                json.dump(worksheet(found,args.scene),f,ensure_ascii=False,indent=2)
                f.write('\n')
        except FileExistsError:
            parser.error('Output exists; choose a new path to preserve actual observations')
        print(json.dumps({'path':str(args.out),'questions':len(found),'status':'unreviewed'}))
    else:
        print(json.dumps({'count':len(found),'results':found},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
