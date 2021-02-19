from helper import aoc_timer
from collections import deque, defaultdict
import pandas as pd
import itertools
import random
import re


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


class Spellbook:
    """Class for magic spells."""

    def __init__(self, path):
        self.spells = pd.read_csv(path)


class Game:
    """Class for battling two characters."""

    def __init__(self, characters, difficulty='normal'):
        self.turn = 0
        self.characters = characters
        self.attacker, self.defender = characters
        self.battle_active = False
        self.battle_winner = None
        self.difficulty = difficulty

    def __str__(self):
        """Print battle status."""
        lines = [
            f"Battle between:\n\n{self.attacker.__str__()}\n",
            "and\n",
            f"{self.defender.__str__()}\n",
            f"Active: {self.battle_active}",
            f"Difficulty: {self.difficulty}",
            f"Turns: {self.turn}",
            f"Winner: {self.battle_winner.__class__.__name__}"
        ]
        return "\n".join(lines)

    def apply_effects(self, characters):
        """Apply active effects for a turn."""
        result = True
        for (char1, char2) in [characters, characters[::-1]]:
            if isinstance(char1, Wizard) and char1.active_effects:
                # Apply Damage, Armor, Mana over time effects
                for _, effect in char1.active_effects.items():
                    char2.hp = max(0, char2.hp - effect['dot'])
                    char1.armor += effect['aot']
                    char1.mana += effect['mot']
                    effect['timer'] -= 1
                # Pop expired effects
                char1.active_effects = {
                    k: v for k, v in char1.active_effects.items() if v['timer'] > 0
                }
                if not char2.hp:
                    # char2 is the only character whose hp can reduce
                    self.battle_winner = char1
                    result = False
        return result

    def take_turn(self):
        """Apply effects then perform attack."""
        if self.difficulty.lower() == 'hard' and self.attacker == self.characters[0]:
            # Decrement player (first character) health on their turn
            self.characters[0].hp -= 1
            if self.characters[0].hp <= 0:
                self.battle_winner = self.characters[1]
                return False
        # Apply effects
        if not self.apply_effects([self.attacker, self.defender]):
            return False
        # Attacker attacks defender
        if not self.attacker.attack(self.defender):
            return False
        self.attacker, self.defender = self.defender, self.attacker
        self.turn += 1
        # Reset Wizard attributes
        for char in self.characters:
            if isinstance(char, Wizard):
                char.reset_attribs()
        return True

    def battle(self, output=False):
        """Repeatedly attack until battle ends."""
        self.battle_active = True
        while self.battle_active:
            if output:
                print("\nBefore turn:")
                print("-" * 80)
                print(self.characters[0], "\n")
                print(self.characters[1], "\n")
            self.battle_active = self.take_turn()
        # Battle complete - determine winner if not already determined
        if self.battle_winner is None:
            if self.characters[1].hp:
                self.battle_winner = self.characters[1]
            else:
                self.battle_winner = self.characters[0]
        # Return battle results
        if self.battle_winner == self.characters[0]:
            if output:
                print("You win!")
                print(self.characters[0])
            return True
        else:
            if output:
                print("You lose!")
                print(self.characters[0])
            return False


class Character:
    """Base class for RPG characters.
       Should be used for the boss in Day21 and Day22.
    """

    def __init__(self, hp=0, damage=0, armor=0, path=None):
        self._path = path  # Optionally set character attributes from input file
        if self._path is None:
            # Manually set attributes when initializing
            self.hp = hp
            self.damage = damage
            self.armor = armor
        else:
            # Set attributes from input file
            attr = self.get_attr(self._path)
            self.hp = attr.get('Hit Points', 0)
            self.damage = attr.get('Damage', 0)
            self.armor = attr.get('Armor', 0)

    def __str__(self):
        """Print base attributes."""
        attrs = {
            'HP': self.hp,
            'Damage': self.damage,
            'Armor': self.armor
        }
        return f"Class: {self.__class__.__name__}\nAttributes: {attrs}"

    def get_attr(self, path):
        """Optionally set character attributes from input file."""
        return {k: int(v) for k, v in
                [line.strip().split(': ') for line in open(path).readlines()]}

    def attack(self, char):
        """Attack given character, char."""
        hit = max(1, self.damage - char.armor)
        char.hp = max(0, char.hp - hit)
        return char.hp > 0


class Warrior(Character):
    """RPG character class that uses standard attacks during battle.
       Warrior can also purchase and equip items from the shop using gold.
       These items affect the Warrior's base attributes.
    """

    def __init__(self, hp=0, damage=0, armor=0, path=None):
        # Inherit base stats from Character class
        super().__init__(hp, damage, armor, path)
        # Warrior attributes
        self.gold = 0
        self.weapon_slots = range(1, 2)    # Must equip a weapon
        self.armor_slots = range(0, 2)     # Armor is optional
        self.ring_slots = range(0, 3)      # Maximum two rings
        # Warrior inventory
        self.weapon_equip = None
        self.armor_equip = None
        self.rings_equip = None

    def __str__(self):
        """Print attributes and inventory."""
        attrs = super().__str__()
        equip = {
            'Weapon': self.weapon_equip,
            'Armor': self.armor_equip,
            'Rings': self.rings_equip,
            'Cost': self.gold
        }
        return f"{attrs}\nInventory: {equip}"

    def purchase(self, items, shop):
        """Purchase items from the shop, amend attributes, record gold cost."""
        buy = shop.inventory.loc[items]
        self.damage = buy.Damage.sum()
        self.armor = buy.Armor.sum()
        self.gold = buy.Cost.sum()
        # Equip items
        self.weapon_equip = buy.Item.loc[buy.Type == 'Weapons'].tolist()
        self.armor_equip = buy.Item.loc[buy.Type == 'Armor'].tolist()
        self.rings_equip = buy.Item.loc[buy.Type == 'Rings'].tolist()


