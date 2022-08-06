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