import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

from models import Product, ProductAttributes
from config import Config

class DataProcessor:
    """Data processing utilities for e-commerce content generation"""
    
    def __init__(self):
        self.attribute_mappings = Config.SMARTPHONE_ATTRIBUTES
    
    def validate_product_data(self, product_data: Dict[str, Any]) -> bool:
        """Validate product data structure and required fields"""
        required_fields = ['product_id', 'name', 'category', 'attributes']
        
        # Check required fields
        for field in required_fields:
            if field not in product_data:
                print(f"Missing required field: {field}")
                return False
        
        # Validate attributes
        if not isinstance(product_data['attributes'], dict):
            print("Attributes must be a dictionary")
            return False
        
        # Check for at least one attribute
        if not product_data['attributes']:
            print("At least one attribute is required")
            return False
        
        return True
    
    def normalize_attributes(self, attributes: Dict[str, str]) -> Dict[str, str]:
        """Normalize attribute keys and values"""
        normalized = {}
        
        for key, value in attributes.items():
            # Normalize key (convert to snake_case for internal use)
            normalized_key = key.lower().replace(' ', '_').replace('-', '_')
            
            # Clean and normalize value
            normalized_value = self._clean_value(value)
            
            if normalized_value:
                normalized[normalized_key] = normalized_value
        
        return normalized
    
    def _clean_value(self, value: str) -> str:
        """Clean and normalize attribute values"""
        if not value:
            return ""
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', value.strip())
        
        # Handle common variations
        cleaned = cleaned.replace('"', 'inch')  # Handle quote marks
        cleaned = cleaned.replace('"', 'inch')
        
        return cleaned
    
    def extract_attributes_from_text(self, text: str) -> Dict[str, str]:
        """Extract product attributes from unstructured text"""
        attributes = {}
        
        # Common patterns for smartphone attributes
        patterns = {
            'screen_size': r'(\d+(?:\.\d+)?)\s*(?:inch|")',
            'battery': r'(\d+)\s*mAh',
            'camera': r'(\d+)\s*MP',
            'ram': r'(\d+)\s*GB\s*RAM',
            'storage': r'(\d+)\s*GB\s*(?:storage|ROM)',
            'processor': r'(Snapdragon|A\d+|Helio|Exynos|Kirin)\s+\d+',
            'operating_system': r'(Android|iOS)\s+\d+',
            'connectivity': r'(5G|4G|Wi-Fi\s*\d*[E]?)',
            'charging': r'(\d+)\s*W\s*(?:fast\s*)?charging'
        }
        
        for attr_name, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                attributes[attr_name] = matches[0]
        
        return attributes
    
    def create_product_from_dict(self, product_data: Dict[str, Any]) -> Optional[Product]:
        """Create a Product object from dictionary data"""
        try:
            # Validate data
            if not self.validate_product_data(product_data):
                return None
            
            # Normalize attributes
            normalized_attrs = self.normalize_attributes(product_data['attributes'])
            
            # Create ProductAttributes object
            attributes = ProductAttributes(**normalized_attrs)
            
            # Create Product object
            product = Product(
                product_id=product_data['product_id'],
                name=product_data['name'],
                category=product_data['category'],
                attributes=attributes,
                manufacturer=product_data.get('manufacturer'),
                brief=product_data.get('brief')
            )
            
            return product
            
        except Exception as e:
            print(f"Error creating product: {str(e)}")
            return None
    
    def load_products_from_json(self, file_path: str) -> List[Product]:
        """Load products from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            products = []
            if isinstance(data, list):
                for item in data:
                    product = self.create_product_from_dict(item)
                    if product:
                        products.append(product)
            elif isinstance(data, dict):
                product = self.create_product_from_dict(data)
                if product:
                    products.append(product)
            
            return products
            
        except Exception as e:
            print(f"Error loading products from {file_path}: {str(e)}")
            return []
    
    def save_products_to_json(self, products: List[Product], file_path: str) -> bool:
        """Save products to JSON file"""
        try:
            data = []
            for product in products:
                product_dict = {
                    'product_id': product.product_id,
                    'name': product.name,
                    'category': product.category,
                    'attributes': product.get_attributes_dict(),
                    'manufacturer': product.manufacturer,
                    'brief': product.brief
                }
                data.append(product_dict)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving products to {file_path}: {str(e)}")
            return False
    
    def create_sample_products(self) -> List[Product]:
        """Create sample smartphone products for testing"""
        sample_data = [
            {
                "product_id": "MPXU-256G",
                "name": "MegaPhone X Ultra",
                "category": "Smartphone",
                "attributes": {
                    "Screen Size": "6.7 inch",
                    "Battery": "5000mAh",
                    "Camera": "50MP",
                    "RAM": "12GB",
                    "Storage": "256GB",
                    "Processor": "Snapdragon 8 Gen 2",
                    "Operating System": "Android 13",
                    "Connectivity": "5G, Wi-Fi 6E",
                    "Security": "Face ID, Fingerprint",
                    "Charging": "65W Fast Charging"
                },
                "manufacturer": "TechX Inc.",
                "brief": "High-end phone with stunning camera and all-day battery."
            },
            {
                "product_id": "IPHONE-15-PRO",
                "name": "iPhone 15 Pro",
                "category": "Smartphone",
                "attributes": {
                    "Screen Size": "6.1 inch",
                    "Battery": "3200mAh",
                    "Camera": "48MP",
                    "RAM": "8GB",
                    "Storage": "128GB",
                    "Processor": "A17 Pro",
                    "Operating System": "iOS 17",
                    "Connectivity": "5G, Wi-Fi 6E",
                    "Security": "Face ID",
                    "Charging": "20W Fast Charging"
                },
                "manufacturer": "Apple Inc.",
                "brief": "Premium iPhone with titanium design and advanced camera system."
            },
            {
                "product_id": "SAMSUNG-S24-ULTRA",
                "name": "Samsung Galaxy S24 Ultra",
                "category": "Smartphone",
                "attributes": {
                    "Screen Size": "6.8 inch",
                    "Battery": "5000mAh",
                    "Camera": "200MP",
                    "RAM": "12GB",
                    "Storage": "512GB",
                    "Processor": "Snapdragon 8 Gen 3",
                    "Operating System": "Android 14",
                    "Connectivity": "5G, Wi-Fi 7",
                    "Security": "Ultrasonic Fingerprint",
                    "Charging": "45W Fast Charging"
                },
                "manufacturer": "Samsung Electronics",
                "brief": "Ultimate Android flagship with S Pen and AI features."
            }
        ]
        
        products = []
        for data in sample_data:
            product = self.create_product_from_dict(data)
            if product:
                products.append(product)
        
        return products
    
    def analyze_product_attributes(self, product: Product) -> Dict[str, Any]:
        """Analyze product attributes for content generation insights"""
        attributes = product.get_attributes_dict()
        
        analysis = {
            "total_attributes": len(attributes),
            "key_features": [],
            "missing_attributes": [],
            "attribute_categories": {
                "performance": [],
                "display": [],
                "camera": [],
                "battery": [],
                "connectivity": []
            }
        }
        
        # Categorize attributes
        for attr_name, attr_value in attributes.items():
            attr_lower = attr_name.lower()
            
            if any(word in attr_lower for word in ['ram', 'storage', 'processor']):
                analysis["attribute_categories"]["performance"].append(f"{attr_name}: {attr_value}")
            elif any(word in attr_lower for word in ['screen', 'display']):
                analysis["attribute_categories"]["display"].append(f"{attr_name}: {attr_value}")
            elif any(word in attr_lower for word in ['camera', 'mp']):
                analysis["attribute_categories"]["camera"].append(f"{attr_name}: {attr_value}")
            elif any(word in attr_lower for word in ['battery', 'mah']):
                analysis["attribute_categories"]["battery"].append(f"{attr_name}: {attr_value}")
            elif any(word in attr_lower for word in ['5g', 'wifi', 'connectivity']):
                analysis["attribute_categories"]["connectivity"].append(f"{attr_name}: {attr_value}")
        
        # Identify key features (attributes with high values)
        for attr_name, attr_value in attributes.items():
            if any(word in attr_value.lower() for word in ['ultra', 'pro', 'max', 'premium']):
                analysis["key_features"].append(f"{attr_name}: {attr_value}")
        
        return analysis

# Example usage
def example_data_processing():
    """Example of data processing functionality"""
    processor = DataProcessor()
    
    # Create sample products
    products = processor.create_sample_products()
    
    print(f"Created {len(products)} sample products:")
    for product in products:
        print(f"- {product.name} ({product.product_id})")
    
    # Save to JSON
    if processor.save_products_to_json(products, "sample_products.json"):
        print("\nSaved products to sample_products.json")
    
    # Load from JSON
    loaded_products = processor.load_products_from_json("sample_products.json")
    print(f"Loaded {len(loaded_products)} products from JSON")
    
    # Analyze attributes
    if loaded_products:
        analysis = processor.analyze_product_attributes(loaded_products[0])
        print(f"\nAttribute analysis for {loaded_products[0].name}:")
        print(f"Total attributes: {analysis['total_attributes']}")
        print(f"Key features: {analysis['key_features']}")

if __name__ == "__main__":
    example_data_processing() 