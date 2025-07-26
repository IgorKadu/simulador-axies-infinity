
import json
import random

class Axie:
    def __init__(self, axie_id, axie_class, parts, cards, game_data):
        self.axie_id = axie_id
        self.axie_class = axie_class
        self.parts = parts  # Dictionary of body parts and their classes
        self.card_objects = cards  # List of Card objects
        self.game_data = game_data

        self.hp = 0
        self.speed = 0
        self.skill = 0
        self.morale = 0
        self.current_hp = 0
        self.current_shield = 0
        self.status_effects = {}

        self._calculate_attributes()

    def _calculate_attributes(self):
        base_attributes = self.game_data["class_base_attributes"].get(self.axie_class, {})
        self.hp = base_attributes.get("HP", 0)
        self.speed = base_attributes.get("Velocidade", 0)
        self.skill = base_attributes.get("Habilidade", 0)
        self.morale = base_attributes.get("Moral", 0)

        # Apply body part bonuses based on the class of the part
        for part_name, part_class in self.parts.items():
            bonus = self.game_data["body_part_bonus_attributes"].get(part_class, {})
            self.hp += bonus.get("HP", 0)
            self.speed += bonus.get("Velocidade", 0)
            self.skill += bonus.get("Habilidade", 0)
            self.morale += bonus.get("Moral", 0)
        self.current_hp = self.hp

    def take_damage(self, damage):
        if self.current_shield >= damage:
            self.current_shield -= damage
            return 0 # No damage to HP
        else:
            remaining_damage = damage - self.current_shield
            self.current_shield = 0
            self.current_hp -= remaining_damage
            if self.current_hp < 0:
                self.current_hp = 0
            return remaining_damage

    def apply_shield(self, shield_amount):
        self.current_shield += shield_amount

    def is_alive(self):
        return self.current_hp > 0

    def reset_for_battle(self):
        self.current_hp = self.hp
        self.current_shield = 0
        self.status_effects = {}

    def __repr__(self):
        return f"Axie(ID: {self.axie_id}, Classe: {self.axie_class}, HP: {self.current_hp}/{self.hp}, Velocidade: {self.speed}, Habilidade: {self.skill}, Moral: {self.morale})"

class Card:
    def __init__(self, card_data):
        self.name = card_data["Nome"]
        self.card_type = card_data["Tipo"]
        self.energy = card_data["Energia"]
        self.attack = card_data["Ataque"]
        self.shield = card_data["Escudo"]
        self.description = card_data["Descricao"]

    def __repr__(self):
        return f"Card(Nome: {self.name}, Ataque: {self.attack}, Escudo: {self.shield}, Energia: {self.energy})"

class BattleSimulator:
    def __init__(self, game_data):
        self.game_data = game_data
        self.class_advantage = {
            "Aquatic": {"forte_contra": ["Beast", "Bug"], "fraco_contra": ["Plant", "Reptile"]},
            "Beast": {"forte_contra": ["Plant", "Reptile"], "fraco_contra": ["Aquatic", "Bird"]},
            "Bird": {"forte_contra": ["Beast", "Bug"], "fraco_contra": ["Plant", "Reptile"]},
            "Bug": {"forte_contra": ["Plant", "Reptile"], "fraco_contra": ["Aquatic", "Bird"]},
            "Plant": {"forte_contra": ["Aquatic", "Bird"], "fraco_contra": ["Beast", "Bug"]},
            "Reptile": {"forte_contra": ["Aquatic", "Bird"], "fraco_contra": ["Beast", "Bug"]},
            "Dawn": {"forte_contra": [], "fraco_contra": []},
            "Dusk": {"forte_contra": [], "fraco_contra": []},
            "Mech": {"forte_contra": [], "fraco_contra": []}
        }

    def _get_turn_order(self, all_axies):
        # Maior Velocidade > Menor HP > Maior Habilidade > Maior Moral > Menor ID do Axie
        return sorted(all_axies, key=lambda axie: (axie.speed, axie.current_hp, axie.skill, axie.morale, axie.axie_id), reverse=True)

    def simulate_battle(self, team1, team2):
        # Reset axies for a new battle
        for axie in team1 + team2:
            axie.reset_for_battle()

        turn = 0
        max_turns = 20
        total_damage_dealt_by_team1 = 0
        total_damage_taken_by_team1 = 0

        while any(axie.is_alive() for axie in team1) and any(axie.is_alive() for axie in team2) and turn < max_turns:
            turn += 1
            all_axies_in_battle = [axie for axie in team1 + team2 if axie.is_alive()]
            turn_order = self._get_turn_order(all_axies_in_battle)

            for attacker_axie in turn_order:
                if not attacker_axie.is_alive():
                    continue

                is_team1_attacker = attacker_axie in team1
                target_team = team2 if is_team1_attacker else team1

                alive_targets = [axie for axie in target_team if axie.is_alive()]
                if not alive_targets:
                    continue

                target_axie = alive_targets[0] # Simple targeting: attack the first alive enemy

                total_attack_damage = 0
                total_shield_gain = 0
                cards_played_count = 0

                for card in attacker_axie.card_objects:
                    damage = card.attack
                    shield = card.shield

                    if damage > 0: 
                        cards_played_count += 1

                    if card.card_type == attacker_axie.axie_class: 
                         damage *= 1.10
                         shield *= 1.10

                    attacker_class = attacker_axie.axie_class
                    target_class = target_axie.axie_class

                    if attacker_class in self.class_advantage:
                        if target_class in self.class_advantage[attacker_class]["forte_contra"]:
                            damage *= 1.15
                        elif target_class in self.class_advantage[attacker_class]["fraco_contra"]:
                            damage *= 0.85

                    total_attack_damage += damage
                    total_shield_gain += shield
                
                if cards_played_count > 1: 
                    skill_bonus_multiplier = (1 + (attacker_axie.skill * 0.55 - 12.25) / 100 * 0.985)
                    total_attack_damage *= skill_bonus_multiplier

                critical_chance = 0.01 + (attacker_axie.morale / 1000.0)
                if random.random() < critical_chance:
                    total_attack_damage *= 2

                attacker_axie.apply_shield(total_shield_gain)
                damage_dealt = target_axie.take_damage(total_attack_damage)

                if is_team1_attacker:
                    total_damage_dealt_by_team1 += damage_dealt
                else:
                    total_damage_taken_by_team1 += damage_dealt

        team1_alive = any(axie.is_alive() for axie in team1)
        team2_alive = any(axie.is_alive() for axie in team2)

        winner = ""
        if team1_alive and not team2_alive:
            winner = "Team 1 Wins"
        elif team2_alive and not team1_alive:
            winner = "Team 2 Wins"
        else:
            team1_total_hp = sum(axie.current_hp for axie in team1)
            team2_total_hp = sum(axie.current_hp for axie in team2)
            if team1_total_hp > team2_total_hp:
                winner = "Team 1 Wins"
            elif team2_total_hp > team1_total_hp:
                winner = "Team 2 Wins"
            else:
                winner = "Draw"
        
        return winner, total_damage_dealt_by_team1, total_damage_taken_by_team1

if __name__ == '__main__':
    # This part is for testing the BattleSimulator directly
    pass


