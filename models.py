from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class ProductAttributes(BaseModel):
    """Model for product technical attributes"""
    screen_size: Optional[str] = Field(None, description="Display size")
    battery: Optional[str] = Field(None, description="Battery capacity")
    camera: Optional[str] = Field(None, description="Camera specifications")
    ram: Optional[str] = Field(None, description="Memory specifications")
    storage: Optional[str] = Field(None, description="Storage capacity")
    processor: Optional[str] = Field(None, description="CPU specifications")
    operating_system: Optional[str] = Field(None, description="OS version")
    connectivity: Optional[str] = Field(None, description="Network capabilities")
    security: Optional[str] = Field(None, description="Security features")
    charging: Optional[str] = Field(None, description="Charging technology")
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary format for API calls"""
        return {k.replace('_', ' ').title(): v for k, v in self.dict().items() if v is not None}

class Product(BaseModel):
    """Model for product data"""
    product_id: str = Field(..., description="Unique product identifier")
    name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    attributes: ProductAttributes = Field(..., description="Product technical attributes")
    manufacturer: Optional[str] = Field(None, description="Manufacturer name")
    brief: Optional[str] = Field(None, description="Brief product description")
    
    def get_attributes_dict(self) -> Dict[str, str]:
        """Get attributes as dictionary for prompt generation"""
        return self.attributes.to_dict()

class ContentRequest(BaseModel):
    """Model for content generation requests"""
    product: Product = Field(..., description="Product data")
    language: str = Field("English", description="Target language")
    tone: str = Field("friendly", description="Content tone/style")
    content_types: List[str] = Field(default_factory=lambda: ["product_description", "specifications", "features_benefits", "whats_in_box"])
    
    class Config:
        schema_extra = {
            "example": {
                "product": {
                    "product_id": "MPXU-256G",
                    "name": "MegaPhone X Ultra",
                    "category": "Smartphone",
                    "attributes": {
                        "screen_size": "6.7 inch",
                        "battery": "5000mAh",
                        "camera": "50MP",
                        "ram": "12GB",
                        "storage": "256GB"
                    }
                },
                "language": "English",
                "tone": "friendly"
            }
        }

class GeneratedContent(BaseModel):
    """Model for generated content response"""
    product_id: str
    content_type: str
    language: str
    content: str
    metadata: Dict[str, str] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "product_id": "MPXU-256G",
                "content_type": "product_description",
                "language": "English",
                "content": "Experience the future of mobile technology with the MegaPhone X Ultra...",
                "metadata": {
                    "word_count": "45",
                    "tone": "friendly",
                    "generated_at": "2024-01-15T10:30:00Z"
                }
            }
        }

class ContentBatch(BaseModel):
    """Model for batch content generation"""
    products: List[Product] = Field(..., description="List of products to generate content for")
    language: str = Field("English", description="Target language for all products")
    tone: str = Field("friendly", description="Content tone for all products")
    
    def __len__(self):
        return len(self.products) 