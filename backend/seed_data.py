"""
Seed data script for Foodie database
Populates the database with sample restaurants, foods, categories, etc.
"""
from database import SessionLocal, Base, engine
from models import User, Category, Restaurant, Food, Coupon
from auth.password import hash_password

def seed_data():
    """Seed the database with sample data"""
    db = SessionLocal()
    
    try:
        # Create admin user
        admin = db.query(User).filter(User.email == "admin@foodie.com").first()
        if not admin:
            admin = User(
                email="admin@foodie.com",
                username="admin",
                full_name="Admin User",
                phone="9876543210",
                password=hash_password("admin123"),
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("Created admin user")
        
        # Create categories
        categories_data = [
            {"name": "Indian", "description": "Authentic Indian cuisine", "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=200"},
            {"name": "Chinese", "description": "Delicious Chinese dishes", "image_url": "https://images.unsplash.com/photo-1525755662778-989d0524087e?w=200"},
            {"name": "Italian", "description": "Italian pasta and pizza", "image_url": "https://images.unsplash.com/photo-1595295333158-4742f28fbd85?w=200"},
            {"name": "Mexican", "description": "Spicy Mexican food", "image_url": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=200"},
            {"name": "Burgers", "description": "Juicy burgers and fries", "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=200"},
            {"name": "Pizza", "description": "Fresh baked pizzas", "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=200"},
            {"name": "Biryani", "description": "Flavorful biryani dishes", "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=200"},
            {"name": "Desserts", "description": "Sweet treats and desserts", "image_url": "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=200"},
        ]
        
        categories = []
        for cat_data in categories_data:
            existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
            if not existing:
                category = Category(**cat_data)
                db.add(category)
                db.commit()
                db.refresh(category)
                categories.append(category)
                print(f"Created category: {category.name}")
            else:
                categories.append(existing)
        
        # Create restaurants
        restaurants_data = [
            {
                "name": "Spice Garden",
                "description": "Authentic Indian cuisine with rich flavors",
                "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400",
                "address": "123 Main Street, Mumbai",
                "phone": "9876543210",
                "rating": 4.5,
                "delivery_time": "30-40 mins",
                "delivery_fee": 40,
                "category_id": categories[0].id if categories else None
            },
            {
                "name": "Dragon Wok",
                "description": "Best Chinese food in town",
                "image_url": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=400",
                "address": "456 Park Avenue, Delhi",
                "phone": "9876543211",
                "rating": 4.3,
                "delivery_time": "35-45 mins",
                "delivery_fee": 35,
                "category_id": categories[1].id if categories else None
            },
            {
                "name": "Bella Italia",
                "description": "Authentic Italian pasta and pizza",
                "image_url": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=400",
                "address": "789 Church Street, Bangalore",
                "phone": "9876543212",
                "rating": 4.7,
                "delivery_time": "25-35 mins",
                "delivery_fee": 45,
                "category_id": categories[2].id if categories else None
            },
            {
                "name": "Taco Fiesta",
                "description": "Spicy Mexican food and tacos",
                "image_url": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400",
                "address": "321 Market Road, Chennai",
                "phone": "9876543213",
                "rating": 4.2,
                "delivery_time": "30-40 mins",
                "delivery_fee": 30,
                "category_id": categories[3].id if categories else None
            },
            {
                "name": "Burger Barn",
                "description": "Juicy burgers and crispy fries",
                "image_url": "https://images.unsplash.com/photo-1466978913421-dad2ebd01d17?w=400",
                "address": "654 Food Court, Hyderabad",
                "phone": "9876543214",
                "rating": 4.6,
                "delivery_time": "20-30 mins",
                "delivery_fee": 25,
                "category_id": categories[4].id if categories else None
            },
            {
                "name": "Pizza Paradise",
                "description": "Fresh baked pizzas with various toppings",
                "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400",
                "address": "987 Pizza Lane, Pune",
                "phone": "9876543215",
                "rating": 4.4,
                "delivery_time": "25-35 mins",
                "delivery_fee": 35,
                "category_id": categories[5].id if categories else None
            },
            {
                "name": "Biryani House",
                "description": "Flavorful biryani dishes",
                "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400",
                "address": "147 Spice Street, Kolkata",
                "phone": "9876543216",
                "rating": 4.8,
                "delivery_time": "35-45 mins",
                "delivery_fee": 40,
                "category_id": categories[6].id if categories else None
            },
            {
                "name": "Sweet Delights",
                "description": "Sweet treats and desserts",
                "image_url": "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=400",
                "address": "258 Dessert Road, Jaipur",
                "phone": "9876543217",
                "rating": 4.5,
                "delivery_time": "20-30 mins",
                "delivery_fee": 20,
                "category_id": categories[7].id if categories else None
            },
        ]
        
        restaurants = []
        for rest_data in restaurants_data:
            existing = db.query(Restaurant).filter(Restaurant.name == rest_data["name"]).first()
            if not existing:
                restaurant = Restaurant(**rest_data)
                db.add(restaurant)
                db.commit()
                db.refresh(restaurant)
                restaurants.append(restaurant)
                print(f"Created restaurant: {restaurant.name}")
            else:
                restaurants.append(existing)
        
        # Create foods
        foods_data = []
        
        # Indian foods
        if restaurants:
            foods_data.extend([
                {"name": "Butter Chicken", "description": "Creamy tomato-based curry with tender chicken", "price": 299, "is_vegetarian": False, "restaurant_id": restaurants[0].id, "category_id": categories[0].id},
                {"name": "Paneer Tikka", "description": "Grilled cottage cheese with spices", "price": 249, "is_vegetarian": True, "restaurant_id": restaurants[0].id, "category_id": categories[0].id},
                {"name": "Biryani", "description": "Aromatic rice with spices and meat", "price": 349, "is_vegetarian": False, "restaurant_id": restaurants[0].id, "category_id": categories[6].id},
                {"name": "Dal Makhani", "description": "Creamy black lentils", "price": 199, "is_vegetarian": True, "restaurant_id": restaurants[0].id, "category_id": categories[0].id},
                
                # Chinese foods
                {"name": "Kung Pao Chicken", "description": "Spicy stir-fried chicken with peanuts", "price": 279, "is_vegetarian": False, "restaurant_id": restaurants[1].id, "category_id": categories[1].id},
                {"name": "Vegetable Fried Rice", "description": "Stir-fried rice with mixed vegetables", "price": 179, "is_vegetarian": True, "restaurant_id": restaurants[1].id, "category_id": categories[1].id},
                {"name": "Spring Rolls", "description": "Crispy vegetable rolls", "price": 149, "is_vegetarian": True, "restaurant_id": restaurants[1].id, "category_id": categories[1].id},
                {"name": "Manchurian", "description": "Indo-Chinese vegetable balls", "price": 199, "is_vegetarian": True, "restaurant_id": restaurants[1].id, "category_id": categories[1].id},
                
                # Italian foods
                {"name": "Margherita Pizza", "description": "Classic pizza with tomato and mozzarella", "price": 399, "is_vegetarian": True, "restaurant_id": restaurants[2].id, "category_id": categories[5].id},
                {"name": "Pasta Carbonara", "description": "Creamy pasta with bacon", "price": 349, "is_vegetarian": False, "restaurant_id": restaurants[2].id, "category_id": categories[2].id},
                {"name": "Lasagna", "description": "Layered pasta with meat sauce", "price": 379, "is_vegetarian": False, "restaurant_id": restaurants[2].id, "category_id": categories[2].id},
                {"name": "Bruschetta", "description": "Grilled bread with tomatoes", "price": 149, "is_vegetarian": True, "restaurant_id": restaurants[2].id, "category_id": categories[2].id},
                
                # Mexican foods
                {"name": "Tacos", "description": "Crispy tacos with meat and vegetables", "price": 199, "is_vegetarian": False, "restaurant_id": restaurants[3].id, "category_id": categories[3].id},
                {"name": "Burrito Bowl", "description": "Rice bowl with beans and meat", "price": 249, "is_vegetarian": False, "restaurant_id": restaurants[3].id, "category_id": categories[3].id},
                {"name": "Nachos", "description": "Crispy tortilla chips with cheese", "price": 179, "is_vegetarian": True, "restaurant_id": restaurants[3].id, "category_id": categories[3].id},
                {"name": "Quesadilla", "description": "Cheese-filled tortilla", "price": 189, "is_vegetarian": True, "restaurant_id": restaurants[3].id, "category_id": categories[3].id},
                
                # Burgers
                {"name": "Classic Burger", "description": "Beef patty with lettuce and tomato", "price": 149, "is_vegetarian": False, "restaurant_id": restaurants[4].id, "category_id": categories[4].id},
                {"name": "Cheese Burger", "description": "Beef patty with extra cheese", "price": 179, "is_vegetarian": False, "restaurant_id": restaurants[4].id, "category_id": categories[4].id},
                {"name": "Veggie Burger", "description": "Plant-based patty with vegetables", "price": 159, "is_vegetarian": True, "restaurant_id": restaurants[4].id, "category_id": categories[4].id},
                {"name": "Chicken Burger", "description": "Crispy chicken fillet burger", "price": 169, "is_vegetarian": False, "restaurant_id": restaurants[4].id, "category_id": categories[4].id},
                
                # Pizza
                {"name": "Pepperoni Pizza", "description": "Pizza with pepperoni slices", "price": 449, "is_vegetarian": False, "restaurant_id": restaurants[5].id, "category_id": categories[5].id},
                {"name": "Veggie Supreme", "description": "Pizza loaded with vegetables", "price": 399, "is_vegetarian": True, "restaurant_id": restaurants[5].id, "category_id": categories[5].id},
                {"name": "BBQ Chicken Pizza", "description": "Pizza with BBQ chicken", "price": 479, "is_vegetarian": False, "restaurant_id": restaurants[5].id, "category_id": categories[5].id},
                {"name": "Hawaiian Pizza", "description": "Pizza with ham and pineapple", "price": 429, "is_vegetarian": False, "restaurant_id": restaurants[5].id, "category_id": categories[5].id},
                
                # Biryani
                {"name": "Chicken Biryani", "description": "Aromatic rice with chicken", "price": 299, "is_vegetarian": False, "restaurant_id": restaurants[6].id, "category_id": categories[6].id},
                {"name": "Mutton Biryani", "description": "Aromatic rice with mutton", "price": 349, "is_vegetarian": False, "restaurant_id": restaurants[6].id, "category_id": categories[6].id},
                {"name": "Veg Biryani", "description": "Aromatic rice with vegetables", "price": 249, "is_vegetarian": True, "restaurant_id": restaurants[6].id, "category_id": categories[6].id},
                {"name": "Egg Biryani", "description": "Aromatic rice with boiled eggs", "price": 229, "is_vegetarian": False, "restaurant_id": restaurants[6].id, "category_id": categories[6].id},
                
                # Desserts
                {"name": "Chocolate Cake", "description": "Rich chocolate layer cake", "price": 199, "is_vegetarian": True, "restaurant_id": restaurants[7].id, "category_id": categories[7].id},
                {"name": "Ice Cream Sundae", "description": "Ice cream with toppings", "price": 149, "is_vegetarian": True, "restaurant_id": restaurants[7].id, "category_id": categories[7].id},
                {"name": "Gulab Jamun", "description": "Sweet milk dumplings in syrup", "price": 99, "is_vegetarian": True, "restaurant_id": restaurants[7].id, "category_id": categories[7].id},
                {"name": "Brownie", "description": "Fudgy chocolate brownie", "price": 129, "is_vegetarian": True, "restaurant_id": restaurants[7].id, "category_id": categories[7].id},
            ])
        
        for food_data in foods_data:
            existing = db.query(Food).filter(
                Food.name == food_data["name"],
                Food.restaurant_id == food_data["restaurant_id"]
            ).first()
            if not existing:
                food = Food(**food_data)
                db.add(food)
                db.commit()
                print(f"Created food: {food.name}")
        
        # Create coupons
        coupons_data = [
            {
                "code": "FIRST50",
                "description": "50% off on first order",
                "discount_type": "percentage",
                "discount_value": 50,
                "min_order_amount": 200,
                "max_discount_amount": 100,
                "is_active": True
            },
            {
                "code": "SAVE100",
                "description": "₹100 off on orders above ₹300",
                "discount_type": "flat",
                "discount_value": 100,
                "min_order_amount": 300,
                "is_active": True
            },
            {
                "code": "WELCOME20",
                "description": "20% off for new users",
                "discount_type": "percentage",
                "discount_value": 20,
                "min_order_amount": 150,
                "max_discount_amount": 75,
                "is_active": True
            },
            {
                "code": "FREEDelivery",
                "description": "Free delivery on orders above ₹500",
                "discount_type": "flat",
                "discount_value": 40,
                "min_order_amount": 500,
                "is_active": True
            },
        ]
        
        for coupon_data in coupons_data:
            existing = db.query(Coupon).filter(Coupon.code == coupon_data["code"]).first()
            if not existing:
                coupon = Coupon(**coupon_data)
                db.add(coupon)
                db.commit()
                print(f"Created coupon: {coupon.code}")
        
        print("\n✅ Database seeded successfully!")
        print("\nAdmin credentials:")
        print("Email: admin@foodie.com")
        print("Password: admin123")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created")
    
    # Seed data
    seed_data()
