import sqlite3
import os.path
from discord import Color, Embed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../db/spells.db")

with sqlite3.connect(db_path) as db:
    c = db.cursor()


def schema(results):
    if not results:
        return {'name': False}

    fields = [
        'name',
        'school',
        'subschool',
        'descriptor',
        'spell_level',
        'casting_time',
        'components',
        'range',
        'area',
        'targets',
        'duration',
        'saving_throw',
        'spell_resistance',
        'description',
        'linktext',
        'id']

    spell = {}
    index = 0
    for field in fields:
        spell.update({field: results[index]})
        index += 1
    return spell


def roman_conv(instr):
    roman_numerals = {'1': 'I', '2': 'II', '3': 'III', '4': 'IV',
                      '5': 'V', '6': 'VI', '7': 'VII', '8': 'VIII', '9': 'IX', }
    for num, rom in roman_numerals.items():
        instr = instr.replace(num.lower(), rom)
    return instr


def get_spell(name):
    # c.execute("SELECT * FROM Spell WHERE name=? COLLATE NOCASE",
    #           ("'{}'".format(roman_conv(name)),))
    c.execute("select * from Spell where name=:spellname collate NOCASE",
              {"spellname": "{}".format(roman_conv(name))})
    return schema(c.fetchone())


def embed_spell(name):
    spell_dict = get_spell(name)

    # handle no results from query
    if not spell_dict['name']:
        embed = Embed(title="No results found",
                      description="Check your spelling")
        return embed

    # each school of magic gets it's own color
    colors = {
        'abjuration': Color(0).dark_blue(),
        'conjuration': Color(0).magenta(),
        'divination': Color(0).teal(),
        'enchantment': Color(0).blue(),
        'evocation': Color(0).red(),
        'illusion': Color(0).purple(),
        'necromancy': Color(0).dark_purple(),
        'transmutation': Color(0).dark_gold(),
        'universalist': Color(0).dark_grey()
    }
    # if school is improperly formatted or not in dict, use lighter_grey
    color = colors[spell_dict['school']
                   ] if spell_dict['school'] in colors else Color(0).lighter_grey()

    # construct embed - char limits might cause 400 errors
    # character floors can also cause 400 errors
    # if an embed val = 0, discord with throw 400 error
    embed = Embed(title=spell_dict['name'][:256],
                  description=spell_dict['description'][:2048],
                  colour=color)
    embed.set_author(name=spell_dict['spell_level'][:256] or 'None')
    embed.add_field(name="Saving Throw",
                    value=spell_dict['saving_throw'][:1024] or 'None')
    embed.add_field(name="Duration",
                    value=spell_dict['duration'][:1024] or 'None')
    embed.add_field(name="Area of Effect",
                    value="Targets: {}\nRange: {}\nArea: {}".format(spell_dict['targets'] or 'None', spell_dict['range'] or 'None', spell_dict['area'] or 'None')[:1024])
    embed.add_field(name='Misc', value="\n".join(
        [spell_dict['descriptor'], spell_dict['school'], spell_dict['components'], spell_dict['casting_time']])[:1024])

    roman = {'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'}
    title = '-'.join([word for word in spell_dict['name'].split()
                      if word not in roman])

    embed.add_field(
        name='Link', value="http://www.d20pfsrd.com/magic/all-spells/{}/{}".format(spell_dict['name'][0], title))
    return embed


if __name__ == '__main__':
    while True:
        inname = input("Enter name: ")
        if inname in ['quit', 'exit']:
            break
        print(get_spell(inname))
    print("Goodbye")
