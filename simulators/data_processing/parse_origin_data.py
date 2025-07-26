import json
import os
import re

def parse_cards_from_skills_file(skills_file_path):
    """
    Parses card information from a skills file.
    Returns a list of cards with their properties.
    """
    cards = []
    
    if not os.path.exists(skills_file_path):
        return cards
    
    try:
        with open(skills_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by card entries (lines starting with "- **")
        card_pattern = r'- \*\*(.*?)\*\*:(.*?)(?=- \*\*|\n## |\Z)'
        matches = re.findall(card_pattern, content, re.DOTALL)
        
        for match in matches:
            card_name = match[0].strip()
            card_content = match[1].strip()
            
            # Extract damage from the first line
            damage_match = re.search(r'(\d+) DMG', card_content)
            damage = int(damage_match.group(1)) if damage_match else 0
            
            # Extract main description (first line after damage)
            lines = card_content.split('\n')
            main_description = lines[0].strip() if lines else ""
            
            # Remove damage from description
            main_description = re.sub(r'\d+ DMG\.?\s*', '', main_description)
            
            card = {
                "name": card_name,
                "damage": damage,
                "description": main_description.strip(),
                "level_2": None
            }
            
            # Check for Level 2 variant
            level_2_match = re.search(r'Level 2: (\d+) DMG\.(.*)', card_content, re.DOTALL)
            if level_2_match:
                level_2_damage = int(level_2_match.group(1))
                level_2_description = level_2_match.group(2).strip()
                card["level_2"] = {
                    "damage": level_2_damage,
                    "description": level_2_description
                }
            
            cards.append(card)
    
    except Exception as e:
        print(f"Erro ao processar arquivo {skills_file_path}: {e}")
    
    return cards

def parse_origin_data(raw_data_path, parsed_data_output_path):
    """
    Parses raw Axie Infinity Origin data from text files and images
    into a structured JSON format.
    """
    print(f"Iniciando o parsing dos dados do Origin de: {raw_data_path}")
    
    parsed_data = {
        "classes": {},
        "parts": {},
        "cards": {},
        "runes": {},
        "charms": {},
        "status_effects": {},
        "instructions": {}
    }

    # Placeholder for parsing logic
    # This will involve reading various text files and potentially
    # extracting metadata from image filenames or accompanying text.

    # Process class parts and their cards
    classes_dir = os.path.join(raw_data_path, "classes")
    if os.path.exists(classes_dir):
        for axie_class in os.listdir(classes_dir):
            class_dir = os.path.join(classes_dir, axie_class)
            if os.path.isdir(class_dir):
                parsed_data["classes"][axie_class] = {}
                parts_dir = os.path.join(class_dir, "parts")
                if os.path.exists(parts_dir):
                    for part_type in os.listdir(parts_dir):
                        part_type_dir = os.path.join(parts_dir, part_type)
                        if os.path.isdir(part_type_dir):
                            skills_file = os.path.join(part_type_dir, "skills")
                            if os.path.exists(skills_file):
                                cards = parse_cards_from_skills_file(skills_file)
                                parsed_data["classes"][axie_class][part_type] = cards
                                print(f"Processadas {len(cards)} cartas para {axie_class} - {part_type}")

    # Save the parsed data to a JSON file
    output_file = os.path.join(parsed_data_output_path, "parsed_origin_info.json")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=4, ensure_ascii=False)
    print(f"Dados processados salvos em: {output_file}")

if __name__ == "__main__":
    # Define paths relative to the project root
    RAW_DATA_PATH = "Axie_Infinity/axie_simulator_Origin/Origin_Info"
    PARSED_DATA_OUTPUT_PATH = "Axie_Infinity/axie_simulator_Origin"
    
    parse_origin_data(RAW_DATA_PATH, PARSED_DATA_OUTPUT_PATH)
