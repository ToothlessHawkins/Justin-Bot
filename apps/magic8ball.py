from random import choice


def magic_8_ball():
    resp = ["It is certain", "It is decidedly so", "Without a doubt",
            "Yes definitely", "You may rely on it", "As I see it, yes",
            "Most likely", "Outlook good", "Yes", "Signs point to yes",
            "Reply hazy try again", "Ask again later", "Better not tell you now",
            "Cannot predict now", "Concentrate and ask again", "Don't count on it",
            "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]

    return choice(resp)


if __name__ == '__main__':
    print("The mystical Magic 8 Ball")
    cont = 1
    while cont:
        question = input("What troubles you? ")
        print(magic_8_ball())
        cont = int(input("1 to play again, 0 to stop: ") or 1)
    print("Goodbye")
