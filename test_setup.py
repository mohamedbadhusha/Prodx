#!/usr/bin/env python3
"""
Test script to verify the E-commerce Content Generation AI setup
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from config import Config
        print("✅ config.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import config.py: {e}")
        return False
    
    try:
        from models import Product, ProductAttributes, ContentRequest, GeneratedContent
        print("✅ models.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import models.py: {e}")
        return False
    
    try:
        from data_processor import DataProcessor
        print("✅ data_processor.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import data_processor.py: {e}")
        return False
    
    try:
        from content_generator import ContentGenerator
        print("✅ content_generator.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import content_generator.py: {e}")
        return False
    
    return True

def test_data_processing():
    """Test data processing functionality"""
    print("\n🔧 Testing data processing...")
    
    try:
        from data_processor import DataProcessor
        from models import Product
        
        processor = DataProcessor()
        
        # Test sample product creation
        sample_data = {
            "product_id": "TEST-001",
            "name": "Test Phone",
            "category": "Smartphone",
            "attributes": {
                "Screen Size": "6.1 inch",
                "Battery": "3000mAh",
                "Camera": "12MP"
            }
        }
        
        product = processor.create_product_from_dict(sample_data)
        if product:
            print("✅ Sample product created successfully")
            print(f"   - Product ID: {product.product_id}")
            print(f"   - Name: {product.name}")
            print(f"   - Attributes: {len(product.get_attributes_dict())}")
        else:
            print("❌ Failed to create sample product")
            return False
        
        # Test attribute extraction
        sample_text = "6.7-inch display, 5000mAh battery, 50MP camera"
        attributes = processor.extract_attributes_from_text(sample_text)
        print(f"✅ Attribute extraction: {len(attributes)} attributes found")
        
        return True
        
    except Exception as e:
        print(f"❌ Data processing test failed: {e}")
        return False

def test_configuration():
    """Test configuration settings"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import Config
        
        print(f"✅ Configuration loaded:")
        print(f"   - Supported languages: {len(Config.SUPPORTED_LANGUAGES)}")
        print(f"   - Content types: {len(Config.CONTENT_TYPES)}")
        print(f"   - Tone options: {len(Config.TONE_OPTIONS)}")
        print(f"   - Smartphone attributes: {len(Config.SMARTPHONE_ATTRIBUTES)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_models():
    """Test Pydantic models"""
    print("\n📋 Testing data models...")
    
    try:
        from models import Product, ProductAttributes, ContentRequest
        
        # Test ProductAttributes
        attrs = ProductAttributes(
            screen_size="6.7 inch",
            battery="5000mAh",
            camera="50MP"
        )
        print("✅ ProductAttributes created successfully")
        
        # Test Product
        product = Product(
            product_id="TEST-002",
            name="Test Product",
            category="Smartphone",
            attributes=attrs
        )
        print("✅ Product created successfully")
        
        # Test ContentRequest
        request = ContentRequest(
            product=product,
            language="English",
            tone="friendly"
        )
        print("✅ ContentRequest created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False

def check_environment():
    """Check environment setup"""
    print("\n🌍 Checking environment...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("⚠️  Warning: Python 3.8+ recommended")
    
    # Check for .env file
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found - create one from env_example.txt")
    
    # Check for required files
    required_files = [
        'requirements.txt',
        'config.py',
        'models.py',
        'content_generator.py',
        'data_processor.py',
        'main.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 E-commerce Content Generation AI - Setup Test")
    print("=" * 60)
    
    tests = [
        ("Environment Check", check_environment),
        ("Import Test", test_imports),
        ("Configuration Test", test_configuration),
        ("Models Test", test_models),
        ("Data Processing Test", test_data_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n{'='*60}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n📋 Next steps:")
        print("1. Set your OpenAI API key in .env file")
        print("2. Run: python main.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 