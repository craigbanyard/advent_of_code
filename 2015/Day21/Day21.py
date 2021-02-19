from helper import aoc_timer
import pandas as pd
import re
import itertools


class Shop:
    """Class for item shop."""

    def __init__(self, path):
        self.inventory = self.get_shop(path)

    def get_shop(self, path):
        """Read shop inventory into pandas DataFrame."""
        df = []
        for line in open(path).read().split('\n'):
            if not line:
                continue
            if ':' in line:
                # New item type (plus headers)
                idx = line.find(':')
                item_type = line[:idx]
                headers = ['Type', 'Item'] + line[idx+1:].split()
            else:
                # Item row - use RegEx to split on 2+ whitespaces
                df.append({k: v for k, v in zip(headers, [item_type] + re.split(r'\s{2,}', line))})
        return pd.DataFrame(df).astype({k: 'int8' for k in headers[2:]})


class Character:
    """Class for RPG characters."""

    def __init__(self, hp=0, damage=0, armor=0, path=None):
        self.path = path  # Optionally set character attributes from input file
        if path is None:
            # Manually set attributes when initializing
            self.hp = hp
            self.damage = damage
            self.armor = armor
        else:
            # Set attributes from input file
            attr = self.get_attr(path)
            self.hp = attr.get('Hit Points', 0)
            self.damage = attr.get('Damage', 0)
            self.armor = attr.get('Armor', 0)
        # Additional attributes
        self.gold = 0
        self.weapon_slots = range(1, 2)  # Must equip a weapon
        self.armor_slots = range(0, 2)   # Armor is optional
        self.ring_slots = range(0, 3)    # Maximum two rings
        # Inventory
        self.weapon_equip = None
        self.armor_equip = None
        self.rings_equip = None

    def __str__(self):
        """Print attributes and inventory."""
        attrs = {
            'HP': self.hp,
            'Damage': self.damage,
            'Armor': self.armor
        }
        equip = {
            'Weapon': self.weapon_equip,
            'Armor': self.armor_equip,
            'Rings': self.rings_equip,
            'Cost': self.gold
        }
        return f'Attributes: {attrs}\nInventory: {equip}'

    def get_attr(self, path):
        """Optionally set character attributes from input file."""
        return {k: int(v) for k, v in
                [line.strip().split(': ') for line in open(path).readlines()]}

    def purchase(self, items, shop):
        """Purchase items from the shop, amend attributes, record gold cost."""
        buy = shop.inventory.loc[items]
        self.damage = buy.Damage.sum()
        self.armor = buy.Armor.sum()
        self.gold = buy.Cost.sum()
        # Equip items
        self.weapon_equip = buy.Item.loc[buy.Type == 'Weapons'].tolist()
        self.armor_equip = buy.Item.loc[buy.Type == 'Armmor'].tolist()
        self.rings_equip = buy.Item.loc[buy.Type == 'Rings'].tolist()

    def attack(self, char):
        """Attack given character, char."""
        hit = max(1, self.damage - char.armor)
        char.hp = max(0, char.hp - hit)

    def battle(self, char, output=True):
        """Take turns (self attacks first) to attack until one character is defeated."""
        attacker, defender = self, char
        # Battle to the death
        while self.hp and char.hp:
            attacker.attack(defender)
            attacker, defender = defender, attacker
        # Battle complete
        if self.hp:
            if output:
                print('You win!')
                print(self)
            return True
        else:
            if output:
                print('You lose!')
                print(self)
            return False


@aoc_timer
def Day21(hp=100, output=False, part2=False):
    # Setup
    player = Character(hp, 0, 0)
    shop = Shop('shop.txt')

    # Combinations of available items
    inv = shop.inventory
    item_types = inv.Type.unique()
    combs = {k: [] for k in item_types}
    items = zip(
        [player.weapon_slots, player.armor_slots, player.ring_slots],  # Player inventory slots
        [inv.loc[inv.Type == x].index for x in item_types],            # Shop item indices
        item_types                                                     # Types of items
    )

    # Compile dictionary of all combinations of each item
    for slots, idx, item in items:
        for n in slots:
            for c in itertools.combinations(idx, n):
                combs[item].append(c)

    # Compile combinations of all possible items
    costs = {
        tuple(loadout): inv.Cost.loc[loadout].sum() for loadout in
        [list(sum(x, ())) for x in itertools.product(*combs.values())]
    }

    # Sort items by cost, purchase item combination and play game until condition is met
    for items, cost in sorted(costs.items(), key=lambda x: x[1], reverse=part2):
        # Reset characters
        player = Character(hp, 0, 0)
        boss = Character(path='input.txt')
        # Purchase item combination and battle
        player.purchase(list(items), shop)
        if player.battle(boss, output=False) ^ part2:
            return cost


# %% Output
def main():
    print("AoC 2015\nDay 21")
    print('Part 1:', Day21(part2=False))
    print('Part 2:', Day21(part2=True))


if __name__ == '__main__':
    main()
