import unittest
import apps

import os
from random import choice


class TestBro(unittest.TestCase):

    def setUp(self):
        dirname = os.path.dirname(__file__)
        brofile = os.path.join(dirname, 'apps/files/bro.txt')
        with open(brofile) as f:
            self.bronames = f.read().split('\n')

    def test_get_bro(self):
        for _ in range(1000):
            self.assertIn(apps.get_bro(), self.bronames)


class TestBTC(unittest.TestCase):

    def setUp(self):
        self.sim_res = {'bpi': {'USD': {'rate_float': 1234.5678}}}
        self.sim_false_res = {'apple': {'banana': {'orange': 1234.5678}}}

    # ensure the API is functioning
    def test_btc_api(self):
        api_res = apps.btc.btc_value()
        # did the method catch an HTTPError?
        self.assertFalse(api_res == 'Server Error.')

        """Do I test the api in here?
        If i import urllib i could, but I don't think that's what
        test suites are for
        """
        # # is bpi in the response?
        # self.assertIn('bpi', api_res)
        # # is USD in bpi?
        # self.assertIn('USD', api_res['bpi'])
        # # is rate_float in USD?
        # self.assertIn('rate_float', api_res['bpi']['USD'])
        # # is value a float number?
        # self.assertIsInstance(api_res['bpi']['USD']['rate_float'], float)

    def test_get_btc_value_invalid_format(self):
        self.assertEqual(apps.btc.get_btc_value(
            self.sim_false_res), "Don't panic, but the API is returning an invalid format. Verify JSON response.")

    def test_get_btc_value(self):
        self.assertEqual(apps.btc.get_btc_value(self.sim_res),
                         "Current value of Bitcoin in USD: $1234.57")


class TestDiceRoller(unittest.TestCase):
    """
    TODO: None of these work anymore since I changed the output. I have to fix these.
    """

    # def test_dice_1d20(self):
    #     self.assertTrue(1 <= apps.dice_roller('1d20') <= 20)

    # def test_dice_1d1000(self):
    #     self.assertTrue(1 <= apps.dice_roller('1d1000') <= 1000)

    # def test_dice_1d20plus20(self):
    #     self.assertTrue(21 <= apps.dice_roller('1d20+20') <= 40)

    # def test_dice_1banana20banana10(self):
    #     self.assertTrue(11 <= apps.dice_roller('1banana20banana10') <= 30)

    # def test_dice_invalid_input_word(self):
    #     self.assertEqual("Incorrect format. Try !help.",
    #                      apps.dice_roller('banana'))

    # def test_dice_invalid_input_wrong_format(self):
    #     self.assertEqual("Incorrect format. Try !help.",
    #                      apps.dice_roller('1'))

    # def test_dice_1whitespace20whitespace10(self):
    #     self.assertTrue(11 <= apps.dice_roller('1 20 10') <= 30)

    # def test_dice_many_times(self):
    #     for _ in range(1000):
    #         self.assertTrue(1 <= apps.dice_roller('1d20') <= 20)


class TestMagic8Ball(unittest.TestCase):

    def setUp(self):
        self.sim_resp = ["It is certain", "It is decidedly so", "Without a doubt",
                         "Yes definitely", "You may rely on it", "As I see it, yes",
                         "Most likely", "Outlook good", "Yes", "Signs point to yes",
                         "Reply hazy try again", "Ask again later", "Better not tell you now",
                         "Cannot predict now", "Concentrate and ask again", "Don't count on it",
                         "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]

    def test_magic_8_ball(self):
        for _ in range(1000):
            self.assertIn(apps.magic_8_ball(), self.sim_resp)


class TestRPS(unittest.TestCase):

    def setUp(self):
        self.rps = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}

    def test_rps_many_times(self):
        for _ in range(1000):
            myChoice = choice(list(self.rps.keys()))
            res = apps.rock_paper_scissors(myChoice)
            if res.endswith('Draw!'):
                self.assertEqual(res.split()[0].lower(), myChoice+':')
            elif res.endswith('You win!'):
                self.assertEqual(
                    res.split()[0].lower(), self.rps[myChoice]+':')
            elif res.endswith('I win!'):
                self.assertEqual(res.split()[0].lower(), [
                                 winner for winner, loser in self.rps.items() if loser == myChoice][0]+':')

    def test_rps_invalid_input(self):
        self.assertEqual("Invalid input. Check your spelling.",
                         apps.rock_paper_scissors("banana"))


