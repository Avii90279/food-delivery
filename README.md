# Foodie - Food Delivery Website

A complete full-stack food delivery website similar to Swiggy, built with modern technologies.

## 🚀 Tech Stack

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling with Swiggy-like design (Orange theme #FC8019)
- **JavaScript (Vanilla)** - Client-side logic
- **Fetch API** - Backend communication
- **Responsive Design** - Mobile-first approach
- **localStorage** - JWT token storage

### Backend
- **FastAPI** - Python web framework
- **JWT Authentication** - Secure user authentication
- **REST APIs** - RESTful API design
- **SQLAlchemy ORM** - Database ORM

### Database
- **PostgreSQL** - Relational database
- **Supabase** - Cloud database hosting

## 📋 Features

### Authentication
- User Registration
- User Login
- JWT Token Storage
- Logout
- Role-based access (User/Admin)

### Restaurant Features
- Browse Restaurants
- Search Restaurants
- Filter by Rating
- Filter by Category
- Restaurant Details
- Menu Categories

### Food Features
- Browse Food Items
- Food Images
- Price Display
- Vegetarian/Non-Vegetarian Indicators
- Add to Cart

### Cart Features
- Add Items to Cart
- Remove Items from Cart
- Update Quantity
- Total Price Calculation
- GST Calculation (5%)
- Delivery Charges

### Order Features
- Place Order
- Order Tracking
- Order History
- Order Status Updates
- Order Summary

### Review System
- Restaurant Reviews
- Food Ratings
- User Comments

### Coupon System
- Apply Discount Coupons
- Percentage and Flat Discounts
- Minimum Order Validation
- Coupon Validation

### Admin Dashboard
- Dashboard Statistics
- Manage Restaurants
- Manage Food Items
- Manage Categories
- Manage Orders
- Manage Users
- Manage Coupons

## 📁 Project Structure

```
foodie/
├── frontend/
│   ├── css/
│   │   ├── style.css          # Main styles
│   │   ├── auth.css           # Authentication styles
│   │   └── admin.css          # Admin dashboard styles
│   ├── js/
│   │   ├── api.js             # API client
│   │   ├── auth.js            # Authentication logic
│   │   ├── cart.js            # Cart functionality
│   │   └── orders.js          # Orders functionality
│   ├── images/                # Static images
│   ├── index.html             # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Register page
│   ├── restaurants.html       # Restaurant listing
│   ├── menu.html              # Restaurant menu
│   ├── cart.html              # Shopping cart
│   ├── checkout.html          # Checkout page
│   ├── profile.html           # User profile
│   ├── orders.html            # Order history
│   └── admin.html             # Admin dashboard
├── backend/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py        # Application settings
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py     # JWT token handling
│   │   ├── password.py        # Password hashing
│   │   └── dependencies.py    # Auth dependencies
│   ├── models/
│   │   └── __init__.py        # Database models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py            # Auth routes
│   │   ├── restaurants.py     # Restaurant routes
│   │   ├── foods.py           # Food routes
│   │   ├── categories.py      # Category routes
│   │   ├── cart.py            # Cart routes
│   │   ├── orders.py          # Order routes
│   │   ├── reviews.py         # Review routes
│   │   ├── coupons.py         # Coupon routes
│   │   ├── addresses.py       # Address routes
│   │   └── users.py           # User routes
│   ├── services/
│   │   └── __init__.py
│   ├── database.py            # Database configuration
│   ├── main.py                # FastAPI application
│   ├── seed_data.py           # Sample data seeder
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
└── README.md                  # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- Node.js (optional, for development)

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure environment variables**

Edit `.env` file with your database credentials:
```
DATABASE_URL=postgresql://postgres:your_password@your_host:5432/your_database
SECRET_KEY=your_secret_key
```

6. **Run database migrations**
```bash
python seed_data.py
```

This will create all database tables and populate them with sample data.

7. **Start the FastAPI server**
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Open index.html in a browser**

You can use any static file server or simply open the HTML files directly in your browser.

**Using Python's built-in server:**
```bash
cd frontend
python -m http.server 5500
```

Then open `http://localhost:5500` in your browser.

**Using VS Code Live Server:**
- Install Live Server extension
- Right-click on `index.html`
- Select "Open with Live Server"

## 🎨 Design Features

### Color Theme
- **Primary Color:** #FC8019 (Orange)
- **Text Dark:** #3d4152
- **Text Light:** #686b78
- **Background Light:** #f9f9f9
- **Background White:** #ffffff

### UI Components
- Modern Navbar
- Hero Section
- Category Cards
- Restaurant Cards
- Food Cards
- Cart Items
- Order Summary
- Admin Dashboard Tables
- Modals for Forms

### Effects
- Smooth Animations
- Hover Effects
- Loading Spinners
- Glassmorphism Effects
- Toast Notifications

## 🔐 Default Admin Credentials

After running the seed script, you can login with:

- **Email:** admin@foodie.com
- **Password:** admin123

## 📊 Database Schema

### Tables
- **users** - User accounts
- **categories** - Food categories
- **restaurants** - Restaurant information
- **foods** - Food items
- **addresses** - User addresses
- **cart** - Shopping carts
- **cart_items** - Cart items
- **orders** - Orders
- **order_items** - Order items
- **reviews** - Reviews and ratings
- **coupons** - Discount coupons

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Restaurants
- `GET /api/restaurants` - Get all restaurants
- `GET /api/restaurants/{id}` - Get restaurant by ID
- `POST /api/restaurants` - Create restaurant (Admin)
- `PUT /api/restaurants/{id}` - Update restaurant (Admin)
- `DELETE /api/restaurants/{id}` - Delete restaurant (Admin)

### Foods
- `GET /api/foods` - Get all foods
- `GET /api/foods/{id}` - Get food by ID
- `POST /api/foods` - Create food (Admin)
- `PUT /api/foods/{id}` - Update food (Admin)
- `DELETE /api/foods/{id}` - Delete food (Admin)

### Categories
- `GET /api/categories` - Get all categories
- `GET /api/categories/{id}` - Get category by ID
- `POST /api/categories` - Create category (Admin)
- `PUT /api/categories/{id}` - Update category (Admin)
- `DELETE /api/categories/{id}` - Delete category (Admin)

### Cart
- `GET /api/cart` - Get user's cart
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/items/{id}` - Update cart item
- `DELETE /api/cart/items/{id}` - Remove cart item
- `DELETE /api/cart` - Clear cart

### Orders
- `GET /api/orders` - Get user's orders
- `GET /api/orders/{id}` - Get order by ID
- `POST /api/orders` - Create order
- `PUT /api/orders/{id}/status` - Update order status (Admin)

### Reviews
- `GET /api/reviews` - Get reviews
- `POST /api/reviews` - Create review

### Coupons
- `GET /api/coupons` - Get coupons
- `POST /api/coupons/validate` - Validate coupon
- `POST /api/coupons` - Create coupon (Admin)
- `DELETE /api/coupons/{id}` - Delete coupon (Admin)

### Addresses
- `GET /api/addresses` - Get user's addresses
- `POST /api/addresses` - Create address
- `PUT /api/addresses/{id}` - Update address
- `DELETE /api/addresses/{id}` - Delete address

### Users
- `GET /api/users/me` - Get current user
- `PUT /api/users/me` - Update current user
- `GET /api/users` - Get all users (Admin)

## 🚀 Deployment

### Backend Deployment (FastAPI)

1. **Deploy to a cloud platform** (e.g., Railway, Render, Heroku, AWS)

2. **Set environment variables** in your deployment platform:
```
DATABASE_URL=your_production_database_url
SECRET_KEY=your_production_secret_key
```

3. **Build and run** the FastAPI application

### Frontend Deployment

1. **Deploy to a static hosting service** (e.g., Netlify, Vercel, GitHub Pages)

2. **Update API base URL** in `frontend/js/api.js`:
```javascript
const API_BASE_URL = 'https://your-backend-url.com';
```

3. **Deploy** the frontend folder

### Using Supabase (Current Setup)

The project is configured to use Supabase PostgreSQL. The database URL is already set in the `.env` file.

## 📝 Sample Data

The `seed_data.py` script creates:

- **8 Categories** (Indian, Chinese, Italian, Mexican, Burgers, Pizza, Biryani, Desserts)
- **8 Restaurants** with sample data
- **32 Food Items** across all restaurants
- **4 Coupons** (FIRST50, SAVE100, WELCOME20, FREEDelivery)
- **1 Admin User** (admin@foodie.com / admin123)

## 🎯 Usage

### For Users
1. Register a new account
2. Browse restaurants and foods
3. Add items to cart
4. Checkout with address and payment
5. Track orders

### For Admins
1. Login with admin credentials
2. Access admin dashboard
3. Manage restaurants, foods, categories
4. View and manage orders
5. Create and manage coupons

## 🔧 Troubleshooting

### Backend Issues
- Ensure PostgreSQL is running
- Check database URL in `.env`
- Verify all dependencies are installed
- Check FastAPI logs for errors

### Frontend Issues
- Ensure backend is running
- Check API base URL in `api.js`
- Verify browser console for errors
- Clear browser cache

### Database Issues
- Run `seed_data.py` to recreate tables
- Check database connection
- Verify database credentials

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Built as a complete full-stack food delivery website demonstration.

## 🙏 Acknowledgments

- Design inspired by Swiggy
- Built with FastAPI and Vanilla JavaScript
- Database hosted on Supabase

---

**Foodie - Food Delivered Faster** 🍔
