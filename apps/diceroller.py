from random import randint
from re import findall


def dice_roller(rollval):
    try:
        d = findall(r'\d+', rollval)
        res = 0
        for _ in range(int(d[0])):
            res += randint(1, int(d[1]))
        if len(d) > 2:
            res += int(d[2])
        return res
    except IndexError:
        return "Incorrect format. Try !help."


if __name__ == '__main__':
    print("Dice roller: [X]d[Y]+[Z]")
    print("Enter 'quit' or 'exit' to quit.")

    while True:
        roll = input("Enter your roll: ")
        if roll.lower() in ['quit', 'exit']:
            break
        print(dice_roller(roll))
    print("Goodbye")
