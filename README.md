# E-commerce Content Generation AI - Phase 1

A comprehensive AI-powered content generation system for e-commerce products, specifically designed for smartphone categories with extensible architecture for other product types.

## 🚀 Features

- **Smart Product Content Generation**: Generate compelling product descriptions, specifications, features, and "what's in the box" content
- **Multi-Language Support**: Generate content in English, French, German, Arabic (easily extensible)
- **Flexible Tone/Style**: Support for friendly, expert, persuasive, and casual tones
- **Structured Data Processing**: Robust product data validation and attribute extraction
- **Batch Processing**: Handle multiple products efficiently
- **SEO-Optimized**: Built-in keyword integration and SEO-friendly content generation

## 📁 Project Structure

```
prodx/
├── config.py              # Configuration and settings
├── models.py              # Pydantic data models
├── content_generator.py   # Main content generation engine
├── data_processor.py      # Data processing and validation
├── main.py               # Main entry point and demos
├── requirements.txt       # Python dependencies
├── env_example.txt       # Environment variables template
└── README.md            # This file
```

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root (copy from `env_example.txt`):

```bash
# Copy the example file
cp env_example.txt .env

# Edit the .env file and add your OpenAI API key
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### 3. Get OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Navigate to API Keys section
4. Create a new API key
5. Add it to your `.env` file

## 🎯 Quick Start

### Run the Demo

```bash
python main.py
```

This will run a comprehensive demo showing:
- Data processing capabilities
- Single product content generation
- Batch processing examples
- Attribute extraction from text

### Basic Usage

```python
from content_generator import ContentGenerator
from data_processor import DataProcessor
from models import Product, ContentRequest

# Initialize components
processor = DataProcessor()
generator = ContentGenerator()

# Create a product
product_data = {
    "product_id": "MPXU-256G",
    "name": "MegaPhone X Ultra",
    "category": "Smartphone",
    "attributes": {
        "Screen Size": "6.7 inch",
        "Battery": "5000mAh",
        "Camera": "50MP",
        "RAM": "12GB",
        "Storage": "256GB"
    }
}

# Create Product object
product = processor.create_product_from_dict(product_data)

# Generate content
request = ContentRequest(
    product=product,
    language="English",
    tone="friendly"
)

contents = generator.generate_content(request)

# Print results
for content in contents:
    print(f"{content.content_type}: {content.content}")
```

## 📊 Data Structure

### Product Data Format

```json
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
}
```

### Generated Content Output

The system generates four types of content:

1. **Product Description**: Compelling 80-word product overview
2. **Specifications**: Technical specifications in bullet points
3. **Key Features**: 3-4 key features with benefits
4. **What's in the Box**: Complete list of included items

## 🔧 Configuration

### Supported Languages
- English (default)
- French
- German
- Arabic

### Content Tones
- `friendly`: Conversational and approachable
- `expert`: Technical and authoritative
- `persuasive`: Sales-focused and compelling
- `casual`: Relaxed and informal

### Smartphone Attributes
The system recognizes and processes these smartphone attributes:
- Screen Size
- Battery Capacity
- Camera Specifications
- RAM & Storage
- Processor
- Operating System
- Connectivity
- Security Features
- Charging Technology

## 📈 Example Output

### Generated Content for MegaPhone X Ultra

**DESCRIPTION:**
Experience the future of mobile technology with the MegaPhone X Ultra. This premium smartphone combines cutting-edge performance with stunning visuals, featuring a 6.7-inch AMOLED display that brings your content to life. Powered by the latest Snapdragon 8 Gen 2 processor and 12GB RAM, every task feels effortless and smooth.

**SPECIFICATIONS:**
- Screen Size: 6.7 inch AMOLED display
- Battery: 5000mAh for all-day power
- Camera: 50MP ultra-clear photos
- RAM: 12GB for smooth performance
- Storage: 256GB internal storage
- Processor: Snapdragon 8 Gen 2
- Operating System: Android 13
- Connectivity: 5G, Wi-Fi 6E
- Security: Face ID, Fingerprint
- Charging: 65W Fast Charging

**KEY FEATURES:**
- 6.7-inch AMOLED Display: Immersive viewing experience with vibrant colors
- 50MP Camera System: Capture stunning photos with incredible detail
- 5000mAh Battery: All-day power for your busy lifestyle
- 65W Fast Charging: Quick power boost when you need it most

**WHAT'S IN THE BOX:**
- MegaPhone X Ultra smartphone
- USB-C charging cable
- 65W fast charger
- Protective case
- Screen protector
- User manual
- Warranty card

## 🔄 Extending the System

### Adding New Product Categories

1. Update `Config.SMARTPHONE_ATTRIBUTES` in `config.py`
2. Add new attribute patterns in `DataProcessor.extract_attributes_from_text()`
3. Modify prompt templates for category-specific content

### Adding New Languages

1. Add language to `Config.SUPPORTED_LANGUAGES`
2. Update prompt templates with language-specific instructions
3. Test with native speakers for accuracy

### Customizing Content Types

1. Modify `Config.CONTENT_TYPES`
2. Update prompt templates in `Config.PROMPT_TEMPLATE`
3. Adjust response parsing in `ContentGenerator._parse_response()`

## 🚀 Next Steps (Phase 2)

1. **Multi-Language Expansion**: Add more languages and localization
2. **Content Validation**: Implement quality checks and review workflows
3. **Image Integration**: Add visual content generation from product images
4. **SEO Optimization**: Advanced keyword integration and SEO analysis
5. **Performance Scaling**: Handle larger product catalogs efficiently
6. **Custom Models**: Fine-tune models for specific product categories

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues:
1. Check the documentation above
2. Review the example code in `main.py`
3. Open an issue on GitHub

---

**Built with ❤️ for e-commerce content generation** 