class Wizard(Character):
    """RPG character class that casts magic spells during battle.
       Wizard can cast spells from the spellbook using mana.
       If Wizard cannot afford to cast any spells, he loses.
    """

    def __init__(self, hp=0, damage=0, armor=0, mana=0, path=None):
        # Inherit base stats from Character class
        super().__init__(hp, damage, armor, path)
        # Wizard attributes
        self.mana = mana
        self._damage = damage         # initial damage
        self._armor = armor           # initial armor
        self.cum_mana_cost = 0        # cumulative mana cost of cast spells
        self.spell_cast_order = []    # spells in the order in which they're cast
        self.spell_strategy = None    # planned spell strategy, set with set_spell_strategy method
        self.spellbook = None         # read as instance attribute using set_spell_strategy method
        # Spell effects
        self.active_effects = {}

    def __str__(self):
        """Print attributes and inventory."""
        attrs = super().__str__()
        equip = {
            'Mana': self.mana,
            'Cumulative Mana': self.cum_mana_cost,
            'Cast Order': self.spell_cast_order,
            'Effects': self.active_effects
        }
        return f"{attrs}\nInventory: {equip}"

    def get_spell(self):
        """Get user input spell (index) as integer."""
        return int(input("Enter a spell to cast: "))

    def set_spell_strategy(self, strategy, spellbook):
        """Set strategy, read spellbook."""
        if isinstance(strategy, str):
            # Named strategy (e.g. 'random')
            self.spell_strategy = strategy
        else:
            try:
                _ = iter(strategy)
            except TypeError:
                # Not iterable or string, default None value is fine so do nothing
                pass
            else:
                # Strategy is iterable (and not string) so create spell queue
                self.spell_strategy = deque(strategy)
        # Read spellbook into instance attribute
        self.spellbook = spellbook

    def get_castable(self):
        """Get indices of all spells that can be cast."""
        spells = self.spellbook.spells
        # Cost
        affordable = spells.loc[spells.Cost <= self.mana]
        # Not already active
        non_active = spells[~spells.Spell.isin(self.active_effects)]
        # Return merged index as list
        return affordable.reset_index().merge(non_active).set_index('index').index.tolist()

    def next_spell(self):
        """Return next spell from strategy."""
        # Get next spell from spell strategy
        if self.spell_strategy is None:
            # Manually enter spell index
            return self.get_spell()
        if isinstance(self.spell_strategy, str):
            # Named strategy
            if self.spell_strategy == 'random':
                # Pick castable spell at random
                castable = self.get_castable()
                if castable:
                    return random.choice(castable)
            return None
        if self.spell_strategy:
            # Pop from deque strategy
            return self.spell_strategy.popleft()
        return None

    def cast(self, spell):
        """Cast a spell from spellbook."""
        # Check spell is castable
        if spell not in self.get_castable():
            return False
        self.spell_cast_order.append(spell)
        spell = self.spellbook.spells.loc[spell]
        # Set immediate attributes from spell
        self.mana -= spell.Cost
        self.cum_mana_cost += spell.Cost
        self.damage = spell.Damage
        self.hp += spell.Heal
        # Set effects
        if spell.Duration:
            self.active_effects[spell.Spell] = {
                'timer': spell.Duration,
                'dot': spell.DoT,
                'aot': spell.AoT,
                'mot': spell.MoT
            }
        return True

    def reset_attribs(self):
        """Reset damage and armor attributes to starting values."""
        self.damage = self._damage
        self.armor = self._armor

    def attack(self, char):
        """Attack given character, char."""
        # Cast next spell from spell strategy
        spell = self.next_spell()
        if spell is None:
            return False
        if not self.cast(spell):
            return False
        # Apply instant damage from base class
        if self.damage:
            return super().attack(char)
        return True


@aoc_timer
def Day21(hp=100, output=False, part2=False):
    # Setup
    player = Warrior(hp, 0, 0)
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
        player = Warrior(hp, 0, 0)
        boss = Character(path='day21.txt')
        characters = [player, boss]
        game = Game(characters)
        # Purchase item combination and battle
        player.purchase(list(items), shop)
        if game.battle(output) ^ part2:
            return cost


@aoc_timer
def Day22(hp=50, mana=500, strategy='random', difficulty='normal', sims=10, output=False):
    best_spells = defaultdict(list)
    spellbook = Spellbook('spells.txt')
    for _ in range(sims):
        player = Wizard(hp=hp, mana=mana)
        boss = Character(path='input.txt')
        characters = [player, boss]
        game = Game(characters, difficulty)
        player.set_spell_strategy(strategy, spellbook)
        if game.battle(output=output):
            best_spells[player.cum_mana_cost].append(player.spell_cast_order)
    if strategy == 'random':
        return sorted(best_spells.items())
    return min(best_spells)


# %% Output
def main():
    print("AoC 2015\nDay 22")
    print("Part 1:", Day22(strategy=[3, 0, 4, 0, 3, 2, 0, 0], sims=1, difficulty='normal'))
    print("Part 2:", Day22(strategy=[3, 4, 2, 3, 1, 4, 3, 0], sims=1, difficulty='hard'))


if __name__ == '__main__':
    main()
