import random
from .game_model import Axie, GameData # Import Axie and GameData from game_model

class BattleSimulator:
    """Represents a battle between two teams of Axies."""
    def __init__(self, team1: list[Axie], team2: list[Axie], game_data: GameData):
        """
        Initializes a new battle.

        Args:
            team1 (list[Axie]): The first team of Axies.
            team2 (list[Axie]): The second team of Axies.
            game_data (GameData): The loaded game data object.
        """
        # Filtra apenas Axies com HP > 0
        self.team1 = [axie for axie in team1 if axie.current_stats['HP'] > 0]
        self.team2 = [axie for axie in team2 if axie.current_stats['HP'] > 0]
        self.game_data = game_data
        self.turn_count = 0
        self.log = [] # To store battle events

        # Initialize battle state for each Axie
        for axie in self.team1 + self.team2:
            axie.current_stats['HP'] = axie.base_stats['HP']
            axie.energy = 3 # Starting energy (Origin default)
            axie.hand = []
            axie.deck = axie.get_cards().copy()
            random.shuffle(axie.deck)
            axie.discard_pile = []

        self.log_event("Battle started!")
        self.log_event(f"Team 1: {[a.axie_id for a in self.team1]}")
        self.log_event(f"Team 2: {[a.axie_id for a in self.team2]}")

    def log_event(self, event: str):
        """Logs an event that occurs during the battle."""
        print(f"Turn {self.turn_count}: {event}")
        self.log.append(f"Turn {self.turn_count}: {event}")

    def is_game_over(self):
        """Checks if the battle is over."""
        team1_alive = any(axie.current_stats['HP'] > 0 for axie in self.team1)
        team2_alive = any(axie.current_stats['HP'] > 0 for axie in self.team2)
        
        if not team1_alive:
            self.log_event("Team 1 defeated!")
            return True, self.team2
        if not team2_alive:
            self.log_event("Team 2 defeated!")
            return True, self.team1
        return False, None

    def simulate_battle(self, max_turns=20):
        """Simula uma batalha completa entre os times."""
        consecutive_no_actions = 0
        max_consecutive_no_actions = 5
        
        while self.turn_count < max_turns:
            self.turn_count += 1
            self.log_event(f"--- Start of Turn {self.turn_count} ---")

            # 1. Energy Gain
            for axie in self.team1 + self.team2:
                axie.energy += 3

            # 2. Draw Cards
            for axie in self.team1 + self.team2:
                self._draw_cards(axie)
                self.log_event(f"{axie.axie_id} hand: {[c.name for c in axie.hand]}")
                self.log_event(f"{axie.axie_id} energy: {axie.energy}")

            # 3. Determine Turn Order
            all_alive_axies = [a for a in self.team1 + self.team2 if a.current_stats['HP'] > 0]
            all_alive_axies.sort(key=lambda axie: axie.current_stats.get('Speed', 0), reverse=True)
            self.log_event(f"Turn order: {[a.axie_id for a in all_alive_axies]}")

            # 4. Play Cards
            for axie in all_alive_axies:
                if axie.current_stats['HP'] <= 0:
                    continue

                self.log_event(f"Axie {axie.axie_id} ({axie.axie_class}) turn.")
                card_played = False
                for card in axie.hand:
                    card_cost = card.energy_cost
                    if axie.energy >= card_cost:
                        self.log_event(f"Axie {axie.axie_id} plays card: {card.name} (Cost: {card_cost})")
                        axie.energy -= card_cost
                        self._play_card(axie, card)
                        axie.hand.remove(card)
                        axie.discard_pile.append(card)
                        card_played = True
                        break
                if not card_played:
                    self.log_event(f"Axie {axie.axie_id} could not play a card.")

            # 5. Check for Game Over
            game_over, winning_team = self.is_game_over()
            if game_over:
                winner_ids = [a.axie_id for a in winning_team] if winning_team else "None"
                self.log_event(f"Battle ended after {self.turn_count} turns. Winning Team: {winner_ids}")
                return winning_team

            self.log_event(f"--- End of Turn {self.turn_count} ---")

        self.log_event(f"Battle reached max turns ({max_turns}). Draw.")
        return None

    def _draw_cards(self, axie: Axie):
        """Draws cards for a single Axie up to hand limit (6)."""
        hand_limit = 6
        while len(axie.hand) < hand_limit and (axie.deck or axie.discard_pile):
            if not axie.deck:
                self.log_event(f"Axie {axie.axie_id}: Deck empty, shuffling discard pile ({len(axie.discard_pile)} cards).")
                axie.deck = axie.discard_pile.copy()
                random.shuffle(axie.deck)
                axie.discard_pile = []
                if not axie.deck:
                    break
            card_to_draw = axie.deck.pop(0)
            axie.hand.append(card_to_draw)

    def _play_card(self, playing_axie: Axie, card_data: dict):
        """
        Executes the effect of a played card.
        This is a very basic implementation. Card effects are complex!
        """
        card_name = card_data.name
        card_type = card_data.card_type
        card_target = getattr(card_data, 'target', 'Enemy')
        card_damage = card_data.attack

        self.log_event(f"Executing card '{card_name}' from Axie {playing_axie.axie_id} (Type: {card_type}, Target: {card_target}, Damage: {card_damage})")

        # Basic Targeting Logic (Needs refinement for real game)
        target_axies = []
        if card_target == 'Enemy':
            # Target the front-most enemy Axie
            enemy_team = self.team2 if playing_axie in self.team1 else self.team1
            alive_enemies = [a for a in enemy_team if a.current_stats['HP'] > 0]
            if alive_enemies:
                # In Origin, targeting is complex (front-most, back-most, lowest HP, etc.)
                # For simplicity, target the first alive enemy in the list
                target_axies.append(alive_enemies[0])
        elif card_target == 'Ally':
             # Target the front-most ally Axie (excluding self)
             ally_team = self.team1 if playing_axie in self.team1 else self.team2
             alive_allies = [a for a in ally_team if a.current_stats['HP'] > 0 and a != playing_axie]
             if alive_allies:
                 target_axies.append(alive_allies[0])
        elif card_target == 'Self':
             target_axies.append(playing_axie)
        elif card_target == 'All Enemies':
             enemy_team = self.team2 if playing_axie in self.team1 else self.team1
             target_axies = [a for a in enemy_team if a.current_stats['HP'] > 0]
        # Add other targeting types as needed

        # Apply Card Effects (Very basic: only damage for now)
        for target_axie in target_axies:
            if card_damage > 0:
                # Damage calculation needs to consider buffs, debuffs, shields, critical hits, etc.
                # Simple damage application:
                # Aplica dano mínimo garantido para prevenir batalhas infinitas
                actual_damage = max(card_damage, 10)  # Dano mínimo de 10 por ataque
                target_axie.current_stats['HP'] -= actual_damage
                self.log_event(f"Axie {playing_axie.axie_id} dealt {actual_damage} damage to Axie {target_axie.axie_id}. {target_axie.axie_id} HP: {target_axie.current_stats['HP']}")

                if target_axie.current_stats['HP'] <= 0:
                    self.log_event(f"Axie {target_axie.axie_id} was defeated!")
                    # Remove defeated Axie from their team list (important for is_game_over and targeting)
                    if target_axie in self.team1:
                        self.team1.remove(target_axie)
                    elif target_axie in self.team2:
                        self.team2.remove(target_axie)

            # Add logic for other card effects here (healing, buffs, debuffs, drawing cards, etc.)
            # Example: if card_data.get('effect_type') == 'Heal': ...
            # Example: if card_data.get('effect_type') == 'Buff': ...


