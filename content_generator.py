import openai
import json
from typing import Dict, List, Optional
from datetime import datetime
import re

from config import Config
from models import Product, ContentRequest, GeneratedContent, ContentBatch

class ContentGenerator:
    """Main content generation engine for e-commerce products"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the content generator with OpenAI API key"""
        self.api_key = api_key or Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        openai.api_key = self.api_key
        self.model = Config.OPENAI_MODEL
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
    
    def _format_attributes(self, attributes: Dict[str, str]) -> str:
        """Format product attributes for prompt generation"""
        return '\n'.join([f"- {k}: {v}" for k, v in attributes.items()])
    
    def _build_prompt(self, product: Product, language: str, tone: str) -> str:
        """Build the prompt for content generation"""
        attributes_str = self._format_attributes(product.get_attributes_dict())
        
        return Config.PROMPT_TEMPLATE.format(
            category=product.category,
            product_name=product.name,
            attributes=attributes_str,
            tone=Config.TONE_OPTIONS.get(tone, tone),
            language=language
        )
    
    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parse the LLM response into structured content sections"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in response.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Check for section headers
            if line.upper().startswith(('DESCRIPTION:', 'SPECIFICATIONS:', 'KEY FEATURES:', 'WHAT\'S IN THE BOX:')):
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = line.split(':')[0].lower().replace(' ', '_')
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def _extract_metadata(self, content: str) -> Dict[str, str]:
        """Extract metadata from generated content"""
        word_count = len(content.split())
        return {
            "word_count": str(word_count),
            "generated_at": datetime.now().isoformat(),
            "model": self.model
        }
    
    def generate_content(self, request: ContentRequest) -> List[GeneratedContent]:
        """Generate content for a single product"""
        try:
            # Build the prompt
            prompt = self._build_prompt(request.product, request.language, request.tone)
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the response
            content_text = response.choices[0].message['content']
            parsed_sections = self._parse_response(content_text)
            
            # Create GeneratedContent objects
            generated_contents = []
            for content_type, content in parsed_sections.items():
                if content:  # Only include non-empty sections
                    metadata = self._extract_metadata(content)
                    metadata["tone"] = request.tone
                    
                    generated_content = GeneratedContent(
                        product_id=request.product.product_id,
                        content_type=content_type,
                        language=request.language,
                        content=content,
                        metadata=metadata
                    )
                    generated_contents.append(generated_content)
            
            return generated_contents
            
        except Exception as e:
            print(f"Error generating content for {request.product.product_id}: {str(e)}")
            return []
    
    def generate_batch_content(self, batch: ContentBatch) -> List[GeneratedContent]:
        """Generate content for multiple products"""
        all_contents = []
        
        for product in batch.products:
            request = ContentRequest(
                product=product,
                language=batch.language,
                tone=batch.tone
            )
            
            contents = self.generate_content(request)
            all_contents.extend(contents)
        
        return all_contents
    
    def extract_attributes(self, product: Dict) -> Dict[str, str]:
        """Extract and structure product attributes"""
        attributes = product.get('attributes', {})
        features = {
            "Performance": f"{attributes.get('RAM', 'N/A')} RAM, {attributes.get('Storage', 'N/A')} Storage",
            "Display": f"{attributes.get('Screen Size', 'N/A')} AMOLED display",
            "Battery": f"{attributes.get('Battery', 'N/A')} for all-day power",
            "Camera": f"{attributes.get('Camera', 'N/A')} ultra-clear photos"
        }
        
        # Add processor if available
        if attributes.get('Processor'):
            features["Performance"] += f", {attributes.get('Processor')} processor"
        
        # Add connectivity if available
        if attributes.get('Connectivity'):
            features["Connectivity"] = attributes.get('Connectivity')
        
        return features

# Example usage function
def example_usage():
    """Example of how to use the ContentGenerator"""
    
    # Create a sample product
    product_data = {
        "product_id": "MPXU-256G",
        "name": "MegaPhone X Ultra",
        "category": "Smartphone",
        "attributes": {
            "screen_size": "6.7 inch",
            "battery": "5000mAh",
            "camera": "50MP",
            "ram": "12GB",
            "storage": "256GB",
            "processor": "Snapdragon 8 Gen 2",
            "operating_system": "Android 13",
            "connectivity": "5G, Wi-Fi 6E",
            "security": "Face ID, Fingerprint",
            "charging": "65W Fast Charging"
        },
        "manufacturer": "TechX Inc.",
        "brief": "High-end phone with stunning camera and all-day battery."
    }
    
    # Create Product object
    product = Product(**product_data)
    
    # Create content request
    request = ContentRequest(
        product=product,
        language="English",
        tone="friendly"
    )
    
    # Initialize generator (you'll need to set OPENAI_API_KEY)
    try:
        generator = ContentGenerator()
        
        # Generate content
        contents = generator.generate_content(request)
        
        # Print results
        for content in contents:
            print(f"\n=== {content.content_type.upper()} ===")
            print(content.content)
            print(f"Word count: {content.metadata.get('word_count', 'N/A')}")
            
    except ValueError as e:
        print(f"Setup error: {e}")
        print("Please set your OPENAI_API_KEY environment variable")
    except Exception as e:
        print(f"Generation error: {e}")

if __name__ == "__main__":
    example_usage() 