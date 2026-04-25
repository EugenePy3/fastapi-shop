from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .category import CategoryResponse


class ProductBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=200, description="Product name")
    description: Optional[str] = Field(None, description='Product description')
    price: float = Field(..., gt=0, description='Product price(must be greater than 0)')
    category_id: int = Field(..., description='Category ID')
    image_url: Optional[str] = Field(None, description='Product image url')


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=5, max_length=200, description='Update product name')
    description: Optional[str] = Field(None, description='Update product description')
    price: Optional[float] = Field(None, gt=0, description='Update product price(must be greater than 0)')
    category_id: Optional[int] = Field(None, gt=0, description='Update category ID')
    image_url: Optional[str] = Field(None, description='Update product image url')


class ProductResponse(BaseModel):
    id: int = Field(..., description='Unique product identifier')

    name: str
    slug: str
    description: Optional[str]
    price: float
    category_id: int
    image_url: Optional[str]

    created_at: datetime
    category: CategoryResponse = Field(..., description='Product category details')

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int = Field(..., description='Total number of products')
