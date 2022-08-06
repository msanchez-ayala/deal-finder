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