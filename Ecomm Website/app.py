from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

# ====================================================
# FLASK APP CONFIGURATION
# ====================================================
# Initialize Flask app
app = Flask(__name__)
# Secret key for session management and CSRF protection
app.config['SECRET_KEY'] = 'your-secret-key'
# Set SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
# Disable modification tracking (better performance)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # SMTP server, change if not using Gmail
app.config['MAIL_PORT'] = 587  # SMTP port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your-app-password'  # Replace with your app password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'  # Replace with your email

# Initialize database
db = SQLAlchemy(app)

# Token serializer for password reset
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# ====================================================
# DATABASE MODELS
# ====================================================
# User Model - Stores user information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)

# Product Model - Stores product information
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=10)
    # Relationships
    cart_items = db.relationship('CartItem', backref='product', lazy=True)

# CartItem Model - Links products to user's cart
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

# Order Model - Stores order information
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

# OrderItem Model - Stores items in an order
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

# ====================================================
# EMAIL FUNCTIONS
# ====================================================
def send_email(to, subject, template):
    """
    Function to send email using SMTP
    
    Parameters:
    - to: Recipient email address
    - subject: Email subject line
    - template: HTML content of the email
    
    Returns:
    - True if email sent successfully, False otherwise
    """
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = app.config['MAIL_DEFAULT_SENDER']
    msg['To'] = to
    
    # Attach HTML content
    msg.attach(MIMEText(template, 'html'))
    
    try:
        # Connect to SMTP server
        server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        
        # Send email
        server.sendmail(app.config['MAIL_DEFAULT_SENDER'], to, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def generate_password_reset_token(email):
    """
    Generate password reset token
    
    Parameters:
    - email: The user's email address to encode in the token
    
    Returns:
    - A secure URL-safe token containing the encoded email
    """
    # Uses the serializer to create a secure token with the email embedded
    # 'salt' adds additional security and helps separate different token types
    return serializer.dumps(email, salt='password-reset-salt')

def verify_password_reset_token(token, expiration=3600):
    """
    Verify password reset token
    
    Parameters:
    - token: The token to verify
    - expiration: How long the token is valid in seconds (default 1 hour)
    
    Returns:
    - The email address if token is valid, None otherwise
    """
    try:
        # Attempts to decode the token and extract the email
        # max_age limits how long the token is valid (3600 seconds = 1 hour)
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
        return email
    except SignatureExpired:
        # Token was valid but has expired
        return None
    except Exception:
        # Token was invalid (tampered with or incorrect)
        return None

# ====================================================
# DATABASE INITIALIZATION AND SAMPLE DATA
# ====================================================
# Create database tables and add sample products
with app.app_context():
    # Create all database tables
    db.create_all()
    
    # Add dummy products if none exist
    if Product.query.count() == 0:
        dummy_products = [
            # Bikes
            Product(name='Mountain Bike Pro', description='High-performance mountain bike for rough terrains', 
                   price=899.99, image='mountain_bike.jpg', category='bike', stock=15),
            Product(name='Road Racer X3', description='Lightweight road bike for speed enthusiasts', 
                   price=1299.99, image='road_bike.jpg', category='bike', stock=10),
            Product(name='City Cruiser', description='Comfortable bike for city commuting', 
                   price=499.99, image='city_bike.jpg', category='bike', stock=20),
            Product(name='BMX Extreme', description='Stunt bike for tricks and jumps', 
                   price=349.99, image='bmx_bike.jpg', category='bike', stock=8),
            Product(name='Electric Bike E1', description='Electric-assisted bike with long battery life', 
                   price=1599.99, image='electric_bike.jpg', category='bike', stock=12),
            
            # Cars
            Product(name='Sedan Luxury', description='Elegant sedan with premium features', 
                   price=35000.00, image='sedan.jpg', category='car', stock=5),
            Product(name='SUV Explorer', description='Spacious SUV for family adventures', 
                   price=42000.00, image='suv.jpg', category='car', stock=7),
            Product(name='Sports Coupe', description='High-speed sports car for thrill-seekers', 
                   price=65000.00, image='sports_car.jpg', category='car', stock=3),
            Product(name='Electric Tesla Clone', description='Eco-friendly electric car with advanced technology', 
                   price=48000.00, image='electric_car.jpg', category='car', stock=6),
            Product(name='Pickup Truck Pro', description='Robust pickup truck for heavy-duty tasks', 
                   price=38000.00, image='pickup.jpg', category='car', stock=8)
        ]
        
        # Add each product to the database
        for product in dummy_products:
            db.session.add(product)
        
        # Commit changes to the database
        db.session.commit()

# ====================================================
# ROUTE: HOME PAGE
# ====================================================
@app.route('/')
def home():
    """Home page displays all products"""
    # Get all products from database
    products = Product.query.all()
    # Render the home page template with products
    return render_template('index.html', products=products)

# ====================================================
# ROUTE: PRODUCT CATEGORY PAGE
# ====================================================
@app.route('/products/<category>')
def products_by_category(category):
    """Shows products of a specific category (bike or car)"""
    # Get products filtered by category
    products = Product.query.filter_by(category=category).all()
    # Render the products page template with filtered products
    return render_template('products.html', products=products, category=category)

# ====================================================
# ROUTE: PRODUCT DETAIL PAGE
# ====================================================
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Shows detailed information about a specific product"""
    # Get the product or return 404 if not found
    product = Product.query.get_or_404(product_id)
    # Render the product detail template
    return render_template('product_detail.html', product=product)

# ====================================================
# ROUTE: SHOPPING CART PAGE
# ====================================================
@app.route('/cart')
def cart():
    """Shows the user's shopping cart"""
    # Check if user is logged in
    if 'user_id' not in session:
        # If not logged in, redirect to login page
        return redirect(url_for('login'))
    
    # Get user's cart items
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    # Calculate total price of items in cart
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    # Render cart template with cart items and total
    return render_template('cart.html', cart_items=cart_items, total=total)

# ====================================================
# ROUTE: ADD TO CART FUNCTIONALITY
# ====================================================
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Adds a product to the user's cart"""
    # Check if user is logged in
    if 'user_id' not in session:
        # If not logged in, redirect to login page
        return redirect(url_for('login'))
    
    # Get quantity from form (default to 1 if not specified)
    quantity = int(request.form.get('quantity', 1))
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(user_id=session['user_id'], product_id=product_id).first()
    
    if cart_item:
        # If item already in cart, update quantity
        cart_item.quantity += quantity
    else:
        # If item not in cart, add new cart item
        cart_item = CartItem(user_id=session['user_id'], product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    # Save changes to database
    db.session.commit()
    # Show success message
    flash('Item added to cart!', 'success')
    # Redirect to product detail page
    return redirect(url_for('product_detail', product_id=product_id))

# ====================================================
# ROUTE: CHECKOUT PAGE AND PROCESS
# ====================================================
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Displays checkout form and processes orders"""
    # Check if user is logged in
    if 'user_id' not in session:
        # If not logged in, redirect to login page
        return redirect(url_for('login'))
    
    # Process checkout form submission
    if request.method == 'POST':
        # Get user's cart items
        cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        
        # Check if cart is empty
        if not cart_items:
            flash('Your cart is empty!', 'danger')
            return redirect(url_for('cart'))
        
        # Calculate total order amount
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        # Create new order
        order = Order(user_id=session['user_id'], total_amount=total_amount)
        db.session.add(order)
        db.session.flush()  # Get the order ID without committing
        
        # Create order items for each cart item
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product.id,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)
            
            # Update product stock
            product = item.product
            product.stock -= item.quantity
            
        # Clear the cart after order is placed
        for item in cart_items:
            db.session.delete(item)
            
        # Save all changes to database
        db.session.commit()
        # Show success message
        flash('Order placed successfully!', 'success')
        # Redirect to order confirmation page
        return redirect(url_for('order_confirmation', order_id=order.id))
    
    # Display checkout page (GET request)
    # Get user's cart items
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    # Calculate total price of items in cart
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    # Render checkout template with cart items and total
    return render_template('checkout.html', cart_items=cart_items, total=total)

# ====================================================
# ROUTE: ORDER CONFIRMATION PAGE
# ====================================================
@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    """Shows order confirmation details after successful purchase"""
    # Check if user is logged in
    if 'user_id' not in session:
        # If not logged in, redirect to login page
        return redirect(url_for('login'))
    
    # Get the order or return 404 if not found
    order = Order.query.get_or_404(order_id)
    
    # Check if order belongs to current user
    if order.user_id != session['user_id']:
        # If not, show error and redirect to home
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('home'))
    
    # Render order confirmation template
    return render_template('order_confirmation.html', order=order)

# ====================================================
# ROUTE: USER REGISTRATION
# ====================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration process"""
    # Process registration form submission
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        
        if existing_user:
            # If user exists, show error and redirect back to register page
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            # Hash password for security
            password_hash=generate_password_hash(password)
        )
        
        # Add user to database
        db.session.add(new_user)
        db.session.commit()
        
        # Show success message
        flash('Registration successful! Please log in.', 'success')
        # Redirect to login page
        return redirect(url_for('login'))
    
    # Display registration page (GET request)
    return render_template('register.html')

# ====================================================
# ROUTE: USER LOGIN
# ====================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login process"""
    # Process login form submission
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password_hash, password):
            # Store user info in session
            session['user_id'] = user.id
            session['username'] = user.username
            # Show success message
            flash('Login successful!', 'success')
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # If login failed, show error
            flash('Invalid username or password!', 'danger')
    
    # Display login page (GET request)
    return render_template('login.html')

