import random


def generate_random_number():
    return random.randint(1, 10)


def get_player_guess():
    return int(input("Enter your guess: "))


def check_guess(guess, answer):
    if guess < answer:
        return "Too low!"
    elif guess > answer:
        return "Too high!"
    else:
        return "Correct!"


def main():
    answer = generate_random_number()
    while True:
        guess = get_player_guess()
        result = check_guess(guess, answer)
        print(result)
        if result == "Correct!":
            break


if __name__ == "__main__":
    main()
