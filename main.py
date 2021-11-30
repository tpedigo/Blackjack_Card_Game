import random

# Lists for how the cards will be created
suits = ("Hearts", "Diamonds", "Clubs", "Spades")
numbers = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10,
          "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}


class Card:

    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        self.value = values[number]

    def __str__(self):
        return f"{self.number} of {self.suit}"


class Deck:

    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for number in numbers:
                created_card = Card(number, suit)
                self.all_cards.append(created_card)

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()


class Player:

    def __init__(self, balance=0):
        self.hand = []
        self.balance = balance

    def add_cards(self, new_card):
        self.hand.append(new_card)

    def bet_money(self):
        bet_amount = input("What would you like to bet? ")
        asking_bet = True
        while asking_bet:
            if bet_amount.isdigit():
                bet_amount = int(bet_amount)
                betting = True
                while betting:
                    if int(bet_amount) > int(self.balance):
                        bet_amount = input(f"Sorry, you only have {self.balance} in your balance. Please try another "
                                           f"bet: ")
                        asking_bet = False
                    else:
                        print(f"Great! You bet {bet_amount}.")
                        betting = False
                        asking_bet = False
            else:
                bet_amount = input("Sorry, that is not a number. Please try again: ")

        return bet_amount

    def __str__(self):
        str_hand = ""
        for i in range(len(self.hand)):
            str_hand += f"\n{self.hand[i]}"
        return str_hand


def ace_card(player):
    # Seeing if a Player has an Ace in their hand
    aces = 0
    for i in range(len(player.hand)):
        if player.hand[i].number == "Ace":
            aces += 1
    return aces


def hand_total(player):
    total = 0
    for i in range(len(player.hand)):
        total += player.hand[i].value
    return total


playing = True


def ask_repeat():
    global playing, user_balance, new_game
    asking_repeat = True
    while asking_repeat:
        if user_balance != 0:
            repeat = input("Do you want to play again? Y or N ")
            if repeat.upper() != "Y" and repeat.upper() != "N":
                print("Sorry, that is not a Y or N. Please try again.")
            if repeat.upper() == "Y":
                print("Great!")
                asking_repeat = False
                new_game = True
                playing = True
            if repeat.upper() == "N":
                print("Goodbye!")
                asking_repeat = False
                playing = False
                new_game = False
        if user_balance == 0:
            repeat = input("You're out of money! Do you want to play again? Y or N ")
            if repeat.upper() != "Y" and repeat.upper() != "N":
                print("Sorry, that is not a Y or N. Please try again.")
            if repeat.upper() == "Y":
                user_balance = int(input("Great! How much money are you starting with? "))
                asking_repeat = False
                new_game = True
                playing = True
            if repeat.upper() == "N":
                print("Goodbye!")
                asking_repeat = False
                playing = False
                new_game = False

    return playing, new_game, user_balance


new_game = True
while new_game:
    new_deck = Deck()
    new_deck.shuffle()

    print(f"Welcome to Blackjack! Let's see who can get closest to 21.")
    user_balance = input("How much money are you starting with? ")
    asking_balance = True
    while asking_balance:
        if user_balance.isdigit():
            user_balance = int(user_balance)
            print(f"Great! Your balance is {user_balance}.")
            asking_balance = False
            new_game = False
        else:
            user_balance = input("Sorry, that is not a number. Please try again: ")