# ====================================================
# ROUTE: USER LOGOUT
# ====================================================
@app.route('/logout')
def logout():
    """Logs out the current user by clearing their session"""
    # Clear user session
    session.clear()
    # Show success message
    flash('You have been logged out!', 'success')
    # Redirect to home page
    return redirect(url_for('home'))

# ====================================================
# ROUTE: FORGOT PASSWORD
# ====================================================
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """
    Handles password reset request
    
    GET: Displays the form to enter email
    POST: Processes the email submission and sends reset link
    """
    # Process form submission - When user submits email for reset
    if request.method == 'POST':
        # Get email from form - Extract submitted email
        email = request.form['email']
        
        # Check if email exists in database - Find user with this email
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate token and reset link - Create secure reset token
            token = generate_password_reset_token(email)  # Generate unique token with email embedded
            # Create full URL for reset page including token - Complete reset link
            reset_url = url_for('reset_password', token=token, _external=True)  # _external=True makes absolute URL
            
            # Create email template - HTML email content
            subject = "BikesCars - Password Reset Request"  # Email subject line
            # HTML email body with personalized greeting and reset link
            template = f"""
            <html>
            <body>
                <h2>Password Reset Request</h2>
                <p>Hi {user.username},</p>
                <p>We received a request to reset your password. Please click the link below to reset your password:</p>
                <p><a href="{reset_url}">Reset Your Password</a></p>
                <p>If you did not request a password reset, please ignore this email.</p>
                <p>This link will expire in 1 hour.</p>
                <p>Thank you,<br>BikesCars Team</p>
            </body>
            </html>
            """
            
            # Send email - Attempt to send the email with reset link
            email_sent = send_email(email, subject, template)  # Returns True/False based on success
            
            if email_sent:
                # Successful email sending - Inform user to check email
                flash('A password reset link has been sent to your email.', 'success')
            else:
                # Email sending failed - Technical error
                flash('Could not send reset email. Please try again later.', 'danger')
        else:
            # Don't reveal if email exists for security - Prevents email enumeration attacks
            # This message is intentionally the same as success to avoid revealing if email exists
            flash('A password reset link has been sent to your email if it exists in our system.', 'success')
        
        # Redirect to login page - Return to login page after request
        return redirect(url_for('login'))
    
    # Display the forgot password form (GET request) - Show form to enter email
    return render_template('forgot_password.html')

