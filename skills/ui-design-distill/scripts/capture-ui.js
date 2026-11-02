// Playwright run-code expression. Read-only capture of the current UI state.
async (page) => {
  return await page.evaluate(() => {
    const visible = el => {
      const r = el.getBoundingClientRect(), s = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden' && !el.closest('[hidden],[aria-hidden="true"]');
    };
    const rect = el => { const r = el.getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height }; };
    const label = el => {
      if (el.getAttribute('aria-label')) return el.getAttribute('aria-label');
      const ids = (el.getAttribute('aria-labelledby') || '').split(/\s+/).filter(Boolean);
      if (ids.length) return ids.map(id => document.getElementById(id)?.textContent || '').join(' ').trim();
      if (el.labels?.length) return [...el.labels].map(x => x.textContent).join(' ').trim();
      return /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName) ? (el.getAttribute('placeholder') || '') : (el.textContent || '').trim();
    };
    const selector = el => el.id ? '#' + CSS.escape(el.id) : el.tagName.toLowerCase() + (el.getAttribute('role') ? '[role="' + el.getAttribute('role').replace(/"/g, '') + '"]' : '');
    const candidates = [...document.querySelectorAll('button,a[href],input:not([type="hidden"]),select,textarea,[role="button"],[role="tab"],[role="combobox"],[role="checkbox"],[role="switch"],[role="dialog"],[role="status"],[role="alert"]')].filter(visible);
    return {
      url: location.href, viewport: { width: innerWidth, height: innerHeight },
      captured_at: new Date().toISOString(),
      landmarks: [...document.querySelectorAll('main,nav,aside,header,[role="navigation"],[role="main"]')].filter(visible).map(el => ({ tag: el.tagName.toLowerCase(), selector: selector(el), name: el.getAttribute('aria-label'), rect: rect(el) })),
      controls: candidates.slice(0, 200).map((el, index) => {
        const s = getComputedStyle(el);
        return { capture_id: 'control-' + index, selector_hint: selector(el), tag: el.tagName.toLowerCase(), role: el.getAttribute('role'), type: el.getAttribute('type'),
          name_candidate: label(el).slice(0, 160), label_source: el.getAttribute('aria-label') ? 'aria-label' : el.getAttribute('aria-labelledby') ? 'aria-labelledby' : el.labels?.length ? 'label' : /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName) ? 'placeholder-not-accessible-name' : 'text',
          disabled: el.disabled === true || el.getAttribute('aria-disabled') === 'true',
          selected: el.getAttribute('aria-selected'), expanded: el.getAttribute('aria-expanded'), checked: /^(checkbox|radio)$/.test(el.getAttribute('type') || '') ? el.checked : el.getAttribute('aria-checked'),
          rect: rect(el), styles: { font: s.font, color: s.color, background: s.backgroundColor, border: s.border, radius: s.borderRadius, padding: s.padding },
          state_observation: el === document.activeElement ? 'focused-at-capture' : 'current-render-only' };
      }),
      truncated: candidates.length > 200,
      limitations: ['No field values read. Labels are candidates, not an accessibility certification.', 'A current DOM snapshot does not establish tasks, transitions, permissions or hidden states.']
    };
  });
}
