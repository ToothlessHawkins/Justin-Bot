from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib.parse import urlencode
from json import load


def fuzzy_search_card_name(query):
    try:
        req = Request(
            "https://api.scryfall.com/cards/named?{}".format(urlencode({'fuzzy': query})))
        with urlopen(req) as f:
            res = load(f)
            # handle flip cards
            if res.get('layout', '') == "transform":
                faces_images = []
                for face in res.get('card_faces', []):
                    faces_images.append(face.get('image_uris', {}).get(
                        'normal', 'Invalid response Format'))
                return "\n".join(faces_images)

            return res.get('image_uris', {}).get('normal', 'Invalid response Format')

    except HTTPError as e:
        if e.code == 404:
            res = load(e.file)
            return "{}: {}".format(res.get('type', 'Error').title(), res.get('details', 'Invalid response Format'))
        else:
            return "Server Error"
