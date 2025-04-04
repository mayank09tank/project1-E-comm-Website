# project1-E-comm-Website
# BikesCars E-Commerce Website

A responsive e-commerce website built with Python Flask for selling bikes and cars.

## Features

- Responsive design that works on desktop, tablet, and mobile devices
- User authentication (register, login, logout)
- Product catalog with categories (bikes and cars)
- Product detail pages with specifications
- Shopping cart functionality
- Checkout process
- Order confirmation and history
- Admin panel (coming soon)

## Technologies Used

- Backend: Python 3.x with Flask framework
- Database: SQLite with SQLAlchemy ORM
- Frontend: HTML5, CSS3, JavaScript
- Icons: Font Awesome
- Authentication: Werkzeug security

## Installation and Setup

1. Clone the repository
```
git clone https://github.com/yourusername/bikescars-ecommerce.git
cd bikescars-ecommerce
```

2. Create and activate a virtual environment (recommended)
```
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies
```
pip install -r requirements.txt
```

4. Run the application
```
python app.py
```

5. Open your browser and navigate to `http://127.0.0.1:5000/`

## Project Structure

```
bikescars-ecommerce/
├── app.py                # Main application file
├── requirements.txt      # Project dependencies
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
└── README.md             # This file
```

## Usage

- Browse products by category (Bikes or Cars)
- View product details
- Add products to cart
- Proceed to checkout
- Register an account or login
- Complete the order

## Demo Accounts

For testing purposes, you can create your own account or use the database that will be automatically populated with sample data when the application runs for the first time.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Font Awesome](https://fontawesome.com/)
- [Google Fonts](https://fonts.google.com/) 
