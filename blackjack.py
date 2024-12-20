import random
import matplotlib.pyplot as plt

# ==========================
# Configuration and Constants
# ==========================

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = (
    'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
    'Jack', 'Queen', 'King', 'Ace'
)
values = {
    'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
    'Eight': 8, 'Nine': 9, 'Ten': 10,
    'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11
}

# Card counting values for Hi-Lo system
count_values = {
    'Two': 1, 'Three': 1, 'Four': 1, 'Five': 1, 'Six': 1,
    'Seven': 0, 'Eight': 0, 'Nine': 0,
    'Ten': -1, 'Jack': -1, 'Queen': -1, 'King': -1, 'Ace': -1
}


# ==========================
# Classes
# ==========================

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self, num_decks=8):
        self.num_decks = num_decks
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks] * self.num_decks

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_one(self):
        if len(self.deck) == 0:
            print("Out of cards! Reshuffling the deck.")
            self.__init__(self.num_decks)
            self.shuffle()
        return self.deck.pop()

    def cards_remaining(self):
        return len(self.deck)


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def is_blackjack(self):
        return self.value == 21 and len(self.cards) == 2

    def can_split(self):
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

    def is_hard_total(self):
        aces_count = sum(1 for c in self.cards if c.rank == 'Ace')
        val_no_ace_11 = sum(10 if c.rank in ['Jack', 'Queen', 'King', 'Ten'] else values[c.rank]
                            for c in self.cards if c.rank != 'Ace')
        all_aces_as_one = val_no_ace_11 + aces_count
        return self.value == all_aces_as_one

    def __str__(self):
        return ', '.join(str(card) for card in self.cards) + f" (Value: {self.value})"


# ==========================
# Strategy and Advice
# ==========================

def basic_strategy_suggestion(player_hand, dealer_upcard, can_split):
    player_total = player_hand.value
    dealer_card_value = values[dealer_upcard.rank] if dealer_upcard.rank != 'Ace' else 11

    # Check for pair splitting
    if can_split:
        if player_hand.cards[0].rank in ['Ace', 'Eight']:
            return 'Split'
        if player_hand.cards[0].rank in ['Two', 'Three', 'Seven']:
            if dealer_card_value in range(2, 8):
                return 'Split'
        if player_hand.cards[0].rank == 'Six':
            if dealer_card_value in range(2, 7):
                return 'Split'
        if player_hand.cards[0].rank == 'Nine':
            if dealer_card_value not in [7, 10, 11]:
                return 'Split'
        if player_hand.cards[0].rank == 'Four':
            if dealer_card_value in [5, 6]:
                return 'Split'

    # Check soft totals
    soft = any(card.rank == 'Ace' for card in player_hand.cards) and player_total <= 21
    if soft:
        if player_total <= 17:
            return 'Hit'
        if player_total == 18:
            if dealer_card_value in range(2, 9):
                return 'Stand'
            else:
                return 'Hit'
        return 'Stand'

    # Hard totals
    if player_total <= 8:
        return 'Hit'
    elif player_total == 9:
        if dealer_card_value in [3,4,5,6]:
            return 'Double Down'
        else:
            return 'Hit'
    elif player_total == 10:
        if dealer_card_value in range(2,10):
            return 'Double Down'
        else:
            return 'Hit'
    elif player_total == 11:
        if dealer_card_value != 11:
            return 'Double Down'
        else:
            return 'Hit'
    elif player_total == 12:
        if dealer_card_value in range(4,7):
            return 'Stand'
        else:
            return 'Hit'
    elif player_total in range(13,17):
        if dealer_card_value in range(2,7):
            return 'Stand'
        else:
            return 'Hit'
    else:
        return 'Stand'


def explain_suggestion(suggestion):
    reasons = {
        'Hit': "Hitting improves your hand if it's too low.",
        'Stand': "Standing avoids risking a bust since your hand is good enough.",
        'Double Down': "Doubling down takes advantage of a favorable situation.",
        'Split': "Splitting can turn a marginal hand into two potentially better hands."
    }
    return reasons.get(suggestion, "No explanation available.")


def evaluate_hand_strength(hand):
    if hand.value >= 17:
        return "Strong"
    elif 12 <= hand.value <= 16:
        return "Moderate"
    else:
        return "Weak"


# ==========================
# Gameplay Functions
# ==========================

def hit(deck, hand):
    card = deck.deal_one()
    hand.add_card(card)
    print(f"Dealt card: {card}")
    return card


