import random
import json

# Define card suits and values
suits = ['♦', '♣', '♥', '♠']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# Load player data from file
try:
    with open('players.json', 'r') as f:
        players = json.load(f)
except FileNotFoundError:
    players = {}

def deck():
    """
    This function creates a deck of 52 cards with suits.
    """
    deck = []
    for suit in suits:
        for value in values:
            deck.append((value, suit))
    random.shuffle(deck)
    return deck

def value(hand):
    """
    This function calculates the value of a blackjack hand.
    """
    total = 0
    aces = 0
    for card in hand:
        total += values[card[0]]
        if card[0] == 'Ace':
            aces += 1
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def new_player(name):
    """
    This function creates a new player with name and initializes their stats.
    """
    players[name] = {'games_played': 0, 'games_won': 0, 'games_lost': 0, 'games_tied': 0}
    with open('players.json', 'w') as f:
        json.dump(players, f)

def select_player():
    """
    This function allows the user to select an existing player or create a new player.
    """
    print("Select a player:")
    for player in players:
        print(player)
    print("Type 'new' to create a new player")
    name = input("Enter player name: ")
    if name == 'new':
        name = input("Enter new player name: ")
        new_player(name)
    return name

def blackjack():
    """
    This function simulates a game of blackjack.
    """
    name = select_player()
    player_hand = []
    dealer_hand = []
    d = deck()
    player_hand.append(d.pop())
    dealer_hand.append(d.pop())
    player_hand.append(d.pop())
    dealer_hand.append(d.pop())
    print(f"\nDealer's hand: [{dealer_hand[0][0]} of {dealer_hand[0][1]}, ***]")
    print(f"{name}'s hand: {[card[0] + ' of ' + card[1] for card in player_hand]}")
    while True:
        if value(player_hand) > 21:
            print("Player busts!")
            players[name]['games_played'] += 1
            players[name]['games_lost'] += 1
            with open('players.json', 'w') as f:
                json.dump(players, f)
            return
        action = input("Do you want to hit or stand? ")
        if action.lower() == 'hit':
            player_hand.append(d.pop())
            print(f"{name}'s hand: {[card[0] + ' of ' + card[1] for card in player_hand]}")
        elif action.lower() == 'stand':
            break
    print(f"Dealer's hand: {[card[0] + ' of ' + card[1] for card in dealer_hand]}")
    while value(dealer_hand) < 19:
        dealer_hand.append(d.pop())
        print(f"Dealer's hand: {[card[0] + ' of ' + card[1] for card in dealer_hand]}")

    if value(dealer_hand) > 21:
        print("Dealer busts!")
        players[name]['games_played'] += 1
        players[name]['games_won'] += 1
        with open('players.json', 'w') as f:
            json.dump(players, f)
        return
    elif value(dealer_hand) > value(player_hand):
        print("Dealer wins!")
        players[name]['games_played'] += 1
        players[name]['games_lost'] += 1
        with open('players.json', 'w') as f:
            json.dump(players, f)
        return
    elif value(player_hand) > value(dealer_hand):
        print(f"{name} wins!")
        players[name]['games_played'] += 1
        players[name]['games_won'] += 1
        with open('players.json', 'w') as f:
            json.dump(players, f)
        return
    else:
        print("It's a tie!")
        players[name]['games_played'] += 1
        players[name]['games_tied'] += 1
        with open('players.json', 'w') as f:
            json.dump(players, f)
        return

while True:
    print("\nMAIN MENU")
    print("1. Start new game")
    print("2. View player statistics")
    print("3. Quit")
    choice = input("Enter your choice: ")
    if choice == '1':
        blackjack()
    elif choice == '2':
        name = select_player()
        stats = players[name]
        print(f"\n{name}'s statistics:")
        print(f"Games played: {stats['games_played']}")
        print(f"Games won: {stats['games_won']}")
        print(f"Games lost: {stats['games_lost']}")
        print(f"Games tied: {stats['games_tied']}")
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")


