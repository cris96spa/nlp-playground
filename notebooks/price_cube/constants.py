from notebooks.price_cube.enums import Category, Column

CATEGORIES = {
    Category.ELECTRONICS.value: (50.0, 500.0),
    Category.APPAREL.value: (10.0, 100.0),
    Category.HOME_KITCHEN.value: (20.0, 200.0),
    Category.SPORTS_OUTDOORS.value: (15.0, 150.0),
    Category.BEAUTY_HEALTH.value: (5.0, 80.0),
}

SEED = 42
N_ROWS = 10000

ELASTICITY = {
    Category.ELECTRONICS.value: -2.0,
    Category.APPAREL.value: -1.5,
    Category.HOME_KITCHEN.value: -1.5,
    Category.SPORTS_OUTDOORS.value: -1.3,
    Category.BEAUTY_HEALTH.value: -0.8,
}

PRODUCT_CATALOG = {
    Category.ELECTRONICS.value: [
        (
            "ELEC001",
            "Wireless Headphones",
            "Premium over-ear headphones with active noise cancellation, deep bass, and Bluetooth 5.0 for seamless wireless audio.",
        ),
        (
            "ELEC002",
            "Smartphone",
            "Cutting-edge smartphone featuring a 6.5-inch OLED display, ultra-fast processor, and 128GB of storage for all your apps and media.",
        ),
        (
            "ELEC003",
            "Smartwatch",
            "Stylish fitness smartwatch with built-in heart rate monitor, GPS tracking, sleep analysis, and water-resistant design.",
        ),
    ],
    Category.APPAREL.value: [
        (
            "APP001",
            "Denim Jeans",
            "Classic-fit denim jeans crafted from a stretchable cotton blend, offering comfort, durability, and timeless style.",
        ),
        (
            "APP002",
            "Winter Jacket",
            "Heavy-duty insulated winter jacket with fleece lining, windproof shell, and adjustable hood for superior cold protection.",
        ),
        (
            "APP003",
            "Running Shoes",
            "Ultra-lightweight running shoes with cushioned soles, breathable mesh upper, and shock-absorbing design for peak performance.",
        ),
    ],
    Category.HOME_KITCHEN.value: [
        (
            "HOME001",
            "Blender",
            "High-powered blender with stainless steel blades, multiple speed settings, and a durable glass jar for smoothies, soups, and more.",
        ),
        (
            "HOME002",
            "Air Fryer",
            "Digital air fryer with rapid hot air circulation, touchscreen controls, and 5L capacity for healthy, oil-free cooking.",
        ),
        (
            "HOME003",
            "Cookware Set",
            "Comprehensive 10-piece non-stick cookware set with ergonomic handles and even heat distribution, suitable for all stovetops.",
        ),
    ],
    Category.SPORTS_OUTDOORS.value: [
        (
            "SPORT001",
            "Yoga Mat",
            "Eco-friendly, high-density yoga mat with anti-slip surface, optimal cushioning, and a carry strap for easy transport.",
        ),
        (
            "SPORT002",
            "Dumbbell Set",
            "Versatile adjustable dumbbell set with ergonomic grips and multiple weight options for effective strength training at home.",
        ),
        (
            "SPORT003",
            "Camping Tent",
            "Compact waterproof 2-person tent with quick setup, breathable mesh panels, and durable weather-resistant materials.",
        ),
    ],
    Category.BEAUTY_HEALTH.value: [
        (
            "BEAU001",
            "Facial Cleanser",
            "Gentle daily foaming cleanser enriched with aloe vera and vitamin E, designed to remove impurities without drying the skin.",
        ),
        (
            "BEAU002",
            "Hair Dryer",
            "Professional-grade ionic hair dryer with multiple heat and speed settings, cool shot feature, and diffuser for salon-quality results.",
        ),
        (
            "BEAU003",
            "Electric Toothbrush",
            "Rechargeable electric toothbrush with smart timer, 3 brushing modes, and long-lasting battery for superior oral hygiene.",
        ),
    ],
}


PRODUCT_PRICE_RANGES = {
    "ELEC001": (80.0, 120.0),  # Wireless Headphones
    "ELEC002": (300.0, 450.0),  # Smartphone
    "ELEC003": (100.0, 180.0),  # Smartwatch
    "APP001": (20.0, 40.0),  # Denim Jeans
    "APP002": (50.0, 90.0),  # Winter Jacket
    "APP003": (30.0, 60.0),  # Running Shoes
    "HOME001": (40.0, 80.0),  # Blender
    "HOME002": (60.0, 120.0),  # Air Fryer
    "HOME003": (50.0, 100.0),  # Cookware Set
    "SPORT001": (20.0, 35.0),  # Yoga Mat
    "SPORT002": (40.0, 90.0),  # Dumbbell Set
    "SPORT003": (70.0, 130.0),  # Camping Tent
    "BEAU001": (8.0, 15.0),  # Facial Cleanser
    "BEAU002": (20.0, 40.0),  # Hair Dryer
    "BEAU003": (30.0, 60.0),  # Electric Toothbrush
}
