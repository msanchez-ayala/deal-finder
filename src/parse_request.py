from src import dataclasses

Url = dataclasses.Url


def make_swatch(data: dict) -> dataclasses.Swatch:
    primary_img = Url(data['primaryImage'])
    hover_img = Url(data['hoverImage'])
    url = Url(data['url'])
    color_id = int(data['colorId'])
    is_in_store = data['inStore']
    return dataclasses.Swatch(
        primary_img=primary_img,
        hover_img=hover_img,
        url=url,
        color_id=color_id,
        is_in_store=is_in_store,
        type_name=data['__typename']
    )


def make_product_variant(data: dict) -> dataclasses.ProductVariant:
    color = dataclasses.Color(
        group=data['colorGroup'],
        id=int(data['colorId']),
        name=data['colorName']
    )
    size = dataclasses.Sizes(data['size'])
    sku_style_order_id = int(data['skuStyleOrderId'])
    return dataclasses.ProductVariant(
        color=color,
        is_in_store=False,
        size=size,
        sku=data['sku'],
        sku_style_order_id=sku_style_order_id,
        style_id_01=data['styleId01'],
        style_id_02=data['styleId02'],
        style_id=data['styleId'],
        type_name=data['__typename']
    )


def make_price_range(prices: list[str]) -> dataclasses.PriceRange:
    if not prices:
        raise ValueError("Expected at least one value for a price range.")
    num_prices = len(prices)
    prices = [float(price) for price in prices]
    if num_prices == 1:
        price = prices[0]
        return dataclasses.PriceRange(min=price, max=price)
    if num_prices > 2:
        raise ValueError(f"Expected at most 2 values, but got {num_prices}")
    min_price, max_price = min(prices), max(prices)
    return dataclasses.PriceRange(min=min_price, max=max_price)


def make_product(data: dict) -> dataclasses.Product:
    sizes = [dataclasses.Sizes(size) for size in data['allAvailableSizes']]
    currency_code = dataclasses.CurrencyCodes(data['currencyCode'])
    default_sku = data['defaultSku']
    list_price_range = make_price_range(data['listPrice'])
    sale_price_range = make_price_range(data['productSalePrice'])
    pdp_url = Url(data['pdpUrl'])
    variants = [make_product_variant(variant_data)
                for variant_data in data['skuStyleOrder']]
    swatches = [make_swatch(swatch_data)
                for swatch_data in data['swatches']]

    return dataclasses.Product(
        available_sizes=sizes,
        currency_code=currency_code,
        default_sku=data['defaultSku'],
        display_name=data['displayName'],
        list_price_range=list_price_range,
        parent_cat_unified_id=data['parentCategoryUnifiedId'],
        is_on_sale=data['productOnSale'],
        sale_price_range=sale_price_range,
        pdp_url=pdp_url,
        product_coverage=data['productCoverage'],
        repo_id=data['repositoryId'],
        proudct_id=data['productId'],
        is_in_store=data['inStore'],
        unified_id=data['unifiedId'],
        variants=variants,
        swatches=swatches,
        type_name=data['__typename']
    )