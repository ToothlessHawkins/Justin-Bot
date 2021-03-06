from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib.parse import urlencode
from json import load


def mtg_search(query):
    if query.startswith('$'):
        price_dict = fuzzy_search_price(query[1:])
        return f"{price_dict['name']}\n{price_dict['set']}\n{price_dict['price']}"
    else:
        return fuzzy_search_card_name(query)


def handle_double_sided_cards(response):
    faces_images = []
    for face in response.get('card_faces', []):
        faces_images.append(face.get('image_uris', {}).get(
            'normal', 'Invalid response Format'))
    return "\n".join(faces_images)


def string_search(query):
    try:
        req = Request(
            "https://api.scryfall.com/cards/search?{}".format(urlencode({'q': query})))
        with urlopen(req) as f:
            res = load(f)
            names = []
            for card in res.get('data'):
                names.append(card.get('name'))
            if names:
                return "\n".join(names)
    except HTTPError as e:
        if getattr(e, 'code') == 404:
            res = load(e.file)
            if res.get('type', ''):
                return "{}: {}".format(res.get('type', 'Error').title(), res.get('details', 'Invalid response format from server'))
        return "Server Error: {}".format(e)


def fuzzy_search_card_name(query):
    try:
        req = Request(
            "https://api.scryfall.com/cards/named?{}".format(urlencode({'fuzzy': query})))
        with urlopen(req) as f:
            res = load(f)
            # handle flip cards
            if res.get('layout', '') == "transform":
                return handle_double_sided_cards(res)
            return res.get('image_uris', {}).get('normal', 'Invalid response format from server')
    except HTTPError as e:
        if getattr(e, 'code') == 404:
            res = load(e.file)
            if res.get('type', '') == 'ambiguous':
                return string_search(query)
            else:
                return "{}: {}".format(res.get('type', 'Error').title(), res.get('details', 'Invalid response format from server'))
        return "Server Error: {}".format(e)


def fuzzy_search_price(query):
    try:
        req = Request(
            "https://api.scryfall.com/cards/named?{}".format(urlencode({'fuzzy': query})))
        with urlopen(req) as f:
            res = load(f)
            return {
                "name": res.get("name", "Name not found!"),
                "set": res.get("set_name", "Set not found!"),
                "price": res.get("prices", {}).get("usd", "Price not found!")
            }
    except HTTPError as e:
        if getattr(e, 'code') == 404:
            res = load(e.file)
            if res.get('type', '') == 'ambiguous':
                return string_search(query)
            else:
                return "{}: {}".format(res.get('type', 'Error').title(), res.get('details', 'Invalid response format from server'))
        return "Server Error: {}".format(e)

# # helpful for debugging
# def fuzzy(query):
#     req = Request(
#         "https://api.scryfall.com/cards/named?{}".format(urlencode({'fuzzy': query})))
#     with urlopen(req) as f:
#         res = load(f)
#     return res