while playing:
    computer = Player()
    user = Player(user_balance)

    for i in range(2):
        user.add_cards(new_deck.deal_one())
        computer.add_cards(new_deck.deal_one())

    print(f"\nLet's begin. \n\nHere is the Dealer's first card: {computer.hand[0]} \n\nHere is your hand: "
          f"\n{user.__str__()}")

    user_bet = int(user.bet_money())

    compare_scores = True
    computer_turn = True
    asking_hit_or_stay = True
    while asking_hit_or_stay:
        user_aces = ace_card(user)
        user_total = hand_total(user)
        if user_total == 21:
            print("That's 21! You win!")
            user_balance += user_bet
            print(f"Here is your new balance {user_balance}.")
            asking_hit_or_stay = False
            computer_turn = False
            compare_scores = False
        if user_total > 21 and user_aces != 0:
            new_total = user_total - (10 * user_aces)
            if new_total > 21:
                print("Bust! You lose.")
                user_balance -= user_bet
                print(f"Here is your new balance {user_balance}.")
                asking_hit_or_stay = False
                computer_turn = False
                compare_scores = False
            if new_total == 21:
                print("That's 21! You win.")
                user_balance += user_bet
                print(f"Here is your new balance {user_balance}.")
                asking_hit_or_stay = False
                computer_turn = False
                compare_scores = False
            if new_total < 21:
                player_choice = input("\nDo you want to hit or stay? (H or S): ")
                if player_choice.upper() == "H":
                    user.add_cards(new_deck.deal_one())
                    print(f"Got it. Here is your hand: \n{user.__str__()}")
                    continue
                if player_choice.upper() == "S":
                    print("\nGot it. I will go now.")
                    asking_hit_or_stay = False
                else:
                    print("Sorry, that is not an H or S. Please try again.")
        if user_total > 21 and user_aces == 0:
            print("Bust! You lose.")
            user_balance -= user_bet
            print(f"Here is your new balance {user_balance}.")
            asking_hit_or_stay = False
            computer_turn = False
            compare_scores = False
        if user_total < 21:
            player_choice = input("\nDo you want to hit or stay? (H or S): ")
            if player_choice.upper() == "H":
                user.add_cards(new_deck.deal_one())
                print(f"Got it. Here is your hand: \n{user.__str__()}")
                continue
            if player_choice.upper() == "S":
                print("\nGot it. I will go now.")
                asking_hit_or_stay = False
            else:
                print("Sorry, that is not an H or S. Please try again.")

    while computer_turn:
        computer_aces = ace_card(computer)
        computer_total = hand_total(computer)
        if computer_total == 21:
            print(f"\nHere is my hand: \n{computer.__str__()}")
            print("I got 21! I win.")
            user_balance -= user_bet
            print(f"Here is your new balance {user_balance}.")
            computer_turn = False
            compare_scores = False
        if computer_total > 21 and computer_aces != 0:
            computer_new_total = computer_total - (10 * computer_aces)
            if computer_new_total > 21:
                computer.hand.pop()
                computer_turn = False
            if computer_new_total == 21:
                print(f"\nHere is my hand: \n{computer.__str__()}")
                print("I got 21! I win.")
                user_balance -= user_bet
                print(f"Here is your new balance {user_balance}.")
                computer_turn = False
                compare_scores = False
            if computer_new_total < 21:
                # print(f"\nHere is my hand: \n{computer.__str__()}")
                computer.add_cards(new_deck.deal_one())
                continue
        if computer_total > 21 and computer_aces == 0:
            computer.hand.pop()
            computer_turn = False
        if computer_total < 21:
            # print(f"\nHere is my hand: \n{computer.__str__()}")
            computer.add_cards(new_deck.deal_one())
            continue

    final_computer_total = hand_total(computer)
    final_user_total = hand_total(user)
    while compare_scores:
        print(f"\nHere is my final hand: \n{computer.__str__()}")
        if final_computer_total > final_user_total:
            print("\nI win!")
            user_balance -= user_bet
            print(f"Your new balance is {user_balance}.")
            compare_scores = False
        if final_computer_total == final_user_total:
            print("\nDraw!")
            print(f"Your balance is still {user_balance}.")
            compare_scores = False
        if final_computer_total < final_user_total:
            print("\nYou win!")
            user_balance += user_bet
            print(f"Your new balance is {user_balance}.")
            compare_scores = False

    playing, new_game, user_balance = ask_repeat()
