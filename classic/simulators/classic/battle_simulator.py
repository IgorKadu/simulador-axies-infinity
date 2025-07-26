
import json
import random

class Axie:
    """Representa um Axie individual com seus atributos, partes, cartas e estado em batalha."""
    def __init__(self, axie_id, axie_class, parts, cards, game_data):
        """
        Inicializa um objeto Axie.

        Args:
            axie_id (int): O ID único do Axie.
            axie_class (str): A classe do Axie (ex: 'Aquatic', 'Beast').
            parts (dict): Um dicionário onde as chaves são nomes das partes do corpo e os valores são suas classes.
            cards (list): Uma lista de objetos Card que o Axie possui.
            game_data (dict): Dados do jogo contendo informações sobre atributos base e bônus de partes.
        """
        self.axie_id = axie_id
        self.axie_class = axie_class
        self.parts = parts  # Dicionário de partes do corpo e suas classes
        self.card_objects = cards  # Lista de objetos Card
        self.game_data = game_data # Dados gerais do jogo

        # Atributos iniciais
        self.hp = 0
        self.speed = 0
        self.skill = 0
        self.morale = 0
        
        # Estado atual em batalha
        self.current_hp = 0
        self.current_shield = 0
        self.status_effects = {} # Dicionário para armazenar efeitos de status

        self._calculate_attributes()

    def _calculate_attributes(self):
        """Calcula os atributos totais do Axie com base na classe e partes do corpo."""
        # Obtém atributos base da classe
        base_attributes = self.game_data["class_base_attributes"].get(self.axie_class, {})
        self.hp = base_attributes.get("HP", 0)
        self.speed = base_attributes.get("Velocidade", 0)
        self.skill = base_attributes.get("Habilidade", 0)
        self.morale = base_attributes.get("Moral", 0)

        # Aplica bônus das partes do corpo com base na classe da parte
        for part_name, part_class in self.parts.items():
            bonus = self.game_data["body_part_bonus_attributes"].get(part_class, {})
            self.hp += bonus.get("HP", 0)
            self.speed += bonus.get("Velocidade", 0)
            self.skill += bonus.get("Habilidade", 0)
            self.morale += bonus.get("Moral", 0)
        
        # Define o HP atual como o HP total no início
        self.current_hp = self.hp

    def take_damage(self, damage):
        """Aplica dano ao Axie, considerando o escudo atual.

        Args:
            damage (float): A quantidade de dano a ser aplicada.

        Returns:
            float: O dano real que atingiu o HP do Axie.
        """
        if self.current_shield >= damage:
            self.current_shield -= damage
            return 0 # Nenhum dano ao HP se o escudo absorver tudo
        else:
            remaining_damage = damage - self.current_shield
            self.current_shield = 0
            self.current_hp -= remaining_damage
            if self.current_hp < 0:
                self.current_hp = 0
            return remaining_damage

    def apply_shield(self, shield_amount):
        """Aplica escudo ao Axie.

        Args:
            shield_amount (float): A quantidade de escudo a ser adicionada.
        """
        self.current_shield += shield_amount

    def is_alive(self):
        """Verifica se o Axie está vivo."""
        return self.current_hp > 0

    def reset_for_battle(self):
        """Reseta o estado do Axie para o início de uma nova batalha."""
        self.current_hp = self.hp
        self.current_shield = 0
        self.status_effects = {}

    def __repr__(self):
        """Retorna uma representação em string do objeto Axie."""
        return f"Axie(ID: {self.axie_id}, Classe: {self.axie_class}, HP: {self.current_hp}/{self.hp}, Velocidade: {self.speed}, Habilidade: {self.skill}, Moral: {self.morale})"

class Card:
    """Representa uma carta de habilidade de um Axie."""
    def __init__(self, card_data):
        """
        Inicializa um objeto Card.

        Args:
            card_data (dict): Um dicionário com os dados da carta.
        """
        self.name = card_data["Nome"]
        self.card_type = card_data["Tipo"]
        self.energy = card_data["Energia"]
        self.attack = card_data["Ataque"]
        self.shield = card_data["Escudo"]
        self.description = card_data["Descricao"]

    def __repr__(self):
        """Retorna uma representação em string do objeto Card."""
        return f"Card(Nome: {self.name}, Ataque: {self.attack}, Escudo: {self.shield}, Energia: {self.energy})"

