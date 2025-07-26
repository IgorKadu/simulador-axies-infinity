import json
import os

import os
# Define the base directory for data files usando caminho relativo absoluto
DATA_BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'origin')

class Part:
    """Represents an Axie body part."""
    def __init__(self, name, part_type, part_class):
        self.name = name
        self.part_type = part_type # e.g., 'Mouth', 'Horn', 'Cauda', 'Boca'
        self.part_class = part_class # e.g., 'Aquatic', 'Beast'

    def __repr__(self):
        return f"Part(name='{self.name}', type='{self.part_type}', class='{self.part_class}')"

class Card:
    """Represents a card associated with an Axie part."""
    def __init__(self, name, card_type, energy_cost, attack, description):
        self.name = name
        self.card_type = card_type # e.g., 'Attack', 'Skill'
        self.energy_cost = energy_cost
        self.attack = attack
        self.description = description

    def __repr__(self):
        return f"Card(name='{self.name}', type='{self.card_type}', energy_cost={self.energy_cost}, attack={self.attack})"

class GameData:
    """Loads and stores game data from parsed files."""
    def __init__(self, json_path: str):
        """
        Initialize GameData with parsed game information.
        
        Args:
            json_path (str): Path to the parsed JSON file with game data
        """
        self.card_data = {} # Maps card name to card data dictionary
        self.part_data = {} # Maps part name to card name (assuming parsed_origin_info.json provides this link)
        self.axie_base_stats = {} # Base stats per Axie class
        self.part_bonus_stats = {} # Bonus stats per part class
        self.class_part_structure = {} # Structure of parts per class and part type from text files

        self._load_data()

    def _load_data(self):
        """Loads all game data from various sources."""
        print("Loading game data...")

        # Load base stats from the table provided by the user
        self.axie_base_stats = {
            'Aquatic': {'HP': 39, 'Speed': 39, 'Skill': 35, 'Morale': 27},
            'Beast': {'HP': 31, 'Speed': 35, 'Skill': 31, 'Morale': 43},
            'Bird': {'HP': 27, 'Speed': 43, 'Skill': 35, 'Morale': 35},
            'Bug': {'HP': 35, 'Speed': 31, 'Skill': 35, 'Morale': 39},
            'Plant': {'HP': 43, 'Speed': 31, 'Skill': 31, 'Morale': 35},
            'Reptile': {'HP': 39, 'Speed': 35, 'Skill': 31, 'Morale': 35},
            'Dawn': {'HP': 35, 'Speed': 35, 'Skill': 39, 'Morale': 31},
            'Dusk': {'HP': 43, 'Speed': 39, 'Skill': 27, 'Morale': 31},
            'Mech': {'HP': 31, 'Speed': 39, 'Skill': 43, 'Morale': 27},
        }
        print(f"Loaded base stats for {len(self.axie_base_stats)} classes.")

        # Load part bonus stats from the table provided by the user
        # Note: The table only lists bonuses for the main 6 classes.
        # Assuming Dawn, Dusk, Mech parts might not have specific bonuses or inherit from base classes.
        # For now, we'll use the provided data and assume 0 bonus for Dawn/Dusk/Mech parts if not listed.
        self.part_bonus_stats = {
            'Aquatic': {'HP': 1, 'Speed': 3, 'Skill': 0, 'Morale': 0},
            'Beast': {'HP': 0, 'Speed': 1, 'Skill': 0, 'Morale': 3},
            'Bird': {'HP': 0, 'Speed': 3, 'Skill': 0, 'Morale': 1},
            'Bug': {'HP': 1, 'Speed': 0, 'Skill': 0, 'Morale': 3},
            'Plant': {'HP': 3, 'Speed': 0, 'Skill': 0, 'Morale': 1},
            'Reptile': {'HP': 3, 'Speed': 1, 'Skill': 0, 'Morale': 0},
            # Add Dawn, Dusk, Mech with 0 bonus as they weren't in the table
            'Dawn': {'HP': 0, 'Speed': 0, 'Skill': 0, 'Morale': 0},
            'Dusk': {'HP': 0, 'Speed': 0, 'Skill': 0, 'Morale': 0},
            'Mech': {'HP': 0, 'Speed': 0, 'Skill': 0, 'Morale': 0},
        }
        print(f"Loaded part bonus stats for {len(self.part_bonus_stats)} classes.")


        # Load card and part data from JSON (assuming it exists and links parts to cards)
        json_file_path = os.path.join(DATA_BASE_PATH, 'parsed_origin_info.json')
        if os.path.exists(json_file_path):
            try:
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Assuming data is a dictionary with a 'cards' key containing a list of card dictionaries
                    # Each card dictionary is assumed to have 'name' and 'part_name' keys
                    cards_list = data.get('cards', [])
                    self.card_data = {card.get('name'): {
            'name': card.get('name'),
            'cost': card.get('cost', 1),
            'attack': card.get('attack', 0),
            'target': card.get('target', 'Enemy'),
            'type': card.get('type', 'Attack')
        } for card in cards_list if card.get('name')}
                    # Build mapping from part name to card name
                    self.part_data = {card.get('part_name'): card.get('name') for card in cards_list if card.get('part_name') and card.get('name')}
                    print(f"Loaded {len(self.card_data)} cards and {len(self.part_data)} part-to-card mappings from {json_file_path}.")
            except Exception as e:
                print(f"Error loading {json_file_path}: {e}")
                self.card_data = {}
                self.part_data = {}
        else:
            print(f"Warning: JSON data file not found: {json_file_path}. Card and part-to-card data will be empty.")
            self.card_data = {}
            self.part_data = {}


        # Load part structure from text files (Origin/Classes/...)
        self._load_class_part_structure()
        print("Game data loading complete.")


    def _load_class_part_structure(self):
        """Loads the structure of parts per class and part type from text files."""
        classes_dir = os.path.join(DATA_BASE_PATH, 'Origin', 'Classes')
        if not os.path.exists(classes_dir):
            print(f"Warning: Directory not found for class parts structure: {classes_dir}")
            return

        for class_name in os.listdir(classes_dir):
            class_path = os.path.join(classes_dir, class_name)
            # Only process directories
            if os.path.isdir(class_path):
                parts_file = os.path.join(class_path, 'Partes do Corpo.txt')
                if os.path.exists(parts_file):
                    try:
                        self.class_part_structure[class_name] = self._parse_parts_file(parts_file)
                        # print(f"Loaded parts structure for class: {class_name}")
                    except Exception as e:
                         print(f"Error parsing parts file for class {class_name}: {e}")
                         self.class_part_structure[class_name] = {}
                else:
                    # print(f"Warning: Parts file not found for class {class_name}: {parts_file}")
                    pass # It's okay if some class folders don't have this file


    def _parse_parts_file(self, file_path):
        """Parses a single Partes do Corpo.txt file."""
        part_structure = {}
        current_part_type = None
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('//'):
                    continue

                if line.endswith(':'):
                    # This is a part type header (e.g., 'Cauda:')
                    current_part_type = line[:-1].strip() # Remove the colon and any whitespace
                    part_structure[current_part_type] = []
                elif current_part_type is not None:
                    # This is a part name under a header
                    part_name = line.strip()
                    if part_name: # Ensure part name is not empty after stripping
                        part_structure[current_part_type].append(part_name)
                # Lines before the first header are ignored

        return part_structure

    # --- Getter methods ---

    def get_card_data(self, card_name):
        """Gets the full data dictionary for a given card name."""
        return self.card_data.get(card_name)

    def get_part_card_name(self, part_name):
         """Gets the card name associated with a given part name."""
         # This mapping comes from the JSON, assuming it links part_name to card_name
         return self.part_data.get(part_name)

    def get_base_stats(self, axie_class):
        """Gets the base stats for a given Axie class."""
        return self.axie_base_stats.get(axie_class, {})

    def get_parts_by_type_and_class(self, part_type, axie_class):
        """Get parts for specific class and type from class structure"""
        class_parts = self.class_part_structure.get(axie_class, {})
        return {part: {} for part in class_parts.get(part_type, [])}

    def get_parts_by_type(self, part_type):
        """Get all parts of a type across all classes"""
        all_parts = {}
        for class_name, parts in self.class_part_structure.items():
            for part in parts.get(part_type, []):
                all_parts[part] = {}
        return all_parts

    def get_cards_for_part(self, part_name):
        """Get cards associated with a part"""
        card_name = self.part_data.get(part_name)
        if not card_name:
            # Fallback para partes sem cartas mapeadas
            return [Card(
                name="Basic Attack",
                card_type="Attack",
                energy_cost=1,
                attack=10,
                description="Basic attack card"
            )]
        card_data = self.card_data.get(card_name)
        if not card_data:
            return [Card(
                name="Basic Attack",
                card_type="Attack",
                energy_cost=1,
                attack=10,
                description="Basic attack card"
            )]
        return [Card(
            name=card_data['name'],
            card_type=card_data['type'],
            energy_cost=card_data.get('cost', 1),
            attack=card_data.get('attack', 10),
            description=card_data.get('description', '')
        )]

    def get_random_rune_for_class(self, axie_class):
        """Placeholder for rune system"""
        return {"name": f"Basic {axie_class} Rune", "effect": "+1 HP"}

    def get_random_charms_for_parts(self, parts):
        """Placeholder for charm system"""
        return {part_type: {"name": "Basic Charm"} for part_type in parts.keys()}

    def get_part_bonus_stats(self, part_class):
         """Gets the bonus stats provided by a part of a given class."""
         # Bonus depends on the part's class, not the Axie's class
         return self.part_bonus_stats.get(part_class, {}) # Return empty dict if class not found

    def get_class_part_structure(self, axie_class):
        """Gets the structure of parts (types and names) for a given Axie class."""
        return self.class_part_structure.get(axie_class, {}) # Return empty dict if class not found

    def get_all_classes(self):
        """Gets a list of all known Axie classes."""
        return list(self.axie_base_stats.keys())

    def get_parts_for_class_and_type(self, axie_class, part_type):
        """Gets a list of part names for a specific class and part type."""
        class_structure = self.get_class_part_structure(axie_class)
        if class_structure:
            return class_structure.get(part_type, [])
        return []


