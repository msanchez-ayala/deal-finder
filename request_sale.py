import argparse
import requests
import string
import sys
import time
from typing import Optional

HOME_ENDPOINT = 'https://shop.lululemon.com'
GQL_ENDPOINT = f"{HOME_ENDPOINT}/snb/graphql"

# Empirically determined maximum results per page without breaking the request
MAX_PAGE_SIZE = 9

MIN_PAGE_NUM = 1
# arbitrarily chosen large page number - usually there aren't actually more
# than 5
MAX_PAGE_NUM = 50

DEFAULT_SIZE = 'M'
DEFAULT_SEARCH_TERMS = ('Lined', '7"')


# idk how to format this better without breaking the request
payload_template = string.Template("""
{"query":"query getCategoryDetails($$category: String!, $$cid: String, $$forceMemberCheck: Boolean, $$nValue: String!, $$sl: String!, $$locale: String!, $$Ns: String, $$storeId: String, $$pageSize: Int, $$page: Int, $$onlyStore: Boolean) {categoryDetails(\\n    category: $$category\\n    nValue: $$nValue\\n    locale: $$locale\\n    sl: $$sl\\n    Ns: $$Ns\\n    page: $$page\\n    pageSize: $$pageSize\\n    storeId: $$storeId\\n    onlyStore: $$onlyStore\\n    forceMemberCheck: $$forceMemberCheck\\n    cid: $$cid\\n  ) {\\n    activeCategory\\n    categoryLabel\\n    fusionExperimentId\\n    fusionExperimentVariant\\n    fusionQueryId\\n    h1Title\\n    isBopisEnabled\\n    isFusionQuery\\n    isWMTM\\n    name\\n    results: totalProducts\\n    totalProductPages\\n    currentPage\\n    type\\n    bopisProducts {\\n      allAvailableSizes\\n      currencyCode\\n      defaultSku\\n      displayName\\n      listPrice\\n      parentCategoryUnifiedId\\n      productOnSale: onSale\\n      productSalePrice: salePrice\\n      pdpUrl\\n      productCoverage\\n      repositoryId: productId\\n      productId\\n      inStore\\n      unifiedId\\n      skuStyleOrder {\\n        colorGroup\\n        colorId\\n        colorName\\n        inStore\\n        size\\n        sku\\n        skuStyleOrderId\\n        styleId01\\n        styleId02\\n        styleId\\n        __typename\\n      }\\n      swatches {\\n        primaryImage\\n        hoverImage\\n        url\\n        colorId\\n        inStore\\n        __typename\\n      }\\n      __typename\\n    }\\n    storeInfo {\\n      totalInStoreProducts\\n      totalInStoreProductPages\\n      storeId\\n      __typename\\n    }\\n    products {\\n      allAvailableSizes\\n      currencyCode\\n      defaultSku\\n      displayName\\n      listPrice\\n      parentCategoryUnifiedId\\n      productOnSale: onSale\\n      productSalePrice: salePrice\\n      pdpUrl\\n      productCoverage\\n      repositoryId: productId\\n      productId\\n      inStore\\n      unifiedId\\n      skuStyleOrder {\\n        colorGroup\\n        colorId\\n        colorName\\n        inStore\\n        size\\n        sku\\n        skuStyleOrderId\\n        styleId01\\n        styleId02\\n        styleId\\n        __typename\\n      }\\n      swatches {\\n        primaryImage\\n        hoverImage\\n        url\\n        colorId\\n        inStore\\n        __typename\\n      }\\n      __typename\\n    }\\n    seoLinks {\\n      next\\n      prev\\n      self\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n","variables":{"nValue":"N-1z0xcmkZ1z0xbb9Z8t6","category":"sale","locale":"en_US","sl":"US","page":${PAGE_NUM},"pageSize":${PAGE_SIZE},"forceMemberCheck":false},"operationName":"getCategoryDetails"}
""")


def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--size',
        dest='sizes',
        action='append',
        help="The available size that each matching item can have. Pass "
             "multiple sizes to filter by at least one of them e.g. --size "
             "M --size 32 to guarantee at least one of those sizes will be "
             "matched."
    )
    parser.add_argument(
        '--req_search_term',
        '--rst',
        dest='req_search_terms',
        action='append',
        help="Keyword search terms that must all be found in each match."
    )
    parser.add_argument(
        '--opt_search_term',
        '--ost',
        dest='opt_search_terms',
        action='append',
        help="Keyword search terms where at least one must be found in each "
             "match."
    )
    return parser.parse_args(args)


def has_matching_sizes(product: dict[str], query_sizes: list[str]) -> bool:
    available_sizes = product['allAvailableSizes']
    if not query_sizes:
        return DEFAULT_SIZE in available_sizes
    elif len(query_sizes) == 1:
        return query_sizes[0] in available_sizes
    else:
        # When there are multiple sizes we can't guarantee that multiple match
        # any given product, but at least one has to
        return any(size in available_sizes for size in query_sizes)


def has_all_search_terms(product: dict[str], search_terms: list[str]) -> bool:
    display_name = product['displayName'].lower()
    if not search_terms:
        search_terms = DEFAULT_SEARCH_TERMS
    return all(search_term.lower() in display_name for search_term in search_terms)


def has_at_least_one_search_term(product: dict[str],
                                 search_terms: list[str]) -> bool:
    display_name = product['displayName'].lower()
    if not search_terms:
        return True
    return any(
        search_term.lower() in display_name for search_term in search_terms)


def get_matching_products(products: list[dict],
                          sizes: list[str],
                          req_search_terms: list[str],
                          opt_search_terms: list[str]) -> list[dict]:
    product_matches = []
    for product in products:
        match_found = (has_matching_sizes(product, sizes) and
                       has_all_search_terms(product, req_search_terms) and
                       has_at_least_one_search_term(product, opt_search_terms))
        if match_found:
            product_matches.append(product)
    return product_matches


def get_products(response: requests.Response) -> Optional[list[dict]]:
    if response.status_code != requests.codes.ok:
        return None
    products = response.json()['data']['categoryDetails']['products']
    if not products:
        return None
    return products


def get_cookie(session: requests.Session) -> str:
    response = session.get(HOME_ENDPOINT)
    if not response.ok:
        print('CANNOT ESTABLISH SESSION')
    cookie_dict = session.cookies.get_dict()
    cookie_kv_pairs = [f'{key}={value}' for key, value in cookie_dict.items()]
    cookie_str = ';'.join(cookie_kv_pairs)
    return cookie_str


def get_headers_w_cookie(session: requests.Session) -> dict[str]:
    cookie = get_cookie(session)
    return {
        "Content-Type": "application/json",
        "Origin": HOME_ENDPOINT,
        "Accept-Language": "en-us",
        "cookie": cookie
    }


def main():
    args = parse_args(sys.argv[1:])
    print('Requesting all pages')
    session = requests.Session()
    headers = get_headers_w_cookie(session)

    product_matches = []
    for page_num in range(MIN_PAGE_NUM, MAX_PAGE_NUM):
        payload = payload_template.substitute(PAGE_NUM=page_num, PAGE_SIZE=MAX_PAGE_SIZE)
        response = requests.request("POST", GQL_ENDPOINT, data=payload, headers=headers)
        products = get_products(response)
        if not products:
            break
        product_matches.extend(
            get_matching_products(products,
                                  args.sizes,
                                  args.req_search_terms,
                                  args.opt_search_terms))
        print(f'Success: {page_num=}')
        time.sleep(0.1)

    print(f'Matches: {[product["displayName"] for product in product_matches]}')


if __name__ == '__main__':
    main()