def hit_or_stand(deck, hand, can_double_down, can_split, dealer_upcard, basic_strategy=True):
    suggestion = basic_strategy_suggestion(hand, dealer_upcard, can_split)
    if basic_strategy:
        print(f"\nBasic Strategy Suggestion: {suggestion}")
        print("Reasoning:", explain_suggestion(suggestion))

    actions = ['H', 'S']
    action_descriptions = {
        'H': 'Hit - Take another card.',
        'S': 'Stand - End your turn.'
    }
    if can_double_down:
        actions.append('D')
        action_descriptions['D'] = 'Double Down - Increase your bet and take one more card.'
    if can_split:
        actions.append('P')
        action_descriptions['P'] = 'Split - Divide your pair into two hands.'

    print("\nAvailable Actions:")
    for act in actions:
        print(f"  {act}: {action_descriptions[act]}")

    while True:
        prompt = f"Choose action ({'/'.join(actions)}): "
        choice = input(prompt).strip().upper()
        if choice in actions:
            return choice
        else:
            print(f"Invalid input. Please enter {', '.join(actions)}.")


def split_hand(deck, hand):
    card1 = hand.cards[0]
    card2 = hand.cards[1]
    new_hand1 = Hand()
    new_hand1.add_card(card1)
    new_hand1.add_card(deck.deal_one())
    new_hand2 = Hand()
    new_hand2.add_card(card2)
    new_hand2.add_card(deck.deal_one())
    return new_hand1, new_hand2


def show_some(player_hand, dealer_hand):
    print("\n--- Current Table State ---")
    print("Dealer's Hand:")
    print(" <hidden card>")
    print('', dealer_hand.cards[1])
    print("\nPlayer's Hand:", *player_hand.cards, sep='\n ')
    print("--------------------------")


def show_all(player_hand, dealer_hand):
    print("\n--- Final Table State ---")
    print("Dealer's Hand:", *dealer_hand.cards, sep='\n ')
    print("Dealer's Hand Value:", dealer_hand.value)
    print("\nPlayer's Hand:", *player_hand.cards, sep='\n ')
    print("Player's Hand Value:", player_hand.value)
    print("-------------------------")


def take_bankroll():
    while True:
        try:
            bankroll = float(input("Enter your starting bankroll (e.g., 1000): $"))
            if bankroll <= 0:
                print("Bankroll must be greater than zero.")
            else:
                return bankroll
        except ValueError:
            print("Invalid input. Please enter a numerical value.")


def take_bet(bankroll):
    while True:
        try:
            bet = float(input(f"\nPlease enter your bet amount (Available: ${bankroll:.2f}): $"))
            if bet <= 0:
                print("Bet must be greater than zero.")
            elif bet > bankroll:
                print("You cannot bet more than your current bankroll.")
            else:
                return bet
        except ValueError:
            print("Invalid input. Please enter a numerical value.")


def take_insurance(bet):
    while True:
        choice = input("\nDealer has an Ace. Would you like to take insurance? (Y/N): ").strip().upper()
        if choice == 'Y':
            insurance_bet = bet / 2
            print(f"You placed an insurance bet of ${insurance_bet:.2f}.")
            return insurance_bet
        elif choice == 'N':
            return 0
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")


def update_count(card, running_count):
    running_count += count_values[card.rank]
    return running_count


def display_count_info(running_count, cards_left):
    decks_remaining = cards_left / 52.0
    true_count = running_count / decks_remaining if decks_remaining > 0 else running_count
    print(f"[Card Counting] Running Count: {running_count}, True Count: {true_count:.2f}")
    if true_count > 1:
        print("Positive true count: More high-value cards remain, favoring the player.")
    elif true_count < -1:
        print("Negative true count: Fewer high-value cards remain, not as favorable.")
    else:
        print("Neutral count: Balanced deck composition.")


# ==========================
# Main Game Loop
# ==========================