class Axie:
    """Represents an individual Axie."""
    def __init__(self, axie_id, axie_class, parts_config, hp, speed, skill, morale, game_data: GameData, rune=None, charms=None):
        """
        Initializes an Axie.

        Args:
            axie_id (int or str): The unique ID of the Axie.
            axie_class (str): The main class of the Axie (e.g., 'Aquatic').
            parts_config (list): A list of dictionaries, each describing a part.
                                 Example: [{'name': 'Shrimp', 'type': 'Cauda', 'class': 'Aquatic'}, ...]
            hp (int): Health points
            speed (int): Speed attribute
            skill (int): Skill attribute
            morale (int): Morale attribute
            game_data (GameData): The loaded game data object.
            rune (dict, optional): Rune equipment data
            charms (dict, optional): Charms equipment data
        """
        self.rune = rune
        self.charms = charms or {}
        self.hp = hp
        self.speed = speed
        self.skill = skill
        self.morale = morale
        # Create Part objects from the config
        # Converte dicionários de partes para objetos Part
        self.parts = []
        for p in parts_config:
            if isinstance(p, dict):
                self.parts.append(Part(p['name'], p['type'], p['class']))
            else:
                # Fallback para garantir estrutura correta
                part_name = str(p)
                self.parts.append(Part(part_name, "Generic", "Neutral"))
        self.axie_id = axie_id
        self.axie_class = axie_class
        self.game_data = game_data
        
        # Inicializa atributos de batalha
        self.base_stats = {'HP': hp, 'Speed': speed, 'Skill': skill, 'Morale': morale}
        self.current_stats = self.base_stats.copy()
        self.cards = []

        self._calculate_stats_and_cards()

    def _calculate_stats_and_cards(self):
        """Calculates Axie's stats and loads its cards based on its class and parts."""
        # Start with base stats for the Axie's class
        base_stats = self.game_data.get_base_stats(self.axie_class)
        if not base_stats:
            print(f"Warning: Base stats not found for class: {self.axie_class}. Using default 0 stats.")
            self.base_stats = {'HP': 0, 'Speed': 0, 'Skill': 0, 'Morale': 0}
        else:
             self.base_stats = base_stats.copy()


        # Add bonus stats from each part
        for part in self.parts:
            bonus = self.game_data.get_part_bonus_stats(part.part_class)
            if bonus:
                self.base_stats['HP'] += bonus.get('HP', 0)
                self.base_stats['Speed'] += bonus.get('Speed', 0)
                self.base_stats['Skill'] += bonus.get('Skill', 0)
                self.base_stats['Morale'] += bonus.get('Morale', 0)
            else:
                 print(f"Warning: Part bonus stats not found for part class: {part.part_class} (Part: {part.name}).")


            # Get ALL cards associated with this part (including fallback)
            part_cards = self.game_data.get_cards_for_part(part.name)
            self.cards.extend(part_cards)

        # Initialize current stats to base stats
        self.current_stats = self.base_stats.copy()

    def __repr__(self):
        return f"Axie(ID={self.axie_id}, Class={self.axie_class}, HP={self.current_stats.get('HP', '?')}, Speed={self.current_stats.get('Speed', '?')}, Cards={len(self.cards)})"

    def get_stats(self):
        """Returns the current stats of the Axie."""
        return self.current_stats

    def get_cards(self):
        """Returns the list of card data dictionaries for this Axie."""
        return self.cards

    def get_parts(self):
        """Returns the list of Part objects for this Axie."""
        return self.parts


