// Scroll-snap carousel: the track scrolls natively (swipe, trackpad, keyboard);
// this only wires the arrows, dots, and counter to it.
(() => {
  const c = document.querySelector('.carousel');
  if (!c) return;
  const track = c.querySelector('.track');
  const slides = Array.from(track.querySelectorAll('.slide'));
  const dots = Array.from(c.querySelectorAll('.dots button'));
  const count = c.querySelector('.count');
  const pad = (n) => String(n).padStart(2, '0');
  let cur = 0;

  const mark = (n) => {
    cur = n;
    dots.forEach((d, k) => (k === n ? d.setAttribute('aria-current', 'true') : d.removeAttribute('aria-current')));
    count.textContent = `${pad(n + 1)} / ${pad(slides.length)}`;
  };
  const go = (n) => {
    n = (n + slides.length) % slides.length;
    track.scrollTo({ left: slides[n].offsetLeft, behavior: 'smooth' });
  };

  c.querySelector('.prev').addEventListener('click', () => go(cur - 1));
  c.querySelector('.next').addEventListener('click', () => go(cur + 1));
  dots.forEach((d, k) => d.addEventListener('click', () => go(k)));
  track.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { go(cur + 1); e.preventDefault(); }
    if (e.key === 'ArrowLeft')  { go(cur - 1); e.preventDefault(); }
  });

  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) mark(slides.indexOf(e.target)); });
  }, { root: track, threshold: 0.6 });
  slides.forEach((s) => io.observe(s));
  mark(0);
})();
