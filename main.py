import argparse
import sys
import time
from types import ModuleType

from src import send_email
from src import format_html
from src import iterate_vendors

EXCLUDED_DIRS = ['__pycache__']


def main():
    search_params = parse_args(sys.argv[1:])
    html = make_html_from_search(search_params)
    if search_params.local_only:
        with open('index.html', 'w') as file:
            file.write(html)
    else:
        send_email.send_email(body="", html=html)


def parse_args(args: list[str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'search_terms',
        nargs='+',
        help="Keyword search terms for all vendor sites."
    )
    parser.add_argument(
        '-min_discount',
        type=int,
        default=0,
        help='Minimum discount percentage that all products must have.'
    )
    parser.add_argument(
        '-local_only',
        action='store_true',
        help='If true, write out index.html in CWD instead of sending an email.'
    )
    search_params = parser.parse_args(args)

    if not search_params.search_terms:
        parser.error('Expected at least one search term, but got '
                     f'{search_params.search_terms}')

    min_discount = search_params.min_discount
    if min_discount < 0 or min_discount > 100:
        parser.error('ERROR: min_discount of {min_discount} is '
                     f'outside the acceptable range of [0, 100]')

    return search_params


def make_html_from_search(search_params: argparse.Namespace):
    vendor_htmls = []
    for vendor_mod in iterate_vendors.yield_vendor_modules():
        vendor_name = derive_vendor_name_from_module(vendor_mod)
        if vendor_name.lower() != 'lululemon':
            print(f'NOTE: skipping {vendor_name}')
            continue
        try:
            requester_mod = vendor_mod.requester
            Parser = vendor_mod.parser.ProductParser
        except AttributeError as err:
            print(f'ERROR: failed to import all {vendor_name} modules.', err)
            continue

        print(f'Starting to scrape {vendor_name}')
        requester = requester_mod.Requester(search_terms=search_params.search_terms)
        products = requester.get_all_products()
        if not products:
            break
        html = format_html.make_vendor_html(
            vendor_name, products, Parser, search_params.min_discount)
        vendor_htmls.append(html)
        print(f'Succeeded with {vendor_name}')

    html = format_html.make_aggregate_html(
        vendor_htmls, search_params.search_terms)
    return html


def derive_vendor_name_from_module(vendor_module: ModuleType) -> str:
    module_string = vendor_module.__name__
    names = module_string.split('.')
    vendor_name = names[-1]
    return vendor_name.title()


if __name__ == '__main__':
    main()