from random import randint
from re import compile, match, IGNORECASE
import operator


def normalize_operator(op_param):
    # pretty sure this is actually the fastest  way to do this, since dict lookup is O(1) in python
    convert_normal = {
        "*": operator.mul,
        "x": operator.mul,
        "X": operator.mul,
        "+": operator.add,
        "-": operator.sub,
        "/": operator.truediv,
        "\\": operator.truediv
    }

    # let this fail if it operator is not in the recognized list
    return convert_normal.get(op_param)


def query_parser(query):
    # match: up to 4 digits as group 0; the letter d or D; up to 4 digits as group 1; optionally a mathematical operator (+, -, / or \, * or x or X); optionally up to 6 digits as group 2;
    pattern = compile(r'(\d{,4})[dD](\d{,4})([\+xX\*\-\/\\])?(\d{,6})?', IGNORECASE)
    try:
        number, faces, operator, modifier = pattern.match(query.replace(" ", "")).groups()
    except AttributeError:
        # this is me being too lazy to just break that line up
        return {"error": "Incorrect format, probably. Format: [number of dice <= 9999]d[number of faces <= 9999][optional arithmetic operator][optional modifier <= 999999]  `1d20+10`"}
    # print(number, faces, operator, modifier)
    if not number or not faces:
        return {"error": "Incorrect format. Format: [number of dice <= 9999]d[number of faces <= 9999][optional arithmetic operator][optional modifier <= 999999]  `1d20+10`"}
    elif modifier and not operator:
        # the regex should make this code unreachable
        return {"error": "invalid or no arithmetic detected. Supported operators: \n  addition: `+`\n  subtraction: `-`\n  multiplication: `*` `x` `X`\n  division: `/` `\`"}

    results = {
        "number": int(number),
        "faces": int(faces),
    }

    # the regex should not allow a situation where operator does not exist
    # this code should ensure there should never be a situation where an operator exists but a modifier does not
    # this also allows modifier to be 0. I could just add `and int(modifier)`, but I want to bait Francisco
    if modifier:
        results.update({
            "operator": operator,
            "modifier": int(modifier)
        })

    # catch francisco
    if results.get("modifier", None) == 0 and operator in ["\\", "/"]:
        return {"error": "Nice try."}

    return results


def dice_roller(raw_query):
    params = query_parser(raw_query)

    if params.get("error", None):
        return params.get("error")

    num = params.get("number")
    face = params.get("faces")
    mod = params.get("modifier", '')
    op = params.get("operator", '')

    res = 0
    for _ in range(num):
        res += randint(1, face)

    if op:
        res = normalize_operator(op)(res, mod)

    return "`{}d{}{}{}:` \n{}".format(num, face, op, mod, res)


if __name__ == '__main__':
    print("Dice roller: [X]d[Y]+[Z]")
    print("Enter 'quit' or 'exit' to quit.")

    while True:
        roll = input("Enter your roll: ")
        if roll.lower() in ['quit', 'exit']:
            break
        print(dice_roller(roll))
    print("Goodbye")
