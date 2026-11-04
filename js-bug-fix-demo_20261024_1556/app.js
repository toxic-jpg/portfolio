// Bug Fix Demo - Interactive explanations
document.querySelectorAll('.bug-card').forEach(card => {
  const checkbox = card.querySelector('.toggle input');
  const demo = card.querySelector('.demo');
  if (!checkbox || !demo) return;

  const update = () => {
    if (checkbox.checked) {
      demo.classList.remove('broken');
      demo.classList.add('fixed');
    } else {
      demo.classList.remove('fixed');
      demo.classList.add('broken');
    }
  };

  checkbox.addEventListener('change', update);
  update(); // Initial state
});

// Modal close
const closeBtn = document.getElementById('closeModal');
const fix3 = document.getElementById('fix3');
if (closeBtn && fix3) {
  closeBtn.addEventListener('click', () => {
    fix3.checked = false;
    fix3.dispatchEvent(new Event('change'));
  });
}

console.log('Bug Fix Demo loaded. Toggle switches to see before/after.');