def create_axie_from_config(axie_config, game_data: GameData):
    """
    Helper function to create an Axie object from a configuration dictionary.

    Args:
        axie_config (dict): A dictionary containing Axie configuration.
                            Example:
                            {
                                'id': 123,
                                'class': 'Aquatic',
                                'parts': [
                                    {'name': 'Shrimp', 'type': 'Cauda', 'class': 'Aquatic'},
                                    {'name': 'Lam', 'type': 'Boca', 'class': 'Aquatic'},
                                    # ... 4 more parts
                                ]
                            }
        game_data (GameData): The loaded game data object.

    Returns:
        Axie: The created Axie object.
    """
    axie_id = axie_config.get('id', 'Unknown')
    axie_class = axie_config.get('class')
    parts_config = axie_config.get('parts', [])

    if not axie_class:
        print(f"Error creating Axie {axie_id}: 'class' is missing in config.")
        return None
    if len(parts_config) != 6:
         print(f"Warning creating Axie {axie_id}: Expected 6 parts, but got {len(parts_config)}.")
         # Continue creation, but the Axie might be incomplete

    # Basic validation for parts config structure
    for i, part in enumerate(parts_config):
        if not all(k in part for k in ['name', 'type', 'class']):
            print(f"Warning creating Axie {axie_id}: Part config at index {i} is missing required keys (name, type, class): {part}")
            # You might want to skip this part or handle the error differently

    return Axie(axie_id, axie_class, parts_config, game_data)
