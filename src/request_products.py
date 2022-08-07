import argparse
import requests
import string
import time
from typing import Optional

from src import dataclasses
from src import filter_products
from src import parse_product


HOME_ENDPOINT = 'https://shop.lululemon.com'
GQL_ENDPOINT = f"{HOME_ENDPOINT}/snb/graphql"

# Empirically determined maximum results per page without breaking the request
MAX_PAGE_SIZE = 20

# idk how to format this better without breaking the request
payload_template = string.Template("""
{"query":"query getCategoryDetails($$category: String!, $$cid: String, $$forceMemberCheck: Boolean, $$nValue: String!, $$sl: String!, $$locale: String!, $$Ns: String, $$storeId: String, $$pageSize: Int, $$page: Int, $$onlyStore: Boolean) {categoryDetails(\\n    category: $$category\\n    nValue: $$nValue\\n    locale: $$locale\\n    sl: $$sl\\n    Ns: $$Ns\\n    page: $$page\\n    pageSize: $$pageSize\\n    storeId: $$storeId\\n    onlyStore: $$onlyStore\\n    forceMemberCheck: $$forceMemberCheck\\n    cid: $$cid\\n  ) {\\n    activeCategory\\n    categoryLabel\\n    fusionExperimentId\\n    fusionExperimentVariant\\n    fusionQueryId\\n    h1Title\\n    isBopisEnabled\\n    isFusionQuery\\n    isWMTM\\n    name\\n    results: totalProducts\\n    totalProductPages\\n    currentPage\\n    type\\n    bopisProducts {\\n      allAvailableSizes\\n      currencyCode\\n      defaultSku\\n      displayName\\n      listPrice\\n      parentCategoryUnifiedId\\n      productOnSale: onSale\\n      productSalePrice: salePrice\\n      pdpUrl\\n      productCoverage\\n      repositoryId: productId\\n      productId\\n      inStore\\n      unifiedId\\n      skuStyleOrder {\\n        colorGroup\\n        colorId\\n        colorName\\n        inStore\\n        size\\n        sku\\n        skuStyleOrderId\\n        styleId01\\n        styleId02\\n        styleId\\n        __typename\\n      }\\n      swatches {\\n        primaryImage\\n        hoverImage\\n        url\\n        colorId\\n        inStore\\n        __typename\\n      }\\n      __typename\\n    }\\n    storeInfo {\\n      totalInStoreProducts\\n      totalInStoreProductPages\\n      storeId\\n      __typename\\n    }\\n    products {\\n      allAvailableSizes\\n      currencyCode\\n      defaultSku\\n      displayName\\n      listPrice\\n      parentCategoryUnifiedId\\n      productOnSale: onSale\\n      productSalePrice: salePrice\\n      pdpUrl\\n      productCoverage\\n      repositoryId: productId\\n      productId\\n      inStore\\n      unifiedId\\n      skuStyleOrder {\\n        colorGroup\\n        colorId\\n        colorName\\n        inStore\\n        size\\n        sku\\n        skuStyleOrderId\\n        styleId01\\n        styleId02\\n        styleId\\n        __typename\\n      }\\n      swatches {\\n        primaryImage\\n        hoverImage\\n        url\\n        colorId\\n        inStore\\n        __typename\\n      }\\n      __typename\\n    }\\n    seoLinks {\\n      next\\n      prev\\n      self\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n","variables":{"nValue":"${QUERY_TYPE}","category":"sale","locale":"en_US","sl":"US","page":${PAGE_NUM},"pageSize":${PAGE_SIZE},"forceMemberCheck":false},"operationName":"getCategoryDetails"}
""")


def get_products(sizes: list[str],
                 req_search_terms: list[str],
                 opt_search_terms: list[str]
                 ) -> Optional[list[dataclasses.Product]]:
    matching_products = []
    page_num = 1
    more_to_search = True
    while more_to_search:
        payload = payload_template.substitute(
            QUERY_TYPE=dataclasses.QueryTypes.MENS_SALE_SHORTS,
            PAGE_NUM=page_num,
            PAGE_SIZE=MAX_PAGE_SIZE)
        products = _get_products(payload)
        if not products:
            more_to_search = False
            break
        matching_products.extend(
            filter_products.get_matching_products(
                products, sizes, req_search_terms, opt_search_terms))
        print(f'Success: {page_num=}')
        page_num += 1
        time.sleep(0.2)
    return matching_products


def _get_products(payload: dict) -> Optional[list[dataclasses.Product]]:
    headers = get_headers()
    response = requests.request(
        "POST", GQL_ENDPOINT, data=payload, headers=headers)
    if response.status_code != requests.codes.ok:
        print(f'ERROR {response.status_code}: {response.reason}')
        print(f'{response.request.data}')
        return None
    products = response.json()['data']['categoryDetails']['products']
    if not products:
        return None
    return [parse_product.make_product(product) for product in products]


def get_cookie(session: requests.Session) -> str:
    response = session.get(HOME_ENDPOINT)
    if not response.ok:
        print(f'ERROR: Cannot establish connection with {HOME_ENDPOINT}')
    cookie_dict = session.cookies.get_dict()
    cookie_kv_pairs = [f'{key}={value}' for key, value in cookie_dict.items()]
    cookie_str = ';'.join(cookie_kv_pairs)
    return cookie_str


def get_headers() -> dict[str]:
    session = requests.Session()
    cookie = get_cookie(session)
    return {
        "Content-Type": "application/json",
        "Origin": HOME_ENDPOINT,
        "Accept-Language": "en-us",
        "cookie": cookie
    }