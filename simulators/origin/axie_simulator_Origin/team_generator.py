import random
# Certifique-se que GameData, Axie, AxiePart, Card suportam as novas propriedades (rune, charms)
from .game_model import Axie, Part, Card, GameData

class TeamGenerator:
    def __init__(self, game_data):
        self.game_data = game_data
        self.classes = ["Aquatic", "Beast", "Plant", "Bird", "Bug", "Reptile", "Dusk", "Dawn", "Mech"]
        # --- MODIFICAÇÃO 1: Incluir todas as 6 partes ---
        self.part_types = ["Eyes", "Mouth", "Ears", "Horn", "Back", "Tail"]
        # Assumindo que game_data tem métodos para buscar partes por tipo e classe

    def _determine_axie_role(self, axie_class, cards):
        """Determina o papel do Axie com base na classe e nas cartas"""
        # Lógica simples de determinação de papel
        attack_keywords = ['Gun', 'Bite', 'Spike']
        defense_keywords = ['Shield', 'Bubble']
        
        attack_count = sum(1 for card in cards if any(kw in card.name for kw in attack_keywords))
        defense_count = sum(1 for card in cards if any(kw in card.name for kw in defense_keywords))
        
        if attack_count > defense_count:
            return "Attacker"
        elif defense_count > attack_count:
            return "Tank"
        else:
            # Default baseado na classe
            class_roles = {
                'Aquatic': 'Balanced',
                'Beast': 'Attacker',
                'Plant': 'Tank',
                'Bird': 'Speed',
                'Bug': 'Debuffer',
                'Reptile': 'Defense',
                'Dawn': 'Support',
                'Dusk': 'Attacker',
                'Mech': 'Versatile'
            }
            return class_roles.get(axie_class, 'Balanced')

    def generate_axie_with_role(self, axie_class, axie_id):
        """Gera um Axie da classe especificada com partes aleatórias"""
        if axie_class not in self.classes:
            axie_class = random.choice(self.classes)
        # Usa o ID fornecido
        parts = {}
        selected_cards = []
        # --- MODIFICAÇÃO 3: Obter atributos base da classe ---
        # Assumindo que game_data tem um método get_base_stats(axie_class)
        base_stats = self.game_data.get_base_stats(axie_class)

        total_hp_bonus = 0
        total_speed_bonus = 0
        total_skill_bonus = 0
        total_morale_bonus = 0

        for part_type in self.part_types:
            # --- MODIFICAÇÃO 2: Selecionar uma PARTE específica e obter seus dados ---
            # A lógica de seleção da parte pode ser aleatória inicialmente,
            # ou mais sofisticada para tentar atender ao target_role.
            # Assumindo que game_data tem um método get_parts_by_type_and_class(part_type, axie_class)
            available_parts_for_type = self.game_data.get_parts_by_type_and_class(part_type, axie_class)

            if not available_parts_for_type:
                 # Fallback: se não houver partes específicas para essa classe/tipo,
                 # pegue de qualquer classe (menos realista, mas evita erro)
                 available_parts_for_type = self.game_data.get_parts_by_type(part_type)

            if not available_parts_for_type:
                # Fallback: Cria uma parte genérica
                chosen_part_name = f"Generic {part_type}"
                part_class = axie_class if axie_class in self.classes else "Neutral"
                parts[part_type] = {
                'name': chosen_part_name,
                'type': part_type,
                'class': part_class
            }
                selected_cards.extend(self.game_data.get_cards_for_part(chosen_part_name))
                continue

            # Seleciona um nome de parte aleatório entre os disponíveis
            chosen_part_name = random.choice(list(available_parts_for_type.keys())) # Assumindo que o retorno é um dict {nome_parte: dados_parte}

            # --- Obter dados da parte, cartas e atributos associados ---
            part_data = available_parts_for_type[chosen_part_name] # Dados da parte selecionada
            # Assumindo que game_data tem um método get_cards_for_part(part_name) que retorna uma lista de objetos Card
            part_cards = self.game_data.get_cards_for_part(chosen_part_name)
            # Assumindo que part_data contém um dicionário 'stats' com os bônus
            part_stats = part_data.get('stats', {})

            # Cria o objeto AxiePart com o nome real da parte e suas cartas
            # Assumindo que AxiePart aceita nome, tipo e lista de objetos Card
            parts[part_type] = {
                'name': chosen_part_name,
                'type': part_type,
                'class': chosen_part_name.split()[-1]  # Extrai a classe do nome da parte
            }
            selected_cards.extend(part_cards) # Adiciona as cartas desta parte à lista geral

            # --- MODIFICAÇÃO 3: Acumular bônus de atributos das partes ---
            total_hp_bonus += part_stats.get('hp', 0)
            total_speed_bonus += part_stats.get('speed', 0)
            total_skill_bonus += part_stats.get('skill', 0)
            total_morale_bonus += part_stats.get('morale', 0)

        # --- MODIFICAÇÃO 3: Calcular atributos finais ---
        # Atributos base da classe + bônus das 6 partes
        final_hp = base_stats.get('hp', 0) + total_hp_bonus
        final_speed = base_stats.get('speed', 0) + total_speed_bonus
        final_skill = base_stats.get('skill', 0) + total_skill_bonus
        final_morale = base_stats.get('morale', 0) + total_morale_bonus

        # --- MODIFICAÇÃO 4: Adicionar Runa e Charms (Implementação depende da estrutura de GameData) ---
        # Por enquanto, vamos adicionar placeholders ou lógica simples
        # Assumindo que game_data tem métodos para obter runas/charms
        rune = self.game_data.get_random_rune_for_class(axie_class) if hasattr(self.game_data, 'get_random_rune_for_class') else None
        charms = self.game_data.get_random_charms_for_parts(parts) if hasattr(self.game_data, 'get_random_charms_for_parts') else {}


        # Cria o objeto Axie com os atributos calculados, partes, runa e charms
        # Assumindo que o construtor de Axie foi atualizado para aceitar rune e charms
        axie = Axie(
            axie_id=axie_id,
            axie_class=axie_class,
            parts_config=list(parts.values()),  # Convertendo dicionário para lista de partes
            hp=final_hp,
            speed=final_speed,
            skill=final_skill,
            morale=final_morale,
            game_data=self.game_data,
            rune=rune,
            charms=charms
        )

        # Determina o papel com base nas CARTAS REAIS das partes selecionadas
        axie.role = self._determine_axie_role(axie_class, selected_cards)

        return axie

    def generate_team_by_composition(self, composition):
        """Gera um time com base em uma composição de classes específica"""
        team = []
        used_axie_ids = set()
        
        for class_name in composition:
            axie_id = f"{class_name[:3]}-{random.randint(1000,9999)}"
            while axie_id in used_axie_ids:
                axie_id = f"{class_name[:3]}-{random.randint(1000,9999)}"
            used_axie_ids.add(axie_id)
            
            axie = self.generate_axie_with_role(class_name, axie_id)
            team.append(axie)
        
        return team

    def generate_all_team_compositions(self):
        """Gera todas as combinações válidas de classes para times"""
        base_compositions = [
            ['Aquatic', 'Aquatic', 'Aquatic'],
            ['Beast', 'Beast', 'Beast'],
            ['Plant', 'Plant', 'Plant'],
            ['Bird', 'Bird', 'Bird'],
            ['Bug', 'Bug', 'Bug'],
            ['Reptile', 'Reptile', 'Reptile'],
            ['Dusk', 'Dawn', 'Mech'],
            ['Aquatic', 'Beast', 'Plant'],
            ['Bird', 'Bug', 'Reptile'],
            ['Dusk', 'Dawn', 'Aquatic']
        ]
        return base_compositions

    def generate_teams_for_simulation(self, num_teams_per_composition=5):
        """Gera múltiplos times para simulação com variações de composição"""
        all_compositions = self.generate_all_team_compositions()
        all_teams = []
        
        for composition in all_compositions:
            for _ in range(num_teams_per_composition):
                team = self.generate_team_by_composition(composition)
                all_teams.append(team)
        
        # Adiciona algumas composições aleatórias
        for _ in range(num_teams_per_composition * 2):
            random_composition = [random.choice(self.classes) for _ in range(3)]
            team = self.generate_team_by_composition(random_composition)
            all_teams.append(team)
        
        return all_teams

if __name__ == '__main__':
    # Teste básico do gerador de times
    from game_model import GameData
    game_data = GameData("dummy_path")
    generator = TeamGenerator(game_data)
    
    test_team = generator.generate_team_by_composition(['Aquatic', 'Beast', 'Plant'])
    print("Time de teste gerado:")
    for axie in test_team:
        print(f"- {axie.axie_id} ({axie.axie_class}) | HP: {axie.hp} | Role: {axie.role}")
        print(f"  Partes: {[p.part_name for p in axie.parts.values()]}")
        print(f"  Cartas: {[c.name for p in axie.parts.values() for c in p.cards]}")
