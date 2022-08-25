import argparse
import dataclasses
import pandas as pd
import sys
from typing import Iterator
from typing import List

from src import models
from src import request_products
from src import send_email


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
    return parser.parse_args(args, namespace=models.SearchParameters())


def _yield_ser_products(products: List[models.Product]) -> Iterator[dict]:
    for product in products:
        yield dataclasses.asdict(product)


def _make_email_body(search_params: models.SearchParameters,
                     products: List[models.Product]) -> str:
    num_products = len(products)
    body_lines = [repr(search_params),
                  '\n',
                  f'{num_products} found']
    return '\n'.join(body_lines)


def _make_email_html(products: List[models.Product]) -> str:
    records = _yield_ser_products(products)
    return pd.DataFrame.from_records(records).to_html()


def main():
    search_params = parse_args(sys.argv[1:])
    products = request_products.get_products(search_params)
    body = _make_email_body(search_params, products)
    html = _make_email_html(products)
    send_email.send_email(body=body, html=html)


if __name__ == '__main__':
    main()