import importlib
import json
from pathlib import Path
from typing import Iterator
from types import ModuleType


EXCLUDED_DIRS = ['__pycache__']


def yield_vendor_dirs() -> Path:
    vendors_dir = Path('src/vendors/')
    for item in vendors_dir.iterdir():
        if not item.is_dir() or item.name in EXCLUDED_DIRS:
            continue
        yield item


def yield_vendor_modules() -> Iterator[ModuleType]:
    for vendor_dir in yield_vendor_dirs():
        mod_name = f'src.vendors.{vendor_dir.name}'
        try:
            vendor_mod = importlib.import_module(mod_name)
        except ModuleNotFoundError:
            print(f'ERROR: No vendor "{mod_name}" found')
            continue
        yield vendor_mod