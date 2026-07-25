from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


from .category import CategoryResponse
from .types import PositivePrice


class ProductBase(BaseModel):
    name: str = Field(min_length=5, max_length=200, description="Product name")

    description: str | None = Field(
        default=None,
        description='Product description'
    )

    price: PositivePrice = Field(description='Product price')
    category_id: int = Field(description='Category ID')
    image_url: str | None = Field(
        default=None,
        description='Product image url')


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=5,
        max_length=200,
        description='Update product name'
    )
    description: str | None = Field(
        default=None,
        description='Update product description'
    )
    price: PositivePrice | None = Field(
        default=None,
        description='Update product price'
    )
    category_id: int | None = Field(
        default=None,
        gt=0,
        description='Update category ID'
    )
    image_url: str | None = Field(
        default=None,
        description='Update product image url'
    )


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Unique product identifier')

    name: str = Field(description='Product name')
    slug: str = Field(description='Product slug')

    description: str | None = Field(
        default=None,
        description='Product description'
    )
    price: PositivePrice = Field(description='Product price')

    image_url: str | None = Field(
        default=None,
        description='Product image URL'
    )
    category_id: int = Field(description='Category ID')
    category: CategoryResponse = Field(
        description='Product category details'
    )
    created_at: datetime = Field(
        description='Product creation date'
    )


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int = Field(description='Total number of products')

