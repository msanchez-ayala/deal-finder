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
    __typename: str


@dataclass
class Swatch:
    primaryImage: Url
    hoverImage: Url
    url: Url
    colorId: int
    inStore: bool
    __typename: str


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
    __typename: str