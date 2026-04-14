from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=50, description='Category name')
    slug: str = Field(..., min_length=5, max_length=50, description='URL-friendly category name')


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str = Field(..., min_length=5, max_length=50, description='Updated category name')
    slug: str = Field(..., min_length=5, max_length=50, description='Display name of the category')


class CategoryResponse(CategoryBase):
    id: int = Field(..., description='Unique category identifier')

    class Config:
        from_attributes = True
