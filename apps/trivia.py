from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
from json import load
from html import unescape


def get_trivia_question(res):
    try:
        if res['response_code'] == 0:
            # get category
            category = res['results'][0]['category']
            question = res['results'][0]['question'].replace('&quot;', '"')
            answer = res['results'][0]['correct_answer']
            # list
            wrong = res['results'][0]['incorrect_answers']
            wrong.append(answer)
            options = sorted(wrong)

            return {'question': "Category: {}\nQuestion: {}\nOptions: {}".format(category, question, '; '.join(options)),
                    'answer': answer}
        else:
            return "Server Error, probably."
    except KeyError:
        return "Don't panic, but the API returned an invalid format. Verify JSON response."


def trivia_question(difficulty):
    try:
        with urlopen("https://opentdb.com/api.php?amount=1&{}".format(urlencode({'difficulty': difficulty}))) as f:
            return unescape(get_trivia_question(load(f)))
    except HTTPError:
        return "Server Error."
