from src import models


DEFAULT_SIZE = 'M'
DEFAULT_SEARCH_TERMS = ('Lined', '7"')


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


def has_matching_sizes(product: models.Product,
                       query_sizes: list[str]) -> bool:
    available_sizes = product.available_sizes
    if not query_sizes:
        return DEFAULT_SIZE in available_sizes
    elif len(query_sizes) == 1:
        return query_sizes[0] in available_sizes
    else:
        # When there are multiple sizes we can't guarantee that multiple match
        # any given product, but at least one has to
        return any(size in available_sizes for size in query_sizes)


def has_all_search_terms(product: models.Product, search_terms: list[str]) -> bool:
    display_name = product.display_name.lower()
    if not search_terms:
        search_terms = DEFAULT_SEARCH_TERMS
    return all(search_term.lower() in display_name for search_term in search_terms)


def has_at_least_one_search_term(product: models.Product,
                                 search_terms: list[str]) -> bool:
    display_name = product.display_name.lower()
    if not search_terms:
        return True
    return any(
        search_term.lower() in display_name for search_term in search_terms)