def play_game():
    print("Welcome to the Crown Perth Blackjack Simulator!")
    print("Rules:")
    print("- 8 Decks, Dealer stands on all 17s, hits on 16 or below.")
    print("- Blackjack pays 3:2.")
    print("- Double down allowed only on hard totals of 9, 10, or 11.")
    print("- Splits allowed if first two cards are a pair.")
    print("- Bet is placed before cards are dealt.\n")
    print("[Educational Note: We track card counting using the Hi-Lo system.]")
    print("2-6 = +1, 7-9 = 0, 10-Ace = -1\n")

    bankroll = take_bankroll()
    starting_bankroll = bankroll
    print(f"\nYour starting bankroll is: ${bankroll:.2f}")

    deck = Deck()
    deck.shuffle()

    hand_count = 0
    wins = 0
    losses = 0
    pushes = 0
    bankroll_history = [bankroll]
    running_count = 0

    while True:
        if bankroll <= 0:
            print("\nYou have run out of money! Game over.")
            break

        cards_left = deck.cards_remaining()
        print(f"\n[Educational Note] Cards remaining in the shoe: {cards_left}")
        print("Fewer cards = changed odds.")
        display_count_info(running_count, cards_left)

        bet = take_bet(bankroll)
        bankroll -= bet
        print(f"\nYou have bet: ${bet:.2f}")

        player_hands = [Hand()]
        dealer_hand = Hand()

        # Initial deal
        for _ in range(2):
            player_card = deck.deal_one()
            player_hands[0].add_card(player_card)
            running_count = update_count(player_card, running_count)

            dealer_card = deck.deal_one()
            dealer_hand.add_card(dealer_card)
            running_count = update_count(dealer_card, running_count)

        show_some(player_hands[0], dealer_hand)

        # Insurance
        insurance_bet = 0
        if dealer_hand.cards[0].rank == 'Ace':
            insurance_bet = take_insurance(bet)
            bankroll -= insurance_bet

        # Check dealer blackjack
        if dealer_hand.is_blackjack():
            show_all(player_hands[0], dealer_hand)
            if player_hands[0].is_blackjack():
                print("\nBoth player and dealer have Blackjack! It's a push.")
                bankroll += bet
                pushes += 1
            else:
                if insurance_bet > 0:
                    print("\nDealer has Blackjack. Insurance pays 2:1.")
                    bankroll += insurance_bet * 3
                print("\nDealer has Blackjack. You lose your bet.")
                losses += 1

            hand_count += 1
            bankroll_history.append(bankroll)
            new_game = input("\nWould you like to play another hand? (Y/N): ").strip().upper()
            if new_game == 'Y':
                print("\nStarting a new hand...\n")
                continue
            else:
                break

        # Check player blackjack
        if player_hands[0].is_blackjack():
            show_all(player_hands[0], dealer_hand)
            print("\nYou have a Blackjack! You win 3:2.")
            bankroll += bet * 2.5
            wins += 1
            hand_count += 1
            bankroll_history.append(bankroll)
            new_game = input("\nAnother hand? (Y/N): ").strip().upper()
            if new_game == 'Y':
                print("\nStarting a new hand...\n")
                continue
            else:
                break

        # Player's turn for all hands
        bets = [bet]
        i = 0
        while i < len(player_hands):
            current_hand = player_hands[i]
            current_bet = bets[i]
            can_split = current_hand.can_split() and bankroll >= current_bet
            can_double_down = (len(current_hand.cards) == 2 and current_hand.is_hard_total()
                               and current_hand.value in [9, 10, 11] and bankroll >= current_bet)

            player_turn_over = False

            # Player action loop
            while not player_turn_over and current_hand.value <= 21:
                hand_strength = evaluate_hand_strength(current_hand)
                print(f"\nHand {i+1}: {current_hand} - {hand_strength} Hand")
                print(f"Dealer's upcard: {dealer_hand.cards[0]}")
                print(f"Current Bankroll: ${bankroll:.2f}")
                display_count_info(running_count, deck.cards_remaining())

                choice = hit_or_stand(deck, current_hand, can_double_down, can_split, dealer_hand.cards[0])

                if choice == 'H':
                    new_card = deck.deal_one()
                    current_hand.add_card(new_card)
                    running_count = update_count(new_card, running_count)
                    print(f"Dealt card: {new_card}")
                    if current_hand.value > 21:
                        print(f"Hand {i+1} busts!")
                        player_turn_over = True
                    else:
                        print(f"Now {i+1}: {current_hand} (You can hit again if you want.)")

                elif choice == 'S':
                    print(f"Hand {i+1} stands.")
                    player_turn_over = True

                elif choice == 'D':
                    bankroll -= current_bet
                    bets[i] += current_bet
                    new_card = deck.deal_one()
                    current_hand.add_card(new_card)
                    running_count = update_count(new_card, running_count)
                    print(f"Dealt card: {new_card}")
                    if current_hand.value > 21:
                        print(f"Hand {i+1} busts!")
                    else:
                        print(f"Hand {i+1} after Double Down: {current_hand}")
                    player_turn_over = True

                elif choice == 'P':
                    if can_split and len(player_hands) < 4:
                        bankroll -= current_bet
                        new_hand1, new_hand2 = split_hand(deck, current_hand)
                        # Potentially update count for new cards dealt from split if needed

                        player_hands[i] = new_hand1
                        player_hands.insert(i+1, new_hand2)
                        bets.insert(i+1, current_bet)
                        print(f"\nHand {i+1} split into two hands:")
                        print(f"Hand {i+1}: {player_hands[i]}")
                        print(f"Hand {i+2}: {player_hands[i+1]}")
                        player_turn_over = True
                    else:
                        print("Cannot split this hand.")

            i += 1

        # Dealer's turn
        print("\nDealer's Turn:")
        show_all(player_hands[0], dealer_hand)

        while dealer_hand.value < 17:
            print("Dealer hits.")
            new_card = deck.deal_one()
            dealer_hand.add_card(new_card)
            running_count = update_count(new_card, running_count)
            print(f"Dealer's Hand: {dealer_hand}")
            if dealer_hand.value > 21:
                print("Dealer busts!")
                break
        if dealer_hand.value >= 17 and dealer_hand.value <= 21:
            print("Dealer stands.")

        # Settle bets
        for idx, hand in enumerate(player_hands):
            current_bet = bets[idx]
            print(f"\nSettling Hand {idx+1}: {hand}")
            if hand.value > 21:
                print(f"Hand {idx+1} busts. You lose ${current_bet:.2f}.")
                losses += 1
            elif dealer_hand.value > 21:
                print(f"Dealer busts. You win ${current_bet:.2f}.")
                bankroll += current_bet * 2
                wins += 1
            elif hand.value > dealer_hand.value:
                print(f"Hand {idx+1} wins. You win ${current_bet:.2f}.")
                bankroll += current_bet * 2
                wins += 1
            elif hand.value < dealer_hand.value:
                print(f"Hand {idx+1} loses. You lose ${current_bet:.2f}.")
                losses += 1
            else:
                print(f"Hand {idx+1} pushes. Your bet of ${current_bet:.2f} is returned.")
                bankroll += current_bet
                pushes += 1

        hand_count += 1
        bankroll_history.append(bankroll)

        if dealer_hand.is_blackjack():
            # Already handled above, no extra action needed
            pass
        else:
            if insurance_bet > 0:
                print("\nInsurance bet loses.")

        print(f"\nYour current bankroll is: ${bankroll:.2f}")
        display_count_info(running_count, deck.cards_remaining())

        new_game = input("\nWould you like to play another hand? (Y/N): ").strip().upper()
        if new_game == 'Y':
            print("\nStarting a new hand...\n")
        else:
            break

    # Session Summary
    final_bankroll = bankroll
    profit_loss = final_bankroll - starting_bankroll

    print("\n--- Session Summary ---")
    print(f"Total Hands Played: {hand_count}")
    print(f"Wins: {wins}, Losses: {losses}, Pushes: {pushes}")
    if hand_count > 0:
        win_rate = (wins / hand_count) * 100
    else:
        win_rate = 0.0
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Starting Bankroll: ${starting_bankroll:.2f}")
    print(f"Final Bankroll: ${final_bankroll:.2f}")
    if profit_loss >= 0:
        print(f"You made a profit of ${profit_loss:.2f}.")
    else:
        print(f"You had a loss of ${-profit_loss:.2f}.")

    # Plot bankroll over time
    plt.figure(figsize=(10, 5))
    plt.plot(bankroll_history, marker='o')
    plt.title("Bankroll Over Time")
    plt.xlabel("Hands Played")
    plt.ylabel("Bankroll")
    plt.grid(True)
    plt.axhline(y=starting_bankroll, color='r', linestyle='--', label='Starting Bankroll')
    plt.legend()

    # Plot distribution of outcomes
    outcomes = ['Wins', 'Losses', 'Pushes']
    counts = [wins, losses, pushes]
    plt.figure(figsize=(6, 4))
    plt.bar(outcomes, counts, color=['green', 'red', 'blue'])
    plt.title("Outcome Distribution")
    plt.ylabel("Count of Hands")
    for i, v in enumerate(counts):
        plt.text(i, v + 0.5, str(v), ha='center', fontweight='bold')

    plt.show()


if __name__ == "__main__":
    play_game()

