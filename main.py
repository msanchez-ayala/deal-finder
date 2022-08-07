import argparse
import sys

from src import request_products


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


def main():
    args = parse_args(sys.argv[1:])
    products = request_products.get_products(
        args.sizes,
        args.req_search_terms,
        args.opt_search_terms)
    print(f'Matches: {[product.display_name for product in products]}')


if __name__ == '__main__':
    main()