import random
#test change
# -----------------------------
# Core Game Logic
# -----------------------------

class NegotiationGame:
    def __init__(self, seed=42):
        random.seed(seed)

        # Player resources
        self.player_money = 50_000_000

        # Market + hidden variables
        self.league_value = random.randint(8_000_000, 15_000_000)
        self.true_min_price = int(self.league_value * random.uniform(0.7, 0.95))  # hidden
        self.founder_desperation = random.randint(40, 90)  # hidden
        self.investor_risk_tolerance = random.randint(40, 80)  # hidden

        # Public variables
        self.debt = 40_680_000
        self.trust = 50
        self.investor_confidence = 50
        self.athlete_support = 50

        # State
        self.round = 1
        self.max_rounds = 6
        self.deal_made = False
        self.last_counter = None
        self.history = []

    # -----------------------------
    # Mechanics
    # -----------------------------

    def evaluate_offer(self, offer):
        score = 0

        # Price vs hidden minimum
        if offer >= self.true_min_price:
            score += 40
        elif offer >= self.true_min_price * 0.85:
            score += 25
        else:
            score += 10

        # Stakeholders
        score += self.trust * 0.2
        score += self.investor_confidence * 0.2
        score += self.athlete_support * 0.2

        # Debt penalty
        if self.debt > 30_000_000:
            score -= 20

        # Desperation boost
        score += self.founder_desperation * 0.1

        return score

    def make_offer(self, offer):
        score = self.evaluate_offer(offer)

        if score > 80:
            self.deal_made = True
            return "accepted", None

        elif score > 60:
            counter = int((offer + self.true_min_price) / 2)
            self.last_counter = counter
            self.trust += 5
            return "counter", counter

        else:
            self.trust -= 10
            return "rejected", None

    def package_deal(self):
        if random.random() > 0.4:
            reduction = random.randint(8_000_000, 15_000_000)
            self.debt -= reduction
            self.trust += 10
            return True, reduction
        else:
            self.trust -= 5
            return False, 0

    def ask_questions(self):
        self.trust += 10
        self.investor_confidence += 5

    def appeal_athletes(self):
        self.athlete_support += 15
        self.trust += 5

    def appeal_investors(self):
        self.investor_confidence += 15
        self.trust += 5

    def walk_away(self):
        success = random.random()
        return success > 0.4

# -----------------------------
# Console UI
# -----------------------------

def main():
    game = NegotiationGame()

    print("🏁 Track League Negotiation Simulator")
    print()

    while not game.deal_made and game.round <= game.max_rounds:
        print(f"Round {game.round}")
        print(f"Trust: {game.trust}")
        print(f"Investor Confidence: {game.investor_confidence}")
        print(f"Athlete Support: {game.athlete_support}")
        print(f"Debt: ${game.debt:,}")
        print()

        print("Choose an action:")
        print("1. Make an Offer")
        print("2. Ask Questions")
        print("3. Package Deal")
        print("4. Appeal to Athletes")
        print("5. Appeal to Investors")
        print("6. Walk Away (BATNA)")
        print("7. Next Round")

        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            try:
                offer = int(input("Enter offer amount: "))
                result, counter = game.make_offer(offer)
                if result == "accepted":
                    print("Deal Accepted!")
                elif result == "counter":
                    print(f"Counteroffer: ${counter:,}")
                else:
                    print("Offer Rejected")
            except ValueError:
                print("Invalid amount")

        elif choice == "2":
            game.ask_questions()
            print("Trust and investor confidence increased")

        elif choice == "3":
            success, reduction = game.package_deal()
            if success:
                print(f"Debt reduced by ${reduction:,}")
            else:
                print("Package proposal rejected")

        elif choice == "4":
            game.appeal_athletes()
            print("Athlete support increased")

        elif choice == "5":
            game.appeal_investors()
            print("Investor confidence increased")

        elif choice == "6":
            success = game.walk_away()
            if success:
                print("Your new league succeeds!")
            else:
                print("Your new league struggles.")
            return

        elif choice == "7":
            game.round += 1
            if game.round > game.max_rounds:
                print("Negotiation window closed")

        else:
            print("Invalid choice")

        print("-" * 40)

    if game.deal_made:
        print("You acquired the league!")
    else:
        print("Negotiation failed.")

if __name__ == "__main__":
    main()