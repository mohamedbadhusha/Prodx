import os
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the E-commerce Content Generation AI"""
    
    # API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Content Generation Settings
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Target Languages
    SUPPORTED_LANGUAGES = ["English", "French", "German", "Arabic"]
    DEFAULT_LANGUAGE = "English"
    
    # Content Types
    CONTENT_TYPES = [
        "product_description",
        "specifications", 
        "features_benefits",
        "whats_in_box"
    ]
    
    # Tone/Style Options
    TONE_OPTIONS = {
        "friendly": "Conversational and approachable",
        "expert": "Technical and authoritative", 
        "persuasive": "Sales-focused and compelling",
        "casual": "Relaxed and informal"
    }
    
    # Smartphone Category Attributes
    SMARTPHONE_ATTRIBUTES = {
        "Screen Size": "Display dimensions",
        "Battery": "Battery capacity and life",
        "Camera": "Camera specifications",
        "RAM": "Memory specifications",
        "Storage": "Internal storage capacity",
        "Processor": "CPU specifications",
        "Operating System": "OS version",
        "Connectivity": "Network capabilities",
        "Security": "Biometric features",
        "Charging": "Charging technology"
    }
    
    # SEO Keywords for Smartphones
    SEO_KEYWORDS = [
        "5G smartphone", "long battery life", "high-res camera",
        "fast charging", "large screen", "premium phone",
        "wireless charging", "water resistant", "face unlock"
    ]
    
    # Content Templates
    PROMPT_TEMPLATE = """You are an expert e-commerce copywriter specializing in {category} products.

Generate the following content for the {product_name} {category}:

1. Product Description (max 80 words)
2. Technical Specifications (bullet points)
3. Key Features and Benefits (3-4 points)
4. What's in the Box (complete list)

Product Attributes:
{attributes}

Brand Tone: {tone}
Language: {language}
Target Audience: Tech-savvy consumers looking for premium {category}

Please format your response as:
DESCRIPTION:
[Your compelling product description]

SPECIFICATIONS:
- [Spec 1]
- [Spec 2]
...

KEY FEATURES:
- [Feature 1]: [Benefit]
- [Feature 2]: [Benefit]
...

WHAT'S IN THE BOX:
- [Item 1]
- [Item 2]
...
"""

# Example product data structure
EXAMPLE_PRODUCT = {
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
} 