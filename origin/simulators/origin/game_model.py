
import json
import os

# Define o caminho base para os dados do jogo de forma relativa e robusta
# Navega três níveis acima do diretório do script atual para chegar à raiz do projeto
# e então desce para 'origin/data/parsed'
DATA_BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'origin', 'parsed')

class Part:
    """Representa uma parte do corpo de um Axie."""
    def __init__(self, name: str, part_type: str, part_class: str):
        """
        Inicializa um objeto Part.

        Args:
            name (str): O nome da parte (ex: 'Shrimp').
            part_type (str): O tipo da parte (ex: 'Boca', 'Cauda').
            part_class (str): A classe da parte (ex: 'Aquatic', 'Beast').
        """
        self.name = name
        self.part_type = part_type
        self.part_class = part_class

    def __repr__(self):
        """Retorna uma representação em string do objeto Part."""
        return f"Part(name='{self.name}', type='{self.part_type}', class='{self.part_class}')"

class Card:
    """Representa uma carta de habilidade associada a uma parte do corpo de um Axie."""
    def __init__(self, name: str, card_type: str, energy_cost: int, attack: int, description: str):
        """
        Inicializa um objeto Card.

        Args:
            name (str): O nome da carta.
            card_type (str): O tipo da carta (ex: 'Attack', 'Skill').
            energy_cost (int): O custo de energia da carta.
            attack (int): O valor de ataque da carta (se aplicável).
            description (str): A descrição da habilidade da carta.
        """
        self.name = name
        self.card_type = card_type
        self.energy_cost = energy_cost
        self.attack = attack
        self.description = description

    def __repr__(self):
        """Retorna uma representação em string do objeto Card."""
        return f"Card(name='{self.name}', type='{self.card_type}', energy_cost={self.energy_cost}, attack={self.attack})"

