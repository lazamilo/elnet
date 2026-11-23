(function(){
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasGsap = typeof gsap !== 'undefined';
  if (reduced || !hasGsap) document.documentElement.classList.add('reduced');
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);

  /* ---------- smooth scroll ---------- */
  let lenis = null;
  if (!reduced && typeof Lenis !== 'undefined') {
    lenis = new Lenis({ duration: 1.15, smoothWheel: true });
    lenis.on('scroll', () => hasGsap && ScrollTrigger.update());
    if (hasGsap) { gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
    else { const raf = t => { lenis.raf(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf); }
  }

  /* ---------- nav ---------- */
  const nav = document.querySelector('.nav');
  let lastY = 0;
  const onScroll = () => {
    const y = window.scrollY;
    nav.classList.toggle('scrolled', y > 20);
    const menuOpen = document.body.classList.contains('menu-open');
    nav.classList.toggle('hide', !menuOpen && y > 400 && y > lastY + 2);
    if (y < lastY - 2) nav.classList.remove('hide');
    lastY = y;
  };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  document.querySelector('.burger')?.addEventListener('click', () => {
    document.body.classList.toggle('menu-open');
    if (lenis) document.body.classList.contains('menu-open') ? lenis.stop() : lenis.start();
  });
  document.querySelectorAll('.mmenu a').forEach(a => a.addEventListener('click', () => { document.body.classList.remove('menu-open'); lenis && lenis.start(); }));

  /* ---------- loader ---------- */
  const loader = document.querySelector('.loader');
  const intro = () => {
    const h = document.querySelectorAll('.hero h1 .row > span, .phero h1 .row > span');
    if (!hasGsap || reduced) return;
    gsap.from(h, { yPercent: 110, duration: 1.2, ease: 'expo.out', stagger: .08 });
    gsap.from('.hero-media, .pbanner', { clipPath: 'inset(18% 12% 0% 12%)', duration: 1.6, ease: 'expo.out', delay: .1 });
    gsap.from('.hero-bottom > *, .phero .body-l, .phero .btn', { y: 30, opacity: 0, duration: 1, ease: 'power3.out', stagger: .08, delay: .35 });
  };
  if (loader && hasGsap && !reduced && !sessionStorageSeen()) {
    const paths = loader.querySelectorAll('path:not(#min-prostor)');
    const order = ['E-color','L-color','N-gray','E-gray','T-gray'].map(id => loader.querySelector('#' + id)).filter(Boolean);
    const tl = gsap.timeline({ onComplete: () => { loader.remove(); } });
    tl.to(order, { opacity: 1, y: 0, duration: .7, ease: 'expo.out', stagger: .07 })
      .to(loader.querySelector('.bar'), { scaleX: 1, duration: .7, ease: 'power2.inOut' }, '<')
      .to(loader, { clipPath: 'inset(0 0 100% 0)', duration: .9, ease: 'expo.inOut' }, '+=.1')
      .add(intro, '-=.45');
  } else { loader && loader.remove(); intro(); }
  function sessionStorageSeen(){
    try { const s = sessionStorage.getItem('elnet-loader'); sessionStorage.setItem('elnet-loader','1'); return !!s; } catch(e){ return false; }
  }

  /* ---------- hero slideshow ---------- */
  const hm = document.querySelector('.hero-media');
  if (hm) {
    const imgs = [...hm.querySelectorAll('img')];
    const tabs = [...document.querySelectorAll('.hero-tabs button')];
    let i = 0, timer;
    const show = n => {
      i = (n + imgs.length) % imgs.length;
      imgs.forEach((im, k) => im.classList.toggle('on', k === i));
      tabs.forEach((t, k) => { t.classList.remove('on'); void t.offsetWidth; t.classList.toggle('on', k === i); });
      clearTimeout(timer); timer = setTimeout(() => show(i + 1), 6000);
    };
    tabs.forEach((t, k) => t.addEventListener('click', () => show(k)));
    show(0);
    if (hasGsap && !reduced) {
      gsap.to(hm, { left: 0, right: 0, borderRadius: 0, ease: 'none',
        scrollTrigger: { trigger: '.hero-media-wrap', start: 'top 70%', end: 'bottom 40%', scrub: true } });
    }
  }

  if (!hasGsap || reduced) return;

  /* ---------- word reveal ---------- */
  document.querySelectorAll('.reveal-words').forEach(el => {
    const words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map(w => `<span class="w">${w}</span>`).join(' ');
    gsap.to(el.querySelectorAll('.w'), { color: 'var(--ink)', stagger: .1, ease: 'none',
      scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 45%', scrub: true } });
  });

  /* ---------- generic reveals ---------- */
  gsap.utils.toArray('.rv').forEach(el => {
    gsap.to(el, { opacity: 1, y: 0, duration: 1.1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%' } });
  });
  gsap.utils.toArray('.split-in').forEach(el => {
    gsap.from(el.querySelectorAll('.row > span'), { yPercent: 110, duration: 1.1, ease: 'expo.out', stagger: .07,
      scrollTrigger: { trigger: el, start: 'top 85%' } });
  });

  /* ---------- image parallax inside frames ---------- */
  gsap.utils.toArray('.tile .ph img, .pbanner img').forEach(img => {
    gsap.fromTo(img, { yPercent: -8 }, { yPercent: 8, ease: 'none',
      scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* ---------- counters ---------- */
  document.querySelectorAll('[data-count]').forEach(el => {
    const end = +el.dataset.count, from = +(el.dataset.from || 0);
    const o = { v: from };
    gsap.to(o, { v: end, duration: 2, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 85%' },
      onUpdate: () => el.firstChild.nodeValue = Math.round(o.v) });
  });

  /* ---------- current wire (draws with scroll) ---------- */
  document.querySelectorAll('svg.wire').forEach(svg => {
    const host = svg.parentElement;
    const build = () => {
      const w = host.offsetWidth, h = host.offsetHeight;
      svg.setAttribute('viewBox', `0 0 ${w} ${h}`); svg.style.height = h + 'px';
      const g = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--gutter')) || 40;
      const x1 = w - g * 1.2, x0 = g * .5;
      const d = `M ${x1} 0 L ${x1} ${h*.28} Q ${x1} ${h*.33} ${x1-60} ${h*.33} L ${x0+60} ${h*.33} Q ${x0} ${h*.33} ${x0} ${h*.38} L ${x0} ${h}`;
      const p = svg.querySelector('path'); p.setAttribute('d', d);
      const len = p.getTotalLength(); p.style.strokeDasharray = len; p.style.strokeDashoffset = len;
      return p;
    };
    const p = build();
    gsap.to(p, { strokeDashoffset: 0, ease: 'none', scrollTrigger: { trigger: host, start: 'top 60%', end: 'bottom 60%', scrub: true, invalidateOnRefresh: true } });
    ScrollTrigger.addEventListener('refreshInit', build);
  });

  window.addEventListener('load', () => ScrollTrigger.refresh());
  document.fonts && document.fonts.ready.then(() => ScrollTrigger.refresh());
})();

/* forms (work without GSAP) */
document.querySelectorAll('form.inq').forEach(f => f.addEventListener('submit', e => {
  e.preventDefault();
  if (!f.checkValidity()) { f.reportValidity(); return; }
  f.classList.add('done');
}));
