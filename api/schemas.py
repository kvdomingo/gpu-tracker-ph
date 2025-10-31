from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_count: int
    has_next_page: bool
    last_data_update: datetime


class PaginatedResponse[T](BaseModel):
    meta: PaginationMeta
    data: list[T]


class ProductVariant(BaseModel):
    id: str
    source_id: str
    product_id: str
    domain_tld: str
    title: str
    is_available: bool
    price: float
    weight: float
    retrieved_at: datetime


class Product(BaseModel):
    id: str
    source_id: str
    domain_tld: str
    title: str
    description: str
    product_url: AnyHttpUrl
    source_created_at: datetime
    source_updated_at: datetime
    retrieved_at: datetime
    brand: str
    image_url: AnyHttpUrl
    price_min: float
    price_max: float
    variants: list[ProductVariant]