# ====================================================
# ROUTE: RESET PASSWORD
# ====================================================
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Handles password reset with token
    
    GET: Displays form to enter new password
    POST: Processes the new password submission
    
    Parameters:
    - token: The secure token from the reset link
    """
    # Verify token - Check if token is valid and not expired
    email = verify_password_reset_token(token)  # Extract email from token if valid
    
    # If token invalid or expired - Security check
    if not email:
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('forgot_password'))  # Return to request page
    
    # Process form submission - When user submits new password
    if request.method == 'POST':
        # Get password data - Extract submitted passwords
        password = request.form['password']  # New password
        confirm_password = request.form['confirm_password']  # Confirmation entry
        
        # Validate password match - Ensure both entries are identical
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('reset_password.html', token=token)  # Show form again
        
        # Update user's password - Find user and change password
        user = User.query.filter_by(email=email).first()
        if user:
            # Set new password hash - Update password with secure hash
            user.password_hash = generate_password_hash(password)
            db.session.commit()  # Save changes
            flash('Your password has been updated! You can now login.', 'success')
            return redirect(url_for('login'))  # Go to login page
        else:
            # User not found (rare case) - Email from token doesn't match any user
            flash('User not found.', 'danger')
            return redirect(url_for('login'))
    
    # Display the reset password form (GET request) - Show form to enter new password
    # Pass token to template to maintain it in the form submission
    return render_template('reset_password.html', token=token)

# ====================================================
# RUN THE APP
# ====================================================
if __name__ == '__main__':
    # Start the Flask app in debug mode
    app.run(debug=True) 