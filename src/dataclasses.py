"""
Classes to store data from QraphQL query responses
"""

from enum import Enum
from dataclasses import dataclass


class Sizes(Enum):
    XXS = 'XXS'
    XS = 'XS'
    S = 'S'
    M = 'M'
    L = 'L'
    XL = 'XL'
    XXL = 'XXL'


class CurrencyCodes(Enum):
    USD = 'USD'


class Url(str):
    pass


@dataclass
class PriceRange:
    min: float = None
    max: float = None

    def __post_init__(self):
        if self.min is None and self.max is None:
            raise ValueError('At least one value must be specified')
        elif self.min is None and self.max is not None:
            self.min = self.max
        elif self.max is None and self.min is not None:
            self.max = self.min


@dataclass
class ProductVariant:
    colorGroup: str
    colorId: int
    colorName: str
    inStore: bool
    size: Sizes
    sku: str
    skuStyleOrderId: int
    styleId01: str
    styleId02: int
    styleId: str
    type_name: str


@dataclass
class Swatch:
    primary_img: Url
    hover_img: Url
    url: Url
    color_id: int
    is_in_store: bool
    type_name: str


@dataclass
class Product:
    allAvailableSizes: list[Sizes]
    currencyCode: CurrencyCodes
    defaultSku: str
    displayName: str
    listPrice: PriceRange
    parentCategoryUnifiedId: str
    productOnSale: bool
    productSalePrice: PriceRange
    pdpUrl: Url
    productCoverage: str
    repositoryId: str
    productId: str
    inStore: bool
    unifiedId: str
    skuStyleOrder: list[ProductVariant]
    swatches: list[Swatch]
    type_name: str