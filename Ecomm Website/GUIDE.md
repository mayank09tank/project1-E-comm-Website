# BikesCars E-Commerce Website - User Guide

In this document, we'll help you understand the project structure and code of the BikesCars e-commerce website.

## Project Structure

```
bikescars-ecommerce/
├── app.py                # Main application file
├── requirements.txt      # Required dependencies
├── static/               # Static files
│   ├── css/              # CSS files
│   │   └── style.css     # Main stylesheet
│   ├── js/               # JavaScript files
│   │   └── script.js     # Main JavaScript file
│   └── images/           # Product images
├── templates/            # HTML templates
│   ├── base.html         # Base template (layout)
│   ├── index.html        # Home page
│   ├── products.html     # Product category page
│   ├── product_detail.html # Product detail page
│   ├── cart.html         # Shopping cart page
│   ├── checkout.html     # Checkout page
│   ├── order_confirmation.html # Order confirmation page
│   ├── login.html        # Login page
│   └── register.html     # Registration page
└── GUIDE.md              # This file
```

## Main Files and Their Purpose

### 1. app.py
This is the main application file that runs the web application using Flask. It includes:

- **Database Models**: User, Product, CartItem, Order, and OrderItem
- **Routes**: For home, product listing, cart, checkout, user authentication, etc.
- **Database Initialization**: Creating tables and dummy products

### 2. static/css/style.css
This file handles all CSS styling and is organized into various sections:

- **Variables and Global Styles**: Consistent colors and styles for all pages
- **Header and Navigation**: Top navigation bar
- **Hero Section**: Main banner on the home page
- **Product Grid and Cards**: Product listings
- **Product Details**: Product detail page
- **Cart and Checkout**: Shopping cart and payment process
- **Footer**: Links and information at the bottom of the page
- **Responsive Styles**: Adaptations for mobile and tablet devices

### 3. static/js/script.js
This JavaScript file provides user interaction and client-side functionality:

- **Mobile Menu Toggle**: Opening and closing the navigation menu on small screens
- **Product Quantity Controls**: Buttons to increase and decrease product quantity
- **Cart Update**: Updating product quantity in the cart
- **Form Validation**: Validation for checkout and user forms
- **Product Filter**: Filtering products on category pages

### 4. templates/
This folder contains all HTML templates:

- **base.html**: Base layout for all pages including header and footer
- **index.html**: Home page with featured products and hero section
- **products.html**: Category-wise product listing page
- **product_detail.html**: Product details and "add to cart" functionality
- **cart.html**: Shopping cart view
- **checkout.html**: Checkout and payment process
- **order_confirmation.html**: Order confirmation page
- **login.html and register.html**: User authentication pages

## How to Get Started

1. Create a Python virtual environment:
```
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux
```

2. Install required packages:
```
pip install -r requirements.txt
```

3. Run the application:
```
python app.py
```

4. Open `http://127.0.0.1:5000/` in your browser

## Key Functionalities

### 1. User Accounts
- **Registration**: Create a new account
- **Login/Logout**: Access or log out of your account

### 2. Product Browsing
- **Category Filtering**: View bikes and cars separately
- **Product Details**: View detailed information and specifications

### 3. Shopping Cart
- **Add Items**: Add products to cart
- **Update Quantity**: Change product quantity
- **Remove Items**: Remove products from cart

### 4. Checkout
- **Shipping Information**: Enter address for delivery
- **Payment**: Add payment details
- **Order Confirmation**: Order confirmation and tracking information

## Database Models Explained

### User
- **Fields**: id, username, email, password_hash
- **Relationships**: orders, cart_items
- **Purpose**: User authentication and order tracking

### Product
- **Fields**: id, name, description, price, image, category, stock
- **Relationships**: cart_items
- **Purpose**: Product information and inventory management

### CartItem
- **Fields**: id, user_id, product_id, quantity
- **Relationships**: user, product
- **Purpose**: Track products and quantities in a user's cart

### Order
- **Fields**: id, user_id, order_date, total_amount, status
- **Relationships**: customer, order_items
- **Purpose**: Order information and status tracking

### OrderItem
- **Fields**: id, order_id, product_id, product_name, quantity, price
- **Relationships**: order
- **Purpose**: Keep details of each product in an order

## Code Modification Guide

If you want to make changes to the code, here are some common modifications and their locations:

### Adding New Products
Add products to the `dummy_products` list in `app.py`.

### Changing UI Style
Modify colors or styling in the `static/css/style.css` file.

### Adding a New Page
1. Create a new HTML template in the `templates/` folder
2. Add a new route for it in `app.py`

### Changing Website Name
1. Change all instances of "BikesCars" in `templates/base.html`
2. Update the logo style in `static/css/style.css`

## FAQ (Frequently Asked Questions)

### Q: Which file should I look at first?
A: Start with `app.py`, which defines all the routes and models for the application.

### Q: Where do I modify the CSS?
A: All styles are defined in `static/css/style.css`.

### Q: How do I deploy this?
A: For production deployment, you can use Heroku, AWS, or other cloud platforms. You'll need to change the SECRET_KEY and remove debug mode from `app.run()`.

### Q: How do I add a real payment gateway?
A: In the `checkout` route, integrate an SDK for a service like Stripe or PayPal for payment processing.

### Q: Is this SEO-friendly?
A: You can add meta tags in `templates/base.html` and improve the semantic HTML usage for better SEO.

## Tips for Better Understanding the Code

1. **Understand Routes**: See how each URL path in `app.py` is connected to a function
2. **Template Inheritance**: How all pages inherit from `base.html`
3. **JavaScript Interaction**: Explore client-side logic in `script.js`
4. **Responsive Design**: Learn how CSS media queries handle mobile and tablet views

This guide should help you develop an understanding of the project and customize it to your needs. If you have more questions, check the comments in the code which explain the purpose of each section. 