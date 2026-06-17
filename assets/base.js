
// Fix: re-apply strikethrough on compare-at prices after app JS strips inline styles
function fixCompareAtStrikethrough() {
  document.querySelectorAll('s.cart-item__old-price').forEach(function(el) {
    el.style.setProperty('text-decoration', 'line-through', 'important');
    el.style.setProperty('opacity', '0.7');
  });
}

document.addEventListener('DOMContentLoaded', fixCompareAtStrikethrough);
document.addEventListener('cart:updated', fixCompareAtStrikethrough);
document.addEventListener('cart-drawer:open', fixCompareAtStrikethrough);

// Also observe DOM mutations in case app rewrites after load
const cartObserver = new MutationObserver(fixCompareAtStrikethrough);
document.addEventListener('DOMContentLoaded', function() {
  const cartEl = document.querySelector('.cart-items, #CartDrawer');
  if (cartEl) cartObserver.observe(cartEl, { childList: true, subtree: true });
});
