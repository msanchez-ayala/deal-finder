import argparse
import requests
import string
import sys
import time

url = "https://shop.lululemon.com/snb/graphql"

# Empirically determined maximum results per page without breaking the request
MAX_PAGE_SIZE = 9

# idk how to format this better without breaking the request
payload_template = string.Template("""
{"query":"query getCategoryDetails($$category: String!, $$cid: String, $$forceMemberCheck: Boolean, $$nValue: String!, $$sl: String!, $$locale: String!, $$Ns: String, $$storeId: String, $$pageSize: Int, $$page: Int, $$onlyStore: Boolean) {categoryDetails(\\n    category: $$category\\n    nValue: $$nValue\\n    locale: $$locale\\n    sl: $$sl\\n    Ns: $$Ns\\n    page: $$page\\n    pageSize: $$pageSize\\n    storeId: $$storeId\\n    onlyStore: $$onlyStore\\n    forceMemberCheck: $$forceMemberCheck\\n    cid: $$cid\\n  ) {\\n    activeCategory\\n    categoryLabel\\n    fusionExperimentId\\n    fusionExperimentVariant\\n    fusionQueryId\\n    h1Title\\n    isBopisEnabled\\n    isFusionQuery\\n    isWMTM\\n    name\\n    results: totalProducts\\n    totalProductPages\\n    currentPage\\n    type\\n    bopisProducts {\\n      allAvailableSizes\\n      currencyCode\\n      defaultSku\\n      displayName\\n      listPrice\\n      parentCategoryUnifiedId\\n      productOnSale: onSale\\n      productSalePrice: salePrice\\n      pdpUrl\\n      productCoverage\\n      repositoryId: productId\\n      productId\\n      inStore\\n      unifiedId\\n      skuStyleOrder {\\n        colorGroup\\n        colorId\\n        colorName\\n        inStore\\n        size\\n        sku\\n        skuStyleOrderId\\n        styleId01\\n        styleId02\\n        styleId\\n        __typename\\n      }\\n      swatches {\\n        primaryImage\\n        hoverImage\\n        url\\n        colorId\\n        inStore\\n        __typename\\n      }\\n      __typename\\n    }\\n    storeInfo {\\n      totalInStoreProducts\\n      totalInStoreProductPages\\n      storeId\\n      __typename\\n    }\\n    products {\\n      allAvailableSizes\\n      currencyCode\\n      defaultSku\\n      displayName\\n      listPrice\\n      parentCategoryUnifiedId\\n      productOnSale: onSale\\n      productSalePrice: salePrice\\n      pdpUrl\\n      productCoverage\\n      repositoryId: productId\\n      productId\\n      inStore\\n      unifiedId\\n      skuStyleOrder {\\n        colorGroup\\n        colorId\\n        colorName\\n        inStore\\n        size\\n        sku\\n        skuStyleOrderId\\n        styleId01\\n        styleId02\\n        styleId\\n        __typename\\n      }\\n      swatches {\\n        primaryImage\\n        hoverImage\\n        url\\n        colorId\\n        inStore\\n        __typename\\n      }\\n      __typename\\n    }\\n    seoLinks {\\n      next\\n      prev\\n      self\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n","variables":{"nValue":"N-1z0xcmkZ1z0xbb9Z8t6","category":"sale","locale":"en_US","sl":"US","page":${PAGE_NUM},"pageSize":${PAGE_SIZE},"forceMemberCheck":false},"operationName":"getCategoryDetails"}
""")

