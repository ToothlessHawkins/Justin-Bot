from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from re import sub


def get_stuff(soup):
    blurb = []
    targ_tags = ['p', 'div']

    header = soup.find(id='firstHeading').string
    blurb.append(header)

    want = soup.find('div', class_='mw-parser-output').contents

    # get the <div> and <p> tags i need
    for i in want:
        try:
            cl = i['class']
        except (AttributeError, KeyError, TypeError) as _:
            cl = [""]

        # classes come back as list of classes
        # robust solution is checking if toc is in any classname in the list
        # but efficient solution is relying on the fact that toc is the only
        # class applied to the toc, which appears to be working
        if "toc" in cl[0]:
            break
        elif i.name in targ_tags:
            if i.get_text().endswith("may refer to:"):
                targ_tags = ['h2', 'ul', 'li']
            blurb.append(i.get_text())

    return blurb


def wiki_search(query):
    try:
        # I actually have no idea why queries with spaces in them still work
        with urlopen("https://en.wikipedia.org/wiki/{}".format(query)) as f:
            soup = BeautifulSoup(f, 'html.parser')
            return clean_text('\n'.join(get_stuff(soup)))
    except HTTPError:
        return "No results found."


# to remove citations i.e. [9] from text
# to remove [edit] links from text
def clean_text(text):
    citations = r"\[\d{,2}\]"
    edit_link = r"\[edit\]"

    new_text = sub(citations, '', text)
    nwr_text = sub(edit_link, '', new_text)
    return nwr_text


if __name__ == '__main__':
    while True:
        query = input("Your query: ")
        if query in ['quit', 'exit']:
            break
        print(wiki_search(query))
    print("Goodbye")
