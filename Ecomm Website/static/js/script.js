/**
 * ===========================================================
 * MAIN JAVASCRIPT FILE
 * This file contains all interactive functionality for the website
 * ===========================================================
 */

// Wait for the DOM to be fully loaded before running any code
document.addEventListener('DOMContentLoaded', () => {
    // ====================================================
    // MOBILE MENU TOGGLE
    // ====================================================
    // Get references to the menu button and navigation menu
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');
    
    // Setup mobile menu toggle if the button exists
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            // Toggle the active class to show/hide the menu
            navMenu.classList.toggle('active');
            
            // Change icon based on menu state (hamburger <-> close)
            const icon = mobileMenuBtn.querySelector('i');
            if (navMenu.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }
    
    // ====================================================
    // CLOSE MOBILE MENU WHEN CLICKING OUTSIDE
    // ====================================================
    document.addEventListener('click', (e) => {
        // Check if menu is active and click was outside menu and button
        if (navMenu && navMenu.classList.contains('active') && 
            !e.target.closest('.nav-menu') && 
            !e.target.closest('.mobile-menu-btn')) {
            // Hide the menu
            navMenu.classList.remove('active');
            
            // Reset the icon to hamburger
            const icon = mobileMenuBtn.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });

    // ====================================================
    // AUTO-DISMISS FLASH MESSAGES
    // ====================================================
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        // After 5 seconds, fade out the message
        setTimeout(() => {
            message.style.opacity = '0';
            // Remove the message after fade out animation
            setTimeout(() => {
                message.remove();
            }, 500); // 0.5 second for fade out
        }, 5000); // 5 seconds display time
    });

    // ====================================================
    // PRODUCT QUANTITY CONTROLS
    // ====================================================
    const quantityInput = document.querySelector('.quantity-input');
    if (quantityInput) {
        // Get the minus and add buttons
        const minBtn = document.querySelector('.quantity-min');
        const addBtn = document.querySelector('.quantity-add');

        // Decrease quantity when minus button is clicked
        if (minBtn) {
            minBtn.addEventListener('click', (e) => {
                e.preventDefault(); // Prevent form submission
                let value = parseInt(quantityInput.value);
                // Ensure quantity doesn't go below 1
                if (value > 1) {
                    quantityInput.value = value - 1;
                }
            });
        }

        // Increase quantity when add button is clicked
        if (addBtn) {
            addBtn.addEventListener('click', (e) => {
                e.preventDefault(); // Prevent form submission
                let value = parseInt(quantityInput.value);
                // Get maximum quantity (from stock) or default to 100
                const max = parseInt(quantityInput.getAttribute('max') || 100);
                // Ensure quantity doesn't exceed max
                if (value < max) {
                    quantityInput.value = value + 1;
                }
            });
        }
    }

    // ====================================================
    // CART QUANTITY UPDATE
    // ====================================================
    const cartQuantityInputs = document.querySelectorAll('.cart-quantity-input');
    cartQuantityInputs.forEach(input => {
        // Auto-submit form when quantity changes
        input.addEventListener('change', function() {
            // Get the form ID from data attribute
            const formId = this.getAttribute('data-form-id');
            const form = document.getElementById(formId);
            // Submit the form to update cart
            if (form) {
                form.submit();
            }
        });
    });

    // ====================================================
    // FORM VALIDATION
    // ====================================================
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            // Check if form is valid
            if (!form.checkValidity()) {
                // Prevent form submission if invalid
                event.preventDefault();
                event.stopPropagation();
            }
            // Add validation class to show validation feedback
            form.classList.add('was-validated');
        }, false);
    });

    // ====================================================
    // PRODUCT FILTER CONTROLS
    // ====================================================
    const filterItems = document.querySelectorAll('.filter-item');
    const productItems = document.querySelectorAll('.product-card');

    filterItems.forEach(item => {
        item.addEventListener('click', function() {
            // Get filter value (all, mountain, road, etc.)
            const filterValue = this.getAttribute('data-filter');
            
            // Update active class on filter buttons
            filterItems.forEach(filter => filter.classList.remove('active'));
            this.classList.add('active');
            
            // Filter products based on selected category
            if (filterValue === 'all') {
                // Show all products
                productItems.forEach(product => {
                    product.style.display = 'block';
                });
            } else {
                // Show only products that match the filter
                productItems.forEach(product => {
                    if (product.classList.contains(filterValue)) {
                        product.style.display = 'block';
                    } else {
                        product.style.display = 'none';
                    }
                });
            }
        });
    });
}); 