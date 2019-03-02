import discord
from discord.ext import commands
import apps
import os
import os.path
from re import findall

from testRunner import run_tests, silent_tests

from random import randint
# from discord import Emoji


DIRNAME = os.path.dirname(__file__)

BOT_PREFIX = ("!")

from config.constants import Tokens
TOKEN = Tokens.TOKEN
JUSTIN_ID = Tokens.JUSTIN_ID


bot = commands.Bot(command_prefix=BOT_PREFIX)

# list for event objects
eventlist = []


"""
TODO:
    add a execute batch file function
    input: !batch [filename]
    output: executes batch file on my computer
    only works when command author is my account
    -read/write batch file
    -can start mongod
    -can shutdown mongod
    -access mongod, etc, etc
"""


class MyClient(discord.Client):

    @bot.command()
    async def funk(self, context):
        await context.send("Success")

    @bot.event
    async def on_message(self, message):
        # we do not want the bot to reply to other bots, or itself
        # mildly redundant, but left it for explicitness
        if message.author.bot or message.author == self.user:
            return

        if message.content.startswith('!restart') and message.author.id == JUSTIN_ID:
            await self.send_message(message.channel, "User verified. Restarting...")
            os.startfile(os.path.join(DIRNAME, "batcave\\restart.bat"))

        if message.content.startswith('!report') and message.author.id == JUSTIN_ID:
            REPORT_DIR = os.path.join(DIRNAME, "reports")
            # count number of reports
            count = len([name for name in os.listdir(REPORT_DIR)
                         if os.path.isfile(os.path.join(REPORT_DIR, name))])
            # make file name report[number]
            report_name = 'report{}.txt'.format(count)
            # get abs path of file
            report_path = os.path.join(REPORT_DIR, report_name)
            with open(report_path, 'w', encoding='utf-8') as f:
                msg = message.author.name + '\n' + \
                    message.content.split(' ', 1)[1]
                f.write(msg)
            await self.send_message(message.channel, "User verified. Report created.")

        if message.content.startswith('!test') and message.author.id == JUSTIN_ID:
            await self.send_message(message.channel, "User verified. Running tests...")
            msg = '\n'.join(run_tests())
            await self.send_message(message.channel, msg)

        if message.content.startswith('!help'):
            msg = "Commands:\n\
                    !hello, \n\
                    !doubt, \n\
                    !itshotintopeka, \n\
                    !weather [city name in the us], \n\
                    !magic8ball, \n\
                    !roll [number of dice]d[number of sides]+[modifier], \n\
                    !trivia [default=easy; medium; hard], \n\
                    !spell [name of spell in Pathfinder]"
            await self.send_message(message.channel, msg)

        if message.content.startswith('!hello'):
            msg = 'Hello {0.author.mention}'.format(message)
            await self.send_message(message.channel, msg)

        if message.content.startswith('!thanks'):
            msg = "Kill me."
            await self.send_message(message.channel, msg)

        if message.content.startswith('!doubt'):
            msg = "https://i.imgur.com/47TsDcA.jpg"
            await self.send_message(message.channel, msg)

        if message.content.startswith('!openthepodbaydoors'):
            msg = "I'm sorry, {0.author.mention}. I'm afraid I can't do that.".format(
                message)
            await self.send_message(message.channel, msg)

        if message.content.startswith('!itshotintopeka'):
            await self.send_message(message.channel, apps.get_weather('Topeka'))

        if message.content.startswith('!weather'):
            city = message.content.split(' ', 1)[1]
            await self.send_message(message.channel, apps.get_weather(city))

        if message.content.startswith('!magic8ball'):
            msg = "{0.author.mention} ".format(message) + apps.magic_8_ball()
            await self.send_message(message.channel, msg)

        if message.content.startswith('!wiki'):
            # get all text after !wiki
            try:
                query = message.content.split(' ', 1)[1]
            except IndexError:
                await self.send_message(message.channel, "Enter a search query after the '!wiki' command.")
                raise
            res = apps.wiki_search(query)
            # cap message at 2000 characters to fit in discord char limit
            # append message to let user know what's going on
            msg = res[:1977] + \
                "\n`CHAR LIMIT REACHED`" if len(res) > 2000 else res
            await self.send_message(message.channel, msg)

        if message.content.startswith('!roll'):
            # get text after !roll
            rollval = message.content.split(' ', 1)[1]
            await self.send_message(message.channel, apps.dice_roller(rollval))

        if message.content.startswith('!btc'):
            await self.send_message(message.channel, apps.btc_value())

        if message.content.startswith('!rps'):
            throw = message.content.split()[1]
            msg = "{0.author.mention} threw {1}, I threw {2}".format(
                message, throw, apps.rock_paper_scissors(throw))
            await self.send_message(message.channel, msg)

        if message.content.endswith('!bro'):
            msg = 'Yeah, {}, '.format(apps.get_bro()) + \
                ' '.join(message.content.lower().split()[:-1])
            await self.send_message(message.channel, msg)

        if message.content.startswith('!event'):
            # args = message.content.split()[1:]
            # if not args:
            #     if not eventlist:
            #         eventlist.append(apps.Event())
            #         await self.send_message(message.channel, 'Name of this event?')
            #         titlemsg = await self.wait_for_message(author=message.author)
            #         eventlist[0].set_title(titlemsg.content)
            #         msg = "Event created"
            #     else:
            #         msg = eventlist
            # elif args[0] == 'list':
            #     msg = eventlist[0].get_details()
            # elif args[0] == 'loc':
            #     location = ' '.join(args[1:])
            #     eventlist[0].set_loc(location)
            #     msg = "Event location set to {}".format(location)
            # elif args[0] == 'time':
            #     time = ' '.join(args[1:])
            #     eventlist[0].set_time(time)
            #     msg = "Event time set to {}".format(time)
            # elif args[0] == 'rsvp':
            #     # consider : message.author.nick
            #     eventlist[0].add_attendee(message.author.nick)
            #     msg = "Thank you for RSVPing, {0.author.mention}".format(
            #         message)
            await self.send_message(message.channel, "This feature is under renovation")

        if message.content.startswith('!trivia'):
            if len(message.content.split()) > 1:
                diff = message.content.split()[1]
            else:
                diff = 'easy'
            # trivia is dict containing question and answer
            trivia = apps.trivia_question(diff)
            await self.send_message(message.channel, trivia['question'])
            guess = await self.wait_for_message(author=message.author)
            msg = "Correct!" if guess.content.lower(
            ) == trivia['answer'].lower() else "Incorrect!"
            await self.send_message(message.channel, msg)

        if message.content.startswith('!spell'):
            embed = apps.embed_spell(message.content.split(' ', 1)[1])
            await self.send_message(message.channel, embed=embed)

        if message.content.startswith('!poop'):
            await self.add_reaction(message, "\U0001F4A9")

        if message.content.startswith('!try'):
            await self.add_reaction(message, self.illuminati)

        """
        Passive stuff
        """
        # for every sent message roll for 1 in 10000 chance
        if randint(0, 9999) == 9999:
            await self.add_reaction(message, self.illuminati)

        cards = findall(r'(?<=\[\[)(.*?)(?=\]\])', message.content)
        if cards:
            for card in cards:
                await self.send_message(message.channel, apps.fuzzy_search_card_name(card))

    @bot.event
    async def on_ready(self):
        print('------------')
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------------')

        # load illuminati emoji
        self.illuminati = [
            emji for emji in bot.get_all_emojis() if emji.name == 'illuminati'][0]

        # announce when bot is online
        for server in self.servers:
            # Spin through every server
            for channel in server.channels:
                # Channels on the server
                if channel.name != 'general' and not channel.bitrate:
                    # don't talk on the main channel or voice channels
                    if channel.permissions_for(server.me).send_messages:
                        await self.send_message(channel, "Online. Running tests silently...")
                        msg = '\n'.join(silent_tests()) or "All tests passed."
                        await self.send_message(channel, msg)
                        # So that we don't send to every channel:
                        break


bot = MyClient(command_prefix=BOT_PREFIX)
bot.run(TOKEN)