# Example of how to use the Battle class (can be put in a separate test file or __main__ block)
# if __name__ == "__main__":
#     # Ensure you have game_model.py, parsed_origin_info.json, and Origin/Classes structure
#     # in the directory where you run this script.

#     print("--- Initializing Game Data ---")
#     game_data = GameData()

#     print("\n--- Creating Example Axies ---")
#     # Create two example Axies using the create_axie_from_config helper
#     # You'll need valid part names that exist in your parsed_origin_info.json
#     # and are mapped to cards.

#     # Example Axie 1 (Aquatic) - Pure
#     axie1_config = {
#         'id': 1,
#         'class': 'Aquatic',
#         'parts': [
#             {'name': 'Sleepess', 'type': 'Olho', 'class': 'Aquatic'},
#             {'name': 'Clear', 'type': 'Orelha', 'class': 'Aquatic'},
#             {'name': 'Babylonia', 'type': 'Chifre', 'class': 'Aquatic'},
#             {'name': 'Lam', 'type': 'Boca', 'class': 'Aquatic'},
#             {'name': 'Perch', 'type': 'Costa', 'class': 'Aquatic'},
#             {'name': 'Shrimp', 'type': 'Cauda', 'class': 'Aquatic'},
#         ]
#     }
#     axie1 = create_axie_from_config(axie1_config, game_data)

#     # Example Axie 2 (Beast) - Pure
#     axie2_config = {
#         'id': 2,
#         'class': 'Beast',
#         'parts': [
#             {'name': 'Imp', 'type': 'Chifre', 'class': 'Beast'}, # Assuming these parts exist and have cards
#             {'name': 'Ronin', 'type': 'Cauda', 'class': 'Beast'},
#             {'name': 'Nut Cracker', 'type': 'Boca', 'class': 'Beast'},
#             {'name': 'Nut Cracker', 'type': 'Costa', 'class': 'Beast'},
#             {'name': 'Confused', 'type': 'Olho', 'class': 'Beast'},
#             {'name': 'Ear Breathing', 'type': 'Orelha', 'class': 'Beast'},
#         ]
#     }
#     axie2 = create_axie_from_config(axie2_config, game_data)

#     # Example Axie 3 (Plant) - Pure
#     axie3_config = {
#         'id': 3,
#         'class': 'Plant',
#         'parts': [
#             {'name': 'Serious', 'type': 'Boca', 'class': 'Plant'}, # Assuming these parts exist and have cards
#             {'name': 'Pumpkin', 'type': 'Costa', 'class': 'Plant'},
#             {'name': 'Cactus', 'type': 'Chifre', 'class': 'Plant'},
#             {'name': 'Carrot', 'type': 'Cauda', 'class': 'Plant'},
#             {'name': 'Leaf Bug', 'type': 'Orelha', 'class': 'Plant'},
#             {'name': 'Papi', 'type': 'Olho', 'class': 'Plant'},
#         ]
#     }
#     axie3 = create_axie_from_config(axie3_config, game_data)


#     if axie1 and axie2 and axie3:
#         print("Axie 1:", axie1)
#         print("Axie 2:", axie2)
#         print("Axie 3:", axie3)

#         # Create teams
#         team_a = [axie1, axie3] # Example team with 2 Axies
#         team_b = [axie2] # Example team with 1 Axie

#         print("\n--- Starting Battle ---")
#         battle = Battle(team_a, team_b, game_data)

#         # Run the battle
#         winning_team = battle.run_battle(max_turns=20)

#         if winning_team:
#             print("\nBattle finished. Winning team Axie IDs:", [a.axie_id for a in winning_team])
#         else:
#             print("\nBattle finished with a draw (max turns reached).")

#         print("\n--- Battle Log ---")
#         for event in battle.log:
#             print(event)

#     else:
#         print("\nFailed to create one or more Axies. Check part names and parsed_origin_info.json.")