class GameData:
    """Carrega, armazena e fornece acesso a todos os dados do jogo Axie Infinity Origin."""
    def __init__(self):
        """
        Inicializa o GameData, carregando todas as informações necessárias de arquivos externos.
        """
        self.card_data = {}             # Mapeia nome da carta -> dados da carta
        self.part_data = {}             # Mapeia nome da parte -> nome da carta
        self.axie_base_stats = {}       # Mapeia classe do Axie -> atributos base
        self.part_bonus_stats = {}      # Mapeia classe da parte -> bônus de atributos
        self.class_part_structure = {}  # Estrutura de partes por classe e tipo

        self._load_data()

    def _load_json_data(self, filename: str) -> dict:
        """
        Função auxiliar para carregar dados de um arquivo JSON.

        Args:
            filename (str): O nome do arquivo JSON a ser carregado (localizado em DATA_BASE_PATH).

        Returns:
            dict: Os dados carregados do arquivo JSON, ou um dicionário vazio se ocorrer um erro.
        """
        filepath = os.path.join(DATA_BASE_PATH, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Successfully loaded data from {filename}.")
                return data
        except FileNotFoundError:
            print(f"[ERROR] Data file not found: {filepath}")
        except json.JSONDecodeError:
            print(f"[ERROR] Failed to decode JSON from {filepath}. Check for syntax errors.")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred while loading {filepath}: {e}")
        return {}

    def _load_data(self):
        """Carrega todos os dados do jogo a partir de arquivos JSON e de texto."""
        print("Loading all game data...")

        # Carrega atributos base e bônus de partes dos arquivos JSON
        self.axie_base_stats = self._load_json_data('axie_base_stats.json')
        self.part_bonus_stats = self._load_json_data('part_bonus_stats.json')
        
        # Carrega dados de cartas e o mapeamento de parte -> carta
        parsed_origin_info = self._load_json_data('parsed_origin_info.json')
        if parsed_origin_info:
            cards_list = parsed_origin_info.get('cards', [])
            self.card_data = {
                card.get('name'): {
                    'name': card.get('name'),
                    'cost': card.get('cost', 1),
                    'attack': card.get('attack', 0),
                    'target': card.get('target', 'Enemy'),
                    'type': card.get('type', 'Attack'),
                    'description': card.get('description', '')
                } for card in cards_list if card.get('name')
            }
            self.part_data = {
                card.get('part_name'): card.get('name') for card in cards_list if card.get('part_name') and card.get('name')
            }
            print(f"Processed {len(self.card_data)} cards and {len(self.part_data)} part-to-card mappings.")

        # Carrega a estrutura de partes de cada classe a partir de arquivos de texto
        self._load_class_part_structure()
        print("Game data loading complete.")

    def _load_class_part_structure(self):
        """Carrega a estrutura de partes por classe a partir de arquivos 'Partes do Corpo.txt'."""
        classes_dir = os.path.join(DATA_BASE_PATH, '..', 'raw', 'classes') # Navega para a pasta 'raw'
        if not os.path.exists(classes_dir):
            print(f"[WARN] Directory not found for class parts structure: {classes_dir}")
            return

        for class_name in os.listdir(classes_dir):
            class_path = os.path.join(classes_dir, class_name)
            if os.path.isdir(class_path):
                parts_file = os.path.join(class_path, 'Partes do Corpo.txt')
                if os.path.exists(parts_file):
                    try:
                        self.class_part_structure[class_name] = self._parse_parts_file(parts_file)
                    except Exception as e:
                         print(f"[ERROR] Failed to parse parts file for class {class_name}: {e}")
                         self.class_part_structure[class_name] = {}

    def _parse_parts_file(self, file_path: str) -> dict:
        """Parseia um arquivo 'Partes do Corpo.txt' para extrair a estrutura de partes."""
        part_structure = {}
        current_part_type = None
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('//'):
                    continue

                if line.endswith(':'):
                    current_part_type = line[:-1].strip()
                    part_structure[current_part_type] = []
                elif current_part_type:
                    part_name = line.strip()
                    if part_name:
                        part_structure[current_part_type].append(part_name)
        return part_structure

    # --- Métodos Getters para acesso seguro aos dados ---

    def get_card_data(self, card_name: str) -> dict:
        """Retorna os dados completos para um nome de carta específico."""
        return self.card_data.get(card_name)

    def get_part_card_name(self, part_name: str) -> str:
        """Retorna o nome da carta associada a uma parte do corpo."""
        return self.part_data.get(part_name)

    def get_base_stats(self, axie_class: str) -> dict:
        """Retorna os atributos base para uma classe de Axie."""
        return self.axie_base_stats.get(axie_class, {})

    def get_part_bonus_stats(self, part_class: str) -> dict:
        """Retorna os bônus de atributos para uma classe de parte."""
        return self.part_bonus_stats.get(part_class, {})

    def get_cards_for_part(self, part_name: str) -> list:
        """Retorna uma lista de objetos Card associados a uma parte do corpo."""
        card_name = self.get_part_card_name(part_name)
        if not card_name:
            # Fornece uma carta básica como fallback se nenhuma carta estiver mapeada
            return [Card(name="Basic Attack", card_type="Attack", energy_cost=1, attack=10, description="Basic attack")]
        
        card_data = self.get_card_data(card_name)
        if not card_data:
             return [Card(name="Basic Attack", card_type="Attack", energy_cost=1, attack=10, description="Basic attack")]

        return [Card(
            name=card_data['name'],
            card_type=card_data.get('type', 'Attack'),
            energy_cost=card_data.get('cost', 1),
            attack=card_data.get('attack', 10),
            description=card_data.get('description', 'No description.')
        )]

    def get_all_classes(self) -> list:
        """Retorna uma lista de todas as classes de Axie conhecidas."""
        return list(self.axie_base_stats.keys())

    def get_parts_for_class_and_type(self, axie_class: str, part_type: str) -> list:
        """Retorna uma lista de nomes de partes para uma classe e tipo específicos."""
        class_structure = self.class_part_structure.get(axie_class, {})
        return class_structure.get(part_type, [])


class Axie:
    """Representa um Axie individual, com seus atributos, partes, cartas e estado de batalha."""
    def __init__(self, axie_id, axie_class, parts_config, game_data: GameData, rune=None, charms=None):
        """
        Inicializa um objeto Axie.

        Args:
            axie_id (any): O ID único do Axie.
            axie_class (str): A classe principal do Axie (ex: 'Aquatic').
            parts_config (list): Lista de dicionários, cada um descrevendo uma parte.
                                 Ex: [{'name': 'Shrimp', 'type': 'Cauda', 'class': 'Aquatic'}, ...]
            game_data (GameData): Objeto GameData com todos os dados do jogo.
            rune (dict, optional): Equipamento de runa. Defaults to None.
            charms (dict, optional): Equipamento de charms. Defaults to None.
        """
        self.axie_id = axie_id
        self.axie_class = axie_class
        self.game_data = game_data
        self.rune = rune
        self.charms = charms or {}
        
        # Converte a configuração de partes em objetos Part
        self.parts = [Part(p['name'], p['type'], p['class']) for p in parts_config if isinstance(p, dict)]
        
        # Inicializa atributos de batalha
        self.base_stats = {}
        self.current_stats = {}
        self.cards = []

        self._calculate_stats_and_cards()

    def _calculate_stats_and_cards(self):
        """Calcula os atributos totais do Axie e carrega suas cartas com base na classe e partes."""
        # Começa com os atributos base da classe do Axie
        self.base_stats = self.game_data.get_base_stats(self.axie_class).copy()
        if not self.base_stats:
            print(f"[WARN] Base stats not found for class: {self.axie_class}. Using default stats.")
            self.base_stats = {'HP': 30, 'Speed': 30, 'Skill': 30, 'Morale': 30} # Default stats

        # Adiciona bônus de atributos de cada parte
        for part in self.parts:
            bonus = self.game_data.get_part_bonus_stats(part.part_class)
            for stat, value in bonus.items():
                self.base_stats[stat] = self.base_stats.get(stat, 0) + value

            # Carrega as cartas associadas a cada parte
            part_cards = self.game_data.get_cards_for_part(part.name)
            self.cards.extend(part_cards)

        # Define os atributos atuais no início da batalha
        self.current_stats = self.base_stats.copy()

    def __repr__(self):
        """Retorna uma representação em string do objeto Axie."""
        hp = self.current_stats.get('HP', 'N/A')
        speed = self.current_stats.get('Speed', 'N/A')
        return f"Axie(ID={self.axie_id}, Class={self.axie_class}, HP={hp}, Speed={speed}, Cards={len(self.cards)})"

    def get_stats(self) -> dict:
        """Retorna os atributos atuais do Axie."""
        return self.current_stats

    def get_cards(self) -> list:
        """Retorna a lista de objetos Card do Axie."""
        return self.cards

    def get_parts(self) -> list:
        """Retorna a lista de objetos Part do Axie."""
        return self.parts


def create_axie_from_config(axie_config: dict, game_data: GameData) -> Axie:
    """
    Função auxiliar para criar um objeto Axie a partir de um dicionário de configuração.

    Args:
        axie_config (dict): Dicionário com a configuração do Axie (id, class, parts).
        game_data (GameData): Objeto GameData com todos os dados do jogo.

    Returns:
        Axie or None: O objeto Axie criado, ou None se a configuração for inválida.
    """
    axie_id = axie_config.get('id', 'Unknown_ID')
    axie_class = axie_config.get('class')
    parts_config = axie_config.get('parts', [])

    if not axie_class:
        print(f"[ERROR] Axie creation failed for ID {axie_id}: 'class' is a required field.")
        return None
    
    # Validação básica da configuração das partes
    if len(parts_config) != 6:
        print(f"[WARN] Axie {axie_id} has {len(parts_config)} parts instead of the expected 6.")

    for i, part in enumerate(parts_config):
        if not isinstance(part, dict) or not all(key in part for key in ['name', 'type', 'class']):
            print(f"[ERROR] Axie {axie_id} has a malformed part config at index {i}: {part}")
            return None # Retorna None se uma parte estiver malformada

    return Axie(axie_id, axie_class, parts_config, game_data)

