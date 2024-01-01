// Wait for DOM to load before running the script
document.addEventListener('DOMContentLoaded', function() {
  const grid = document.getElementById('grid');
  if (grid) {
    const divs = grid.getElementsByClassName('item');
    const columns = divs.length > 0 ? Math.floor(grid.offsetWidth / divs[0].offsetWidth) : 0;
    const rows = Math.ceil(divs.length / columns);
  
    for (let i = 0; i < divs.length; i++) {
      const row = Math.floor(i / columns) + 1;
      const column = i % columns + 1;
  
      // Add classes to corners
      if (row === 1 && column === 1) divs[i].classList.add('top-left');
      if (row === 1 && column === columns) divs[i].classList.add('top-right');
      if (row === rows && column === 1) divs[i].classList.add('bottom-left');
      if (row === rows && column === columns) divs[i].classList.add('bottom-right');
    }
  }
});

// Get necessary elements
const xInput = document.getElementById("x-coordinate");
const zInput = document.getElementById("z-coordinate");
const shippingOption1 = document.getElementById("shipping-option-1");
const shippingOption2 = document.getElementById("shipping-option-2");
const shippingCostElement = document.getElementById("shipping-cost");
const totalCostElement = document.getElementById("total-cost");

if (xInput && zInput && shippingOption1 && shippingOption2 && shippingCostElement && totalCostElement) {
  function updateShippingCost() {
    const x = xInput.value;
    const z = zInput.value;
    const distance = Math.ceil(Math.abs(x) + Math.abs(z));
    let shippingCost = 0;
  
    const cartSubtotal = parseFloat(document.getElementById("cart-subtotal").textContent);
  
    // Calculate shipping cost based on cart subtotal and distance
    if (cartSubtotal >= 50) shippingCost = Math.max(0, Math.ceil((distance - 100000) / 5000));
    else if (cartSubtotal >= 20) shippingCost = Math.max(0, Math.ceil((distance - 20000) / 5000));
    else if (cartSubtotal >= 10) shippingCost = Math.max(0, Math.ceil((distance - 5000) / 5000));
    else if (cartSubtotal >= 5) shippingCost = Math.max(0, Math.ceil((distance - 1000) / 5000));
    else shippingCost = Math.ceil(distance / 5000);
  
    // Adjust for express shipping
    if (shippingOption2.checked) shippingCost = (shippingCost*1.5) + 2;
  
    const newTotalCost = cartSubtotal + shippingCost;
  
    // Update costs
    shippingCostElement.innerHTML = "$" + shippingCost.toFixed(2);
    totalCostElement.innerHTML = "$" + newTotalCost.toFixed(2);
  
    const newTotalCostInput = document.getElementById("new-total-cost-input");
    newTotalCostInput.value = newTotalCost.toFixed(2);
  }
  
  // Add event listeners to update costs
  xInput.addEventListener("input", updateShippingCost);
  zInput.addEventListener("input", updateShippingCost);
  shippingOption1.addEventListener("change", updateShippingCost);
  shippingOption2.addEventListener("change", updateShippingCost);
  
  updateShippingCost();
}

// Submit form on quantity change
const quantityInput = document.getElementById('quantityInput');
if (quantityInput) quantityInput.addEventListener('change', () => document.getElementById('updateForm').submit());

// Calculate subtotals
const subtotalElements = document.querySelectorAll('.subtotal');
subtotalElements.forEach((subtotalElement) => {
  const priceElement = subtotalElement.previousElementSibling;
  const quantityElement = priceElement.previousElementSibling;
  const price = parseFloat(priceElement.textContent.replace('$', ''));
  const quantity = parseInt(quantityElement.textContent);
  const subtotal = price * quantity;
  subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
});

// Dark mode toggle
const toggleInput = document.getElementById('dark-mode-toggle');
const body = document.body;
const isDarkMode = localStorage.getItem('darkMode') === 'true';
toggleInput.checked = isDarkMode;
if (isDarkMode) body.classList.add('dark-mode');
else body.classList.remove('dark-mode');
toggleInput.addEventListener('change', () => {
  if (toggleInput.checked) {
    body.classList.add('dark-mode');
    localStorage.setItem('darkMode', 'true');
  } else {
    body.classList.remove('dark-mode');
    localStorage.setItem('darkMode', 'false');
  }
});