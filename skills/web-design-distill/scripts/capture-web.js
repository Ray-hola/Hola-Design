// Playwright run-code expression. Repeat at relevant widths; do not infer unseen changes.
async (page) => {
  return await page.evaluate(() => {
    const visible = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden' && !el.closest('[hidden],[aria-hidden="true"]'); };
    const rect = el => { const r = el.getBoundingClientRect(); return { x: r.x + scrollX, y: r.y + scrollY, width: r.width, height: r.height }; };
    const nodes = [...document.querySelectorAll('header,main,section,article,footer,nav,[role="region"]')].filter(visible);
    return { url: location.href, title: document.title, viewport: { width: innerWidth, height: innerHeight },
      captured_at: new Date().toISOString(),
      headings: [...document.querySelectorAll('h1,h2,h3')].filter(visible).map(el => ({ level: el.tagName.toLowerCase(), text: el.textContent.trim(), rect: rect(el), font: getComputedStyle(el).font })),
      sections: nodes.slice(0, 100).map((el, index) => ({ capture_id: 'section-' + index, tag: el.tagName.toLowerCase(), id: el.id || null, rect: rect(el),
        heading: el.querySelector('h1,h2,h3')?.textContent.trim() || null,
        text_sample: (el.innerText || '').trim().slice(0, 400),
        layout_children: [...el.children].filter(visible).slice(0, 12).map(child => ({ tag: child.tagName.toLowerCase(), rect: rect(child), grid: { display: getComputedStyle(child).display, columns: getComputedStyle(child).gridTemplateColumns, gap: getComputedStyle(child).gap } })),
        links: [...el.querySelectorAll('a[href]')].filter(visible).slice(0, 12).map(a => ({ text: a.textContent.trim().slice(0, 80), href: a.getAttribute('href') })),
        grid: { display: getComputedStyle(el).display, columns: getComputedStyle(el).gridTemplateColumns, gap: getComputedStyle(el).gap } })),
      truncated: nodes.length > 100,
      limitations: ['Purpose and ordering rationale require content analysis.', 'Only the current viewport was observed; compare the same source content at other widths.'] };
  });
}
