// Bug Fix Demo - Interactive explanations
document.querySelectorAll('.toggle input').forEach(cb => {
  cb.addEventListener('change', () => {
    // Force re-render by toggling a class on body
    document.body.classList.toggle('force-repaint');
    requestAnimationFrame(() => document.body.classList.toggle('force-repaint'));
  });
});

// Modal close
document.getElementById('closeModal')?.addEventListener('click', () => {
  document.getElementById('fix3')?.click(); // Toggle off
});

console.log('Bug Fix Demo loaded. Toggle switches to see before/after.');