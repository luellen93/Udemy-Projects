'''
Blackjack Simulator
'''

import random
import time
import os
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)



suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:

    def __init__(self, suit, rank):

        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'
    
class Deck:

    def __init__(self):

        self.deck = []
        
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
       
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp
    
    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card
    
class Hand:

    def __init__(self):

        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):

        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:

    def __init__(self):

        self.total = 100
        self.bet = 0

    def win_bet(self):

        self.total += self.bet

    def lose_bet(self):

        self.total -= self.bet

def take_bet(chips):

    while True:
        try:
            chips.bet = int(input("Please enter your bet amount: "))
            while chips.bet < 1:
                chips.bet = int(input("Please enter your bet amount: "))

        except:
            print("Please enter a valid bet amount.")

        else:
            if chips.bet > chips.total:
                print(f"Chips total not sufficient. You have {chips.total} chips.")
            else:
                break

def hit(deck, hand):

    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing

    while True:

        x = input("Hit or Stand? Enter h or s ")

        if x[0].lower() == 'h':
            hit(deck, hand)
        
        elif x[0].lower() == 's':
            print("Player stands. Dealer's turn.")
            playing = False

        else:
            print("Sorry, I did not understand your command. Please enter h or s only.")
        break

def show_some(player, dealer):
    
    # Show only one dealer card 
    print(Back.WHITE + Fore.BLACK + "\n Dealer's Hand: ")
    print("First card hidden!")
    print(dealer.cards[1])
    print(Fore.CYAN + Style.BRIGHT + f'Dealer hand total: {values[dealer.cards[1].rank]}')

    # Show all of players cards
    print(Back.WHITE + Fore.BLACK + "\n Player's hand: ")
    for card in player.cards:
        print(card)
    print(Fore.CYAN + Style.BRIGHT + f'Player hand total: {player_hand.value}')
    

def show_all(player, dealer):

    # Show all the dealer's cards
    print(Back.WHITE + Fore.BLACK + "\n Dealer's hand: ")
    for card in dealer.cards:
        print(card)
    # Calculate value and display
    print(Fore.CYAN + Style.BRIGHT + f"Value of Dealer's hand is: {dealer.value}")

    # Show all of the players cards
    print(Back.WHITE + Fore.BLACK + "\n Player's hand: ")
    for card in player.cards:
        print(card)
    print(Fore.CYAN + Style.BRIGHT + f"Value of Player's hand is: {player.value}")

def player_busts(player, dealer, chips):
    print(Fore.YELLOW + "Players busts!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print(Fore.MAGENTA + Style.BRIGHT + "Player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print(Fore.MAGENTA + Style.BRIGHT + "Player wins, Dealer busted!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print(Fore.YELLOW + "Dealer wins!")
    chips.lose_bet()

def push(player, dealer):
    print("Dealer and player tie. Push!")

def clear_screen():
    # Clear the screen for Windows
    if os.name == 'nt':
        os.system('cls')
    # Clear the screen for macOS and Linux
    else:
        os.system('clear')

'''
This begins the logic engine of the game
'''

player_chips = Chips()
#Game logic
while True:
    #Opening statement
    print("Welcome To Blackjack!")
    print(Fore.GREEN + f'Starting chips are: {player_chips.total}')

    #Create a new deck object
    deck = Deck()
    deck.shuffle()

    #Create a hand object for the player/dealer
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    

    #Prompt player for bet
    
    take_bet(player_chips)

    #Show cards (keeping one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:

        #prompt player for hit or stand
        hit_or_stand(deck, player_hand)

        #Show cards (keeping one dealer card hidden)
        clear_screen()
        show_some(player_hand, dealer_hand)

        #If player hand exceeds 21
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
    
    #If player hasn't busted, player dealer's hand until dealer reaches 17/busts
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        #Show all cards now that dealer is done playing
        clear_screen()
        show_all(player_hand, dealer_hand)

        #Determine winner
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    #Inform player of chip total
    print(Fore.GREEN + f"\n Player total chips are: {player_chips.total}")

    #Determine if chip total is 0
    if player_chips.total == 0:
        print("Thanks for playing Blackjack!")
        break

    #Ask to play again

    while True:
        new_game = input("Would you like to play another hand? y/n ")
        if new_game.lower() == 'y' or new_game.lower() == 'n':
            break
        

    if new_game[0].lower() == 'y':
        playing = True
        clear_screen()
        continue
    else:
        print("Thanks for playing Blackjack!")
        clear_screen()
        break
