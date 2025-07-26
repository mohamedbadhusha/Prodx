#!/usr/bin/env python3
"""
E-commerce Content Generation AI - Phase 1
Main entry point for the content generation pipeline
"""

import os
import json
from typing import List

from config import Config
from models import Product, ContentRequest, GeneratedContent
from content_generator import ContentGenerator
from data_processor import DataProcessor

def setup_environment():
    """Setup environment and check API key"""
    if not Config.OPENAI_API_KEY:
        print("⚠️  OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key:")
        print("1. Create a .env file in the project root")
        print("2. Add: OPENAI_API_KEY=your_api_key_here")
        print("3. Or set the environment variable directly")
        return False
    return True

def demo_single_product():
    """Demonstrate content generation for a single product"""
    print("\n" + "="*60)
    print("📱 SINGLE PRODUCT CONTENT GENERATION DEMO")
    print("="*60)
    
    # Initialize components
    processor = DataProcessor()
    
    # Create sample product
    product_data = {
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
    
    # Create Product object
    product = processor.create_product_from_dict(product_data)
    if not product:
        print("❌ Failed to create product object")
        return
    
    print(f"✅ Created product: {product.name}")
    
    # Analyze product attributes
    analysis = processor.analyze_product_attributes(product)
    print(f"📊 Product analysis:")
    print(f"   - Total attributes: {analysis['total_attributes']}")
    print(f"   - Key features: {len(analysis['key_features'])}")
    
    # Create content request
    request = ContentRequest(
        product=product,
        language="English",
        tone="friendly"
    )
    
    # Generate content
    try:
        generator = ContentGenerator()
        contents = generator.generate_content(request)
        
        print(f"\n🎯 Generated {len(contents)} content sections:")
        
        for content in contents:
            print(f"\n📝 {content.content_type.upper()}:")
            print("-" * 40)
            print(content.content)
            print(f"📊 Word count: {content.metadata.get('word_count', 'N/A')}")
            
    except Exception as e:
        print(f"❌ Content generation failed: {str(e)}")

def demo_batch_processing():
    """Demonstrate batch content generation"""
    print("\n" + "="*60)
    print("📦 BATCH CONTENT GENERATION DEMO")
    print("="*60)
    
    # Initialize components
    processor = DataProcessor()
    generator = ContentGenerator()
    
    # Create sample products
    products = processor.create_sample_products()
    print(f"✅ Created {len(products)} sample products")
    
    # Save products to JSON
    processor.save_products_to_json(products, "sample_products.json")
    print("💾 Saved products to sample_products.json")
    
    # Generate content for first product only (to save API calls)
    if products:
        product = products[0]
        request = ContentRequest(
            product=product,
            language="English",
            tone="persuasive"
        )
        
        try:
            contents = generator.generate_content(request)
            print(f"\n🎯 Generated content for {product.name}:")
            
            for content in contents:
                print(f"\n📝 {content.content_type}:")
                print(f"   Word count: {content.metadata.get('word_count', 'N/A')}")
                
        except Exception as e:
            print(f"❌ Batch generation failed: {str(e)}")

def demo_data_processing():
    """Demonstrate data processing capabilities"""
    print("\n" + "="*60)
    print("🔧 DATA PROCESSING DEMO")
    print("="*60)
    
    processor = DataProcessor()
    
    # Test attribute extraction from text
    sample_text = """
    The new smartphone features a 6.7-inch AMOLED display, 
    5000mAh battery, 50MP camera, 12GB RAM, 256GB storage,
    Snapdragon 8 Gen 2 processor, Android 13, 5G connectivity,
    and 65W fast charging.
    """
    
    print("📝 Extracting attributes from text:")
    print(sample_text)
    
    attributes = processor.extract_attributes_from_text(sample_text)
    print(f"\n✅ Extracted attributes:")
    for key, value in attributes.items():
        print(f"   - {key}: {value}")
    
    # Test data validation
    print(f"\n🔍 Testing data validation:")
    valid_data = {
        "product_id": "TEST-001",
        "name": "Test Phone",
        "category": "Smartphone",
        "attributes": {"Screen Size": "6.1 inch"}
    }
    
    invalid_data = {
        "product_id": "TEST-002",
        "name": "Test Phone"
        # Missing category and attributes
    }
    
    print(f"   Valid data: {processor.validate_product_data(valid_data)}")
    print(f"   Invalid data: {processor.validate_product_data(invalid_data)}")

def save_generated_content(contents: List[GeneratedContent], filename: str = "generated_content.json"):
    """Save generated content to JSON file"""
    try:
        data = []
        for content in contents:
            content_dict = {
                "product_id": content.product_id,
                "content_type": content.content_type,
                "language": content.language,
                "content": content.content,
                "metadata": content.metadata
            }
            data.append(content_dict)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved generated content to {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to save content: {str(e)}")
        return False

def main():
    """Main function to run the e-commerce content generation demo"""
    print("🚀 E-commerce Content Generation AI - Phase 1")
    print("="*60)
    
    # Check environment setup
    if not setup_environment():
        print("\n📋 To get started:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set your OpenAI API key in .env file")
        print("3. Run: python main.py")
        return
    
    # Run demos
    demo_data_processing()
    demo_single_product()
    demo_batch_processing()
    
    print("\n" + "="*60)
    print("✅ Phase 1 Demo Complete!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Replace sample data with your actual product catalog")
    print("2. Add more languages (French, German, Arabic)")
    print("3. Implement content validation and review workflows")
    print("4. Add image processing for visual content generation")
    print("5. Scale to handle larger product catalogs")

if __name__ == "__main__":
    main() 