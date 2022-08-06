import pytest
from src import dataclasses
from src import parse_request

Url = dataclasses.Url


@pytest.fixture
def swatch_data():
    return {
        "primaryImage": "https://images.lululemon.com/is/image/lululemon/LM1219S_053870_1",
        "hoverImage": "https://images.lululemon.com/is/image/lululemon/LM1219S_053870_2",
        "url": "/p/mens-tanks/Metal-Vent-Breathe-Tank-MD/_/prod9370474?color=53870",
        "colorId": "53870",
        "inStore": False,
        "__typename": "ColorSwatch_CDP"
    }


def test_make_swatch(swatch_data):
    swatch = parse_request.make_swatch(swatch_data)
    assert swatch == dataclasses.Swatch(
        primary_img=Url(
            'https://images.lululemon.com/is/image/lululemon/LM1219S_053870_1'),
        hover_img=Url(
            'https://images.lululemon.com/is/image/lululemon/LM1219S_053870_2'),
        url=Url(
            '/p/mens-tanks/Metal-Vent-Breathe-Tank-MD/_/prod9370474?color=53870'),
        color_id=53870,
        is_in_store=False,
        type_name='ColorSwatch_CDP'
    )