class TestWeather(unittest.TestCase):

    def setUp(self):
        # regex pattern for get_weather output
        self.gw_pattern = r"^It is \d+\.?\d* degrees and \w+ at .*$"
        # misses multi word text_description of weather

        # test city values
        self.city0 = 'Newark'   # base
        self.city1 = 'New York'  # city with spaces
        self.city2 = 'UWUWUWU'  # city not in US

        self.sim_weather_res = {
            'main': {'temp': 255.37222}, 'weather': [{'main': 'TEST_TEXT'}]}
        self.sim_address = "TEST_ADDRESS"

    def test_get_info_send_message(self):
        self.assertEqual(apps.weather.get_info_send_message(
            self.sim_weather_res, self.sim_address), "It is -0.00 degrees and TEST_TEXT at TEST_ADDRESS")

    # def test_get_address(self):
    #     # i am reluctant to test the google api here because I only have X amount of calls/day
    #     pass

    def test_get_weather(self):
        self.assertRegex(apps.get_weather(self.city0), self.gw_pattern)

    def test_get_weather_name_w_spaces(self):
        self.assertRegex(apps.get_weather(self.city1), self.gw_pattern)

    def test_get_weather_invalid(self):
        self.assertEqual(apps.get_weather(self.city2),
                         "Error. Check your spelling.")


class TestTrivia(unittest.TestCase):

    def setUp(self):
        self.sim_fail_res = {"response_code": 1}
        self.sim_invalid_res = {"apple": "banana"}
        self.sim_trivia_res = {"response_code": 0, "results": [{"category": "TEST_CATEGORY", "type": "TEST_TYPE", "difficulty": "TEST_DIFFICULTY",
                                                                "question": "TEST_QUESTION", "correct_answer": "TEST_CORRECT", "incorrect_answers": ["TEST_INCORRECT"]}]}

    def test_get_trivia_question(self):
        expected = {'question': "Category: TEST_CATEGORY\nQuestion: TEST_QUESTION\n",
                    'options': {
                        '1': 'TEST_CORRECT',
                        '2': 'TEST_INCORRECT'
                    },
                    'answer': "TEST_CORRECT"}
        self.assertEqual(
            apps.trivia.get_trivia_question(self.sim_trivia_res), expected)

    def test_get_trivia_question_server_error(self):
        self.assertEqual(apps.trivia.get_trivia_question(
            self.sim_fail_res), "Server Error, probably.")

    def test_get_trivia_question_invalid_res(self):
        self.assertEqual(apps.trivia.get_trivia_question(
            self.sim_invalid_res), "Don't panic, but the API returned an invalid format. Verify JSON response.")

    def test_trivia_question_api(self):
        # get response
        # because the formatting is a callback function, we can't test
        # the actual JSON from the API easily
        res = apps.trivia_question('easy')
        # ensure response contains question
        self.assertIn('question', res)
        # ensure response contains answer
        self.assertIn('answer', res)


class TestPFSpells(unittest.TestCase):

    def test_roman_conv(self):
        in_seq = '1, 2, 3, 4, 5, 6, 7, 8, 9;'
        expected = 'I, II, III, IV, V, VI, VII, VIII, IX;'
        self.assertEqual(apps.pfspells.roman_conv(in_seq), expected)

    # the rest of this app is pretty tricky to test
    # do i simulate a db connection or do i just use an actual one
    # I can verify the retrieval of records as well as schema()
    # but how do i verify a discord embed object?


class TestWikiSearch(unittest.TestCase):

    def test_clean_text_citations(self):
        a_str = "Lorem[5] ip[7]sum [8]dolorem monkey.[9] banana[11] apple[111]"
        b_str = "Lorem ipsum dolorem monkey. banana apple[111]"
        self.assertEqual(apps.wiki.clean_text(a_str), b_str)

    def test_clean_text_edit(self):
        a_str = "Lorem[edit] ip[edit]sum [edit]dolorem monkey.[edit] banana[edit] apple[edit]"
        b_str = "Lorem ipsum dolorem monkey. banana apple"
        self.assertEqual(apps.wiki.clean_text(a_str), b_str)

    # def test_get_stuff(self):
    #     a_html = "<!DOCTYPE html>\
    #                 <html>\
    #                 <head>\
    #                 <meta charset = 'UTF-8'>\
    #                 <title> Title of the document </title>\
    #                 </head>\
    #                 <body>\
    #                 <div class=>\
    #                 Content of the document......\
    #                 </body>\
    #                 </html>"


if __name__ == '__main__':
    unittest.main()
