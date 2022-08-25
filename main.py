import argparse
import dataclasses
import pandas as pd
import sys
from typing import Iterator
from typing import List

from src import models
from src import request_products
from src import send_email
from src import format_html

DEFAULT_SIZES = ['M']
DEFAULT_RST = ['Lined', '7"']

def parse_args(args: list[str]) -> models.SearchParameters:
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
    search_params = parser.parse_args(args, namespace=models.SearchParameters())
    if not search_params.sizes:
        search_params.sizes = DEFAULT_SIZES
    if not search_params.req_search_terms:
        search_params.req_search_terms = DEFAULT_RST
    return search_params


def _yield_ser_products(products: List[models.Product]) -> Iterator[dict]:
    for product in products:
        yield dataclasses.asdict(product)


def _make_email_body(search_params: models.SearchParameters,
                     products: List[models.Product]) -> str:
    body_lines = [repr(search_params),
                  '\n']
    return '\n'.join(body_lines)


def main():
    search_params = parse_args(sys.argv[1:])
    products = request_products.get_products(search_params)
    body = _make_email_body(search_params, products)
    html = format_html.make_products_html(products)
    send_email.send_email(body=body, html=html)
    print(f'{html}')


if __name__ == '__main__':
    main()