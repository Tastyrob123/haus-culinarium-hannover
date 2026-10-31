/*
 * Hover Reveal — Bild folgt dem Cursor, sobald ein Listen-Eintrag berührt wird.
 * Abhängigkeiten: keine. Läuft in jedem Browser-Projekt (HTML, Next.js, super.so, Notion-Custom-Code).
 *
 * Markup:
 *   <ul class="hr-list" data-hover-reveal>
 *     <li class="hr-item" data-hr-src="/img/eins.jpg"><a href="#">Titel</a></li>
 *   </ul>
 *
 * Init:  initHoverReveal()                      → alle [data-hover-reveal] auf der Seite
 *        initHoverReveal(el, { width: 420 })    → ein Container mit Optionen
 *
 * Optionen:
 *   width    (320)   Breite der Bildkarte in px
 *   ratio    (1.25)  Höhe = width * ratio
 *   ease     (0.14)  0.05 = träge Nachlauf-Fahrt, 0.3 = klebt am Cursor
 *   tilt     (12)    max. Neigung in Grad, aus der Cursor-Geschwindigkeit
 *   offsetX/Y (0)    Versatz zum Cursor in px
 *
 * Reduced Motion: Nachlauf und Neigung werden abgeschaltet, das Bild blendet nur ein/aus.
 */

export function initHoverReveal(root, options = {}) {
  if (!root) {
    return Array.from(document.querySelectorAll('[data-hover-reveal]')).map((el) =>
      initHoverReveal(el, options),
    );
  }

  const opts = { width: 320, ratio: 1.25, ease: 0.14, tilt: 12, offsetX: 0, offsetY: 0, ...options };
  const items = Array.from(root.querySelectorAll('[data-hr-src]'));
  if (!items.length) return { destroy() {} };

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Bildkarte einmal bauen, Bilder vorladen, damit beim ersten Hover nichts flackert.
  const card = document.createElement('div');
  card.className = 'hr-card';
  card.setAttribute('aria-hidden', 'true');
  card.style.width = `${opts.width}px`;
  card.style.height = `${Math.round(opts.width * opts.ratio)}px`;
  root.appendChild(card);

  const layers = items.map((item) => {
    const img = document.createElement('img');
    img.src = item.dataset.hrSrc;
    img.alt = '';
    img.loading = 'eager';
    img.decoding = 'async';
    card.appendChild(img);
    return img;
  });

  let mouseX = 0, mouseY = 0;      // Ziel (Cursor)
  let cardX = 0, cardY = 0;        // aktuelle Karten-Position
  let active = -1;                 // Index des gehoverten Eintrags, -1 = keiner
  let raf = null;
  let started = false;

  const bounds = () => root.getBoundingClientRect();

  function onMove(e) {
    const b = bounds();
    mouseX = e.clientX - b.left + opts.offsetX;
    mouseY = e.clientY - b.top + opts.offsetY;
    if (!started) {                // erster Kontakt: Karte springt an den Cursor, statt hereinzufliegen
      cardX = mouseX;
      cardY = mouseY;
      started = true;
    }
  }

  function show(index) {
    if (active === index) return;
    active = index;
    layers.forEach((img, i) => img.classList.toggle('is-active', i === index));
    card.classList.add('is-visible');
    items.forEach((item, i) => item.classList.toggle('is-dimmed', index !== -1 && i !== index));
  }

  function hide() {
    active = -1;
    started = false;
    card.classList.remove('is-visible');
    items.forEach((item) => item.classList.remove('is-dimmed'));
  }

  function tick() {
    const dx = mouseX - cardX;
    const dy = mouseY - cardY;
    cardX += dx * (reduced ? 1 : opts.ease);
    cardY += dy * (reduced ? 1 : opts.ease);
    // Neigung aus der horizontalen Restdistanz — je schneller die Maus, desto stärker.
    const rot = reduced ? 0 : Math.max(-opts.tilt, Math.min(opts.tilt, dx * 0.08));
    card.style.transform = `translate3d(${cardX}px, ${cardY}px, 0) translate(-50%, -50%) rotate(${rot}deg)`;
    raf = requestAnimationFrame(tick);
  }

  const enterHandlers = items.map((item, i) => {
    const fn = () => show(i);
    item.addEventListener('mouseenter', fn);
    // Tastatur: Fokus zeigt dasselbe Bild, mittig über dem Eintrag.
    item.addEventListener('focusin', () => {
      const b = bounds();
      const r = item.getBoundingClientRect();
      mouseX = r.left - b.left + r.width / 2;
      mouseY = r.top - b.top + r.height / 2;
      cardX = mouseX;
      cardY = mouseY;
      started = true;
      show(i);
    });
    item.addEventListener('focusout', hide);
    return fn;
  });

  root.addEventListener('mousemove', onMove);
  root.addEventListener('mouseleave', hide);
  raf = requestAnimationFrame(tick);

  return {
    destroy() {
      cancelAnimationFrame(raf);
      root.removeEventListener('mousemove', onMove);
      root.removeEventListener('mouseleave', hide);
      items.forEach((item, i) => item.removeEventListener('mouseenter', enterHandlers[i]));
      card.remove();
    },
  };
}

export default initHoverReveal;