class BattleSimulator:
    """Simula batalhas entre equipes de Axies."""
    def __init__(self, game_data):
        """
        Inicializa o BattleSimulator.

        Args:
            game_data (dict): Dados do jogo contendo informações como vantagem de classe.
        """
        self.game_data = game_data
        # Definição da vantagem e desvantagem de classes
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
        """Determina a ordem de turno dos Axies com base nos atributos.

        A ordem é determinada por: Maior Velocidade > Menor HP > Maior Habilidade > Maior Moral > Menor ID do Axie.

        Args:
            all_axies (list): Uma lista de objetos Axie na batalha.

        Returns:
            list: Uma lista de objetos Axie ordenados pela iniciativa de turno.
        """
        # Regra de desempate: Velocidade (desc) > HP atual (asc) > Habilidade (desc) > Moral (desc) > ID (asc)
        return sorted(all_axies, key=lambda axie: (axie.speed, -axie.current_hp, axie.skill, axie.morale, -axie.axie_id), reverse=True)

    def simulate_battle(self, team1, team2):
        """Simula uma batalha entre duas equipes de Axies.

        Args:
            team1 (list): Uma lista de objetos Axie representando a Equipe 1.
            team2 (list): Uma lista de objetos Axie representando a Equipe 2.

        Returns:
            tuple: Uma tupla contendo o vencedor ('Team 1 Wins', 'Team 2 Wins', ou 'Draw'),
                   o dano total causado pela Equipe 1, e o dano total sofrido pela Equipe 1.
        """
        # Reseta o estado dos Axies para o início da batalha
        for axie in team1 + team2:
            axie.reset_for_battle()

        turn = 0
        max_turns = 20 # Define um limite máximo de turnos para evitar batalhas infinitas
        total_damage_dealt_by_team1 = 0
        total_damage_taken_by_team1 = 0

        # Loop principal da batalha, continua enquanto houver Axies vivos em ambas as equipes ou até o limite de turnos
        while any(axie.is_alive() for axie in team1) and any(axie.is_alive() for axie in team2) and turn < max_turns:
            turn += 1
            # Obtém todos os Axies vivos na batalha
            all_axies_in_battle = [axie for axie in team1 + team2 if axie.is_alive()]
            # Determina a ordem de turno
            turn_order = self._get_turn_order(all_axies_in_battle)

            # Processa cada Axie na ordem de turno
            for attacker_axie in turn_order:
                # Verifica se o Axie atacante ainda está vivo
                if not attacker_axie.is_alive():
                    continue

                # Determina qual é a equipe do atacante e a equipe alvo
                is_team1_attacker = attacker_axie in team1
                target_team = team2 if is_team1_attacker else team1

                # Obtém alvos vivos na equipe alvo
                alive_targets = [axie for axie in target_team if axie.is_alive()]
                if not alive_targets:
                    continue # A batalha pode ter terminado antes do turno deste Axie

                # Lógica de mira simples: ataca o primeiro Axie vivo na equipe alvo
                target_axie = alive_targets[0] 

                total_attack_damage = 0
                total_shield_gain = 0
                cards_played_count = 0

                # Processa as cartas jogadas pelo Axie atacante
                for card in attacker_axie.card_objects:
                    damage = card.attack
                    shield = card.shield

                    # Conta apenas cartas com dano para o cálculo de bônus de habilidade
                    if damage > 0: 
                        cards_played_count += 1

                    # Bônus de dano/escudo por usar carta da mesma classe
                    if card.card_type == attacker_axie.axie_class: 
                         damage *= 1.10
                         shield *= 1.10

                    # Aplica vantagem/desvantagem de classe
                    attacker_class = attacker_axie.axie_class
                    target_class = target_axie.axie_class

                    if attacker_class in self.class_advantage:
                        if target_class in self.class_advantage[attacker_class]["forte_contra"]:
                            damage *= 1.15 # Vantagem de classe (15% mais dano)
                        elif target_class in self.class_advantage[attacker_class]["fraco_contra"]:
                            damage *= 0.85 # Desvantagem de classe (15% menos dano)

                    total_attack_damage += damage
                    total_shield_gain += shield
                
                # Aplica bônus de dano por combo (mais de uma carta jogada)
                if cards_played_count > 1: 
                    # Fórmula do bônus de habilidade no Classic
                    skill_bonus_multiplier = (1 + (attacker_axie.skill * 0.55 - 12.25) / 100 * 0.985)
                    total_attack_damage *= skill_bonus_multiplier

                # Calcula chance de crítico com base na moral
                critical_chance = 0.01 + (attacker_axie.morale / 1000.0)
                # Aplica crítico se ocorrer
                if random.random() < critical_chance:
                    total_attack_damage *= 2

                # Aplica o escudo ganho antes de receber dano
                attacker_axie.apply_shield(total_shield_gain)
                # Aplica o dano calculado ao Axie alvo e obtém o dano real que passou pelo escudo
                damage_dealt = target_axie.take_damage(total_attack_damage)

                # Registra o dano para o relatório final
                if is_team1_attacker:
                    total_damage_dealt_by_team1 += damage_dealt
                else:
                    total_damage_taken_by_team1 += damage_dealt

        # Determina o vencedor após o fim do loop de turnos
        team1_alive = any(axie.is_alive() for axie in team1)
        team2_alive = any(axie.is_alive() for axie in team2)

        winner = ""
        if team1_alive and not team2_alive:
            winner = "Team 1 Wins"
        elif team2_alive and not team1_alive:
            winner = "Team 2 Wins"
        else:
            # Critério de desempate: soma total de HP dos Axies vivos
            team1_total_hp = sum(axie.current_hp for axie in team1)
            team2_total_hp = sum(axie.current_hp for axie in team2)
            if team1_total_hp > team2_total_hp:
                winner = "Team 1 Wins"
            elif team2_total_hp > team1_total_hp:
                winner = "Team 2 Wins"
            else:
                winner = "Draw" # Empate se o HP total for igual (ou se todos morrerem simultaneamente no último turno)
        
        # Retorna o resultado da batalha
        return winner, total_damage_dealt_by_team1, total_damage_taken_by_team1

if __name__ == '__main__':
    # Esta seção é tipicamente usada para testar o módulo diretamente.
    # Atualmente está vazia, mas pode ser preenchida com exemplos de uso do simulador.
    pass


