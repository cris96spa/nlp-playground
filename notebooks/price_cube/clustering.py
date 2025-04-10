import json

import matplotlib.pyplot as plt
import polars as pl
from scipy.cluster.hierarchy import dendrogram, linkage, to_tree
from sentence_transformers import SentenceTransformer

from notebooks.price_cube.constants import PRODUCTS_PATH
from notebooks.price_cube.enums import Column
from notebooks.price_cube.models import Product

# Define the products list, including product id, name, description, and category.
products = [
    {
        "sku": "ELEC001",
        "name": "Wireless Headphones",
        "description": "Premium over-ear headphones with active noise cancellation, deep bass, and Bluetooth 5.0 for seamless wireless audio.",
        "category": "ELECTRONICS",
    },
    {
        "sku": "ELEC002",
        "name": "Smartphone",
        "description": "Cutting-edge smartphone featuring a 6.5-inch OLED display, ultra-fast processor, and 128GB of storage for all your apps and media.",
        "category": "ELECTRONICS",
    },
    {
        "sku": "ELEC003",
        "name": "Smartwatch",
        "description": "Stylish fitness smartwatch with built-in heart rate monitor, GPS tracking, sleep analysis, and water-resistant design.",
        "category": "ELECTRONICS",
    },
    {
        "sku": "APP001",
        "name": "Denim Jeans",
        "description": "Classic-fit denim jeans crafted from a stretchable cotton blend, offering comfort, durability, and timeless style.",
        "category": "APPAREL",
    },
    {
        "sku": "APP002",
        "name": "Winter Jacket",
        "description": "Heavy-duty insulated winter jacket with fleece lining, windproof shell, and adjustable hood for superior cold protection.",
        "category": "APPAREL",
    },
    {
        "sku": "APP003",
        "name": "Running Shoes",
        "description": "Ultra-lightweight running shoes with cushioned soles, breathable mesh upper, and shock-absorbing design for peak performance.",
        "category": "APPAREL",
    },
    {
        "sku": "HOME001",
        "name": "Blender",
        "description": "High-powered blender with stainless steel blades, multiple speed settings, and a durable glass jar for smoothies, soups, and more.",
        "category": "HOME_KITCHEN",
    },
    {
        "sku": "HOME002",
        "name": "Air Fryer",
        "description": "Digital air fryer with rapid hot air circulation, touchscreen controls, and 5L capacity for healthy, oil-free cooking.",
        "category": "HOME_KITCHEN",
    },
    {
        "sku": "HOME003",
        "name": "Cookware Set",
        "description": "Comprehensive 10-piece non-stick cookware set with ergonomic handles and even heat distribution, suitable for all stovetops.",
        "category": "HOME_KITCHEN",
    },
    {
        "sku": "SPORT001",
        "name": "Yoga Mat",
        "description": "Eco-friendly, high-density yoga mat with anti-slip surface, optimal cushioning, and a carry strap for easy transport.",
        "category": "SPORTS_OUTDOORS",
    },
    {
        "sku": "SPORT002",
        "name": "Dumbbell Set",
        "description": "Versatile adjustable dumbbell set with ergonomic grips and multiple weight options for effective strength training at home.",
        "category": "SPORTS_OUTDOORS",
    },
    {
        "sku": "SPORT003",
        "name": "Camping Tent",
        "description": "Compact waterproof 2-person tent with quick setup, breathable mesh panels, and durable weather-resistant materials.",
        "category": "SPORTS_OUTDOORS",
    },
    {
        "sku": "BEAU001",
        "name": "Facial Cleanser",
        "description": "Gentle daily foaming cleanser enriched with aloe vera and vitamin E, designed to remove impurities without drying the skin.",
        "category": "BEAUTY_HEALTH",
    },
    {
        "sku": "BEAU002",
        "name": "Hair Dryer",
        "description": "Professional-grade ionic hair dryer with multiple heat and speed settings, cool shot feature, and diffuser for salon-quality results.",
        "category": "BEAUTY_HEALTH",
    },
    {
        "sku": "BEAU003",
        "name": "Electric Toothbrush",
        "description": "Rechargeable electric toothbrush with smart timer, 3 brushing modes, and long-lasting battery for superior oral hygiene.",
        "category": "BEAUTY_HEALTH",
    },
]

df = pl.read_csv(PRODUCTS_PATH).sort(Column.PRODUCT_NAME.value)
products = df.to_dicts()
products = [Product.model_validate(p) for p in products]
# Extract descriptions for embedding.
descriptions = [p.product_description for p in products]

# Load a pre-trained Hugging Face embedder using SentenceTransformer.
# Here we use 'all-MiniLM-L6-v2' - adjust to any model available on Hugging Face.
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(descriptions, convert_to_tensor=False)  # returns numpy arrays

# Perform hierarchical clustering using Ward's method.
Z = linkage(embeddings, method="ward")


# Recursive helper to build a nested JSON tree from the clustering result.
def build_tree(node, labels):
    if node.is_leaf():
        return {"name": labels[node.id]}
    else:
        return {
            "distance": node.dist,
            "children": [
                build_tree(node.get_left(), labels),
                build_tree(node.get_right(), labels),
            ],
        }


# Create labels using product IDs.
labels = [p.sku for p in products]
root, _ = to_tree(Z, rd=True)
json_tree = build_tree(root, labels)

# Convert the tree structure to a JSON formatted string.
json_str = json.dumps(json_tree, indent=2)
print(json_str)

plt.figure(figsize=(12, 8))
dendrogram(
    Z,
    labels=labels,
    leaf_rotation=90,  # Rotate the labels for better readability
    leaf_font_size=10,
)
plt.title("Hierarchical Clustering Dendrogram")
plt.xlabel("Product ID")
plt.ylabel("Distance")
plt.show()