headers = {
    "cookie": "_abck=E331451B69F31CD97C2D9CF92195BCEF~-1~YAAQJDorFzYbQx6CAQAAArSVLQjDXS%2F7D%2FHpDtat9flgcR3NRHc0YVXZyp4EK0OLrEqXF1mk3p1kTlpzRjeU7xn2C2xb6KKEGY1ek0ECWF4WME1pPxmeB56fvH2wtLWUH3kNVX8pJGS3jkGKFV5JQKveS%2FwC%2F9xgH3LQ1bD9y%2BXIQ0tJ%2BolMGrjkNlwjSkpjMj76zqEMIPuN9O7dYqGQWeItxe4z1YFZZQTiasZ9suB1SReeVVZYsqx%2B4Lsvrr7y4gYyfo%2FV%2BGIYavLoU4da23w4mdgMHw85JiKOx0htIng9HjnNjOlak7u0vwsaPh308jaszPsEHo2vqsu9U6OpaTr18pl4iv%2FVZRTQiLjLt749%2BkJiA3isOYXDeoqPP31EXfmP~-1~-1~-1; bm_sv=777F8BDD6F02ADEDE8C5D62BC6412BAF~YAAQJDorFzcbQx6CAQAAArSVLRDhJuZIz7HKPxH8XcKNwgy4lYmTgbRHccRuO5x1QkbtebV%2BBUKhXS1uHDPe5sNn7Q0%2FdE9MokvWlEfOzYctW%2Fx3gMt31hDCY8%2BUwzdsgDCLfNFZ9JQTuwaQPHrD6IP%2FqYWBRvMgpr4nXqzB7UFF9JQ2Xb5%2F7cAbx9Yx1o4R8%2BKBTb1f6yo%2FuHCQqqvtf6emhxnVHu4Hm1%2Fn9aHoE95CSLG7FutVbhcbiHUZdpZa5gGW~1",
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Origin": "https://shop.lululemon.com",
    "Cookie": "_abck=E331451B69F31CD97C2D9CF92195BCEF~0~YAAQJDorF8kZQx6CAQAASHiVLQgziv7gU+qpM9H1pH4iFIB8ZSqFk25gXSwOhGTLBtFZPu+pcTckb+/3L7mIhydJlIHySCFjXf88jnkj3CmrOz01ld7f5XUXahwtc2fzN6kCb4oR9qtjDYSpiA6BFF2zAUdZYRXRbRcDCczU3gvDSyv5NFUic8045vtzctmsE0G05Ql0oxoNsGAgPS2+OSAlTvUNfbTCzsj06wp90eHwlmZQOWOM8C0rcejpj2dQCZZmbx0ckzX4aeOZOUp2Ahhpg9KC2xJg6OSqyn7bqINC/uADnsCIin1cFRqPTJxdjMdtrQB3O/fZfmp7vwrYhqy1ixGCQqQRTsr6Vz1PVqPtEElK8L/D+L3X7aYhuMJKhyU=~-1~-1~-1; bm_sv=777F8BDD6F02ADEDE8C5D62BC6412BAF~YAAQJDorF8oZQx6CAQAASHiVLRC68xqm5JgLMI8C/ZhYPDLtS+TUQuhPG2Iw1ARLGPzT0d5vwF0+qLnvpwvuy2s82oXUxBpENZ1YliKc8UJcpWotH5I7ZLy1V/NzW5jlbXYJWB/UdsHkpmIrpUvB2M++hlBB3WVR586vE5RlUJ09MnW3Q57L1GBexDSJP5PuKwe2TUgEeKC3EHLNhaiNQ/GevD6qSLlyFj3HQmy0IT0t5NpY47n6WnAF6z5dUCLslwdA~1; ak_bmsc=9E3BC115E9C6BD89C5037F45960FCEA4~000000000000000000000000000000~YAAQJDorF3oZQx6CAQAAymuVLRDrWoc4o7yrK5sPgPKosiabHE85WTUGF5fCu/DmwbwgLLrudNazOeR7rsnAjQZU4hdlsgdrTLDz2sGw8uooOS+fePu8YEDdfy/FXSUJ9STNWVSP7BvA6jKN/gaLBhqOt4mGqvDyzyOi8EMBRejbv5FEBCZmHlTCDmataM6y1JllaHGCYBeb/FzDasi2jTJIed2a5/BQBPQvY1pKyjqyBltfD8N4mzc/DzeGoZGj+h2trwfpOFGLBMweJYIt0Op8AT/l9+vw2IF6yON9X0wKFdPASqVprJN3bLoKVQWR1IWVdY3m1j1WU1KhDP7+zMslD9Xecj0GawHADDgx9HjlMetSWLBJtUBtmJxjSutpcAqe8IJ54/3nCbphuHylSl8mS8uRlc/vC3NbmNOY0OJ+dLktPUxQgMgauz+G0bDTQgN9keT3FQ1hpYLYX3uq+exrQr4g8s2NVQd408KQA/IOqmGvSKzMWb5EOlRH; _ga_CCD7VVYPZ7=GS1.1.1658622136.2.0.1658622136.60; QuantumMetricUserID=d3d6f9fa40dffbd9cd79a9fe98581572; _tt_enable_cookie=1; _ttp=a9c7eb9b-58f1-4225-a9b4-6a6a0437e841; _fbp=fb.1.1658614791308.421220616; kampyleSessionPageCounter=1; kampyleUserSession=1658618975465; kampyleUserSessionsCount=7; mdLogger=false; _uetsid=94293b500ad511ed9beabb362e2a2bb1; _uetvid=942983800ad511ed8a43c91396234239; _ga=GA1.2.463763061.1658614782; _gid=GA1.2.357360138.1658614784; UsrLocale=en_US; s_cc=true; s_ecid=MCMID%7C89132822367958837681045104342180869371; mbox=session#1658614774427_0e8572e7-6ff4-4dcc-8b3b-e9b8dbd1487a#|PC#1658614774427_0e8572e7-6ff4-4dcc-8b3b-e9b8dbd1487a.35_0#; mboxEdgeCluster=35; _evga_8f06={%22uuid%22:%226a42b318aebd2a2a%22}; s_sq=%5B%5BB%5D%5D; JSESSIONID=skMtTyGGsYxP1HYLGvGGKQLey9Cq2ofEf3v49XNWm9zEgtC0ddkR!1396224499; AMCVS_A92B3BC75245B1030A490D4D%40AdobeOrg=1; AMCV_A92B3BC75245B1030A490D4D%40AdobeOrg=-2121179033%7CMCIDTS%7C19197%7CMCMID%7C89132822367958837681045104342180869371%7CMCAAMLH-1659221073%7C7%7CMCAAMB-1659221073%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1658623473s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19204%7CvVersion%7C5.3.0; WLS_ROUTE=.152; ltmo=2; lll-ecom-correlation-id=E8B2C330-432A-8F9E-7741-67CF37232F12; akacd_RWASP-default-phased-release=3836069064~rv=22~id=e3bd4d924bf2b05dc418f325c5d04ab3; _sfid_cc29={%22anonymousId%22:%226a42b318aebd2a2a%22}; _sctr=1|1658548800000; _scid=e641322f-26cd-4ea9-b4f1-502fe070bbd1; __pdst=405075c8281e44318e48cb6bdc753868; kampyle_userid=875f-9b78-01b1-9c95-0911-60de-6a0a-02ea; _gcl_au=1.1.979997769.1658614783; sl=US; s_ecid=MCMID%7C89132822367958837681045104342180869371; Country=US; bm_sz=BE189AC2932B99B5C9D430C4E94EB6A3~YAAQdoPXFw/3oSuCAQAAHKYkLRA/iT41Rw+R6PO15QW5xjXQ/JXLn4m5cZnUEHZavCmA/icp2TUpA5pDjLQxrtkeBeDEz1uNv9OMHPg+CnsTTYbneDM70iAslPM0c/pBW2zrCZguEIQwAeKxUzM/AThBfG4dDDzCqo43xroxuY6Den18UAw73eNlayBrmChzfLU0qJwlSybxMlQZh5fw+kAE0E1L9sHgyTpUcRji/Im1n5J+R75YEiA2qzsb6RNJVbWBxTzUlE7jJzCR2jqcQ+WVcocnYrGtXjScgUJLNy6GCeB8O/Y=~3291186~4403248; userPrefLanguage=en_US; atgRecVisitorId=13C9lilmhMiuak5ganYuBlYqOc5i8oPJ1eGJKqTqd2gL8Vc77F5; ADRUM_BT1=R:86|i:1991465|e:77; ADRUM_BTa=R:86|g:b7981f8c-28c2-45d0-85fe-54106065891e|n:lululemon_dbcafd93-1a1d-4932-9039-d48f2b4739fa; a1ashgd=nx5oqk2lqxi00000nx5oqk2lqxi00000; omniID=14532621653648ilG",
    "Content-Length": "2602",
    "Accept-Language": "en-us",
    "Host": "shop.lululemon.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Referer": "https://shop.lululemon.com/c/sale/_/N-1z0xcmkZ1z0xbb9Z8t6",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

MIN_PAGE_NUM = 1
# arbitrarily chosen large page number - usually there aren't actually more
# than 5
MAX_PAGE_NUM = 50

DEFAULT_SIZE = 'M'
DEFAULT_SEARCH_TERMS = ('Lined', '7"')


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


def main():
    args = parse_args(sys.argv[1:])
    print('Requesting all pages')
    product_matches = []
    for page_num in range(MIN_PAGE_NUM, MAX_PAGE_NUM):
        payload = payload_template.substitute(PAGE_NUM=page_num, PAGE_SIZE=MAX_PAGE_SIZE)
        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code != requests.codes.ok:
            break
        products = response.json()['data']['categoryDetails']['products']
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
