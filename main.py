import random
import time


class Location:
    def __init__(self, name: str, output: str, intake: str):
        self.prices = {
            "Metal": 10.0,
            "Wood": 5.0,
            "Food": 2.5,
            "Cogs": 15.0,
            "Machinery": 20.0
        }

        self.prices[output] = self.prices[output] * 0.5
        self.prices[intake] = self.prices[intake] * 2

        self.name = name

        self.distances = {}

    def fluctuate_prices(self):
        for k, v in self.prices.items():
            self.prices[k] = round(v + (v * (random.randint(-25, 25) / 100)), 2)


locations = [Location("Factory", "Cogs", "Metal"), Location("Farm", "Food", "Wood"),
             Location("Forest", "Wood", "Machinery"), Location("City", "Machinery", "Food"),
             Location("Mines", "Metal", "Cogs")]

# Determine distances in days to travel
for i, l in enumerate(locations):
    other_locations = locations.copy()
    other_locations.pop(i)
    for o in other_locations:
        l.distances[o.name] = random.randint(1, 5)


def main():
    days = 1
    coins = 100
    inventory = {
        "Metal": 0,
        "Wood": 0,
        "Food": 0,
        "Cogs": 0,
        "Machinery": 0
    }

    print(
        "This is a trading game, inspired by this (https://github.com/Susseratal/Fantasy-trading-system).",
        "It's loosely based on the travelling salesman problem."
        "\nThe basic premise of the game is that you will move between 5 different locations, buying and selling 5 "
        "different types of commodity. ",
        "Each location has a particular item it generally sells for less, and one it generally buys for more. ("
        "Representing different economy types) "
        "However, there is a number of days required to move between each location, during which time the prices will "
        "fluctuate. This is to accurately model the invisible hand of the free market with a random number generator. "
        "\nThe objective of this game is to reach 1000 coins in as few days as possible.",
        "\n\nEconomy types and preferred item to buy/sell:\nFactory: Metal/Cogs\nFarm: Wood/Food\nForest: "
        "Machinery/Wood\nCity: Food/Machinery\nMines: Cogs/Metal\n\n"
    )

    choice = "0"
    while choice not in ["1", "2", "3", "4", "5"]:
        print("Choose a starting location:")
        print("1: Factory | 2: Farm | 3: Forest | 4: City | 5: Mines")
        choice = input()
    current_location = locations[int(choice) - 1]

    # Main game loop
    running = True
    while running:
        # Display interface

        if coins >= 500:
            print(f"You won the game in {days} days, with a final score of {coins} coins!")
            input()
            break

        print("\n\n" + "-" * 30)

        print(f"Day: {days}")
        print(f"Coins: {coins}")
        print("Inventory:")
        for k, v in inventory.items():
            print(f"{k}: {v}")

        print(f"\nCurrent location: {current_location.name}")
        print("Prices:")
        for k, v in current_location.prices.items():
            print(f"{k}: {v} coins")

        print(f"\nDays to travel to:")
        for k, v in current_location.distances.items():
            print(f"{k}: {v}")

        print("\n1: Buy items | 2: Sell items | 3: Travel")
        decision = input()

        if decision == "1":
            print("Choose an item to buy:")
            print("Metal | Wood | Food | Cogs | Machinery")
            item = input().capitalize()
            if item not in ["Metal", "Wood", "Food", "Cogs", "Machinery"]:
                print("Not a valid item, press enter to continue")
                input()
            else:
                print("How many units do you want to buy: ")
                num_units = int(input())
                cost = current_location.prices[item] * num_units
                if cost > coins:
                    print("You don't have enough coins for that, press enter to continue")
                    input()
                else:
                    inventory[item] = inventory[item] + num_units
                    coins -= cost
                    print(f"Brought {num_units} {item} for {cost}, press enter to continue")
                    input()
        elif decision == "2":
            print("Choose an item to sell:")
            print("Metal | Wood | Food | Cogs | Machinery")
            item = input().capitalize()
            if item not in ["Metal", "Wood", "Food", "Cogs", "Machinery"]:
                print("Not a valid item, press enter to continue")
                input()
            else:
                print("How many units do you want to sell: ")
                num_units = int(input())
                if num_units > inventory[item]:
                    print("You don't have enough units of that item, press enter to continue")
                    input()
                else:
                    profit = current_location.prices[item] * num_units
                    inventory[item] = inventory[item] - num_units
                    coins += profit
                    print(f"Sold {num_units} {item} for {profit}, press enter to continue")
                    input()
        elif decision == "3":
            available_locations = [i for i in locations if i.name != current_location.name]
            for l in available_locations:
                print(f"\n{l.name}:")
                print(f"Days to travel to: {current_location.distances[l.name]}")
                print("Current prices (will change during travel):")
                for k, v in l.prices.items():
                    print(f"{k}: {v} coins")

            available_locations_names = [i.name for i in available_locations]

            print("\nChoose a location to go to:")
            print(" | ".join(available_locations_names))
            chosen_location = input().capitalize()
            if chosen_location not in available_locations_names:
                print("Not a valid location, press enter to continue")
                input()
            else:
                # Change prices
                days_to_travel = current_location.distances[chosen_location]
                days += days_to_travel
                for i in range(days_to_travel):
                    for l in locations:
                        l.fluctuate_prices()

                print(f"Travelling to {chosen_location}")
                current_location = locations[[i.name for i in locations].index(chosen_location)]
                time.sleep(days_to_travel)

        else:
            print("Not a valid command, press enter to continue")
            input()


if __name__ == '__main__':
    main()
