from random import choice


# this method could be improved by just rolling 1-3 and picking outcome based on that
def rock_paper_scissors(throw):
    rps = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
    myChoice = choice(list(rps.keys()))
    if throw.lower() in rps:
        if myChoice == throw.lower():
            return "{}: Draw!".format(myChoice.title())
        elif throw.lower() == rps[myChoice]:
            return "{}: I win!".format(myChoice.title())
        else:
            return "{}: You win!".format(myChoice.title())
    else:
        return "Invalid input. Check your spelling."


if __name__ == '__main__':
    print("Rock Paper Scissors!")
    while True:
        throw = input("Your throw?: ")
        if throw in ['exit', 'quit']:
            break
        print(rock_paper_scissors(throw))
    print("Goodbye")
