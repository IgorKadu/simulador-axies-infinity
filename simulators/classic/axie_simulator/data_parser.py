
import re
import json

def parse_classic_info(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {}

    # Mapeamento de nomes de classes do português para o inglês (para consistência)
    class_name_mapping = {
        'Aquático': 'Aquatic',
        'Besta': 'Beast',
        'Pássaro': 'Bird',
        'Inseto': 'Bug',
        'Planta': 'Plant',
        'Réptil': 'Reptile',
        'Amanhecer': 'Dawn',
        'Crepúsculo': 'Dusk',
        'Mech': 'Mech'
    }

    # Helper function to parse attribute tables
    def parse_generic_attribute_table(text, section_title, table_header_regex, num_columns, section_name):
        print(f"[DEBUG] Parsing section: {section_name}")
        attributes = {}
        
        # Find the section first
        section_start_match = re.search(section_title, text, re.DOTALL)
        if not section_start_match:
            print(f"[WARN] Section '{section_name}' not found with title regex: {section_title}")
            return attributes

        section_content = text[section_start_match.end():]
        
        # Now find the table within the section content
        table_regex = table_header_regex + r'\s*\n((?:\|[^\n]*\n)+?)(?=\n## |\Z|\n\n\n)'
        table_match = re.search(table_regex, section_content, re.DOTALL)

        if table_match:
            table_content = table_match.group(1).strip()
            print(f"[DEBUG] Table content found for {section_name}:\n{table_content}\n")
            
            for line in table_content.split('\n'):
                if not line.strip() or not line.strip().startswith('|') or not line.strip().endswith('|'):
                    continue
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) == num_columns: 
                    name_pt = parts[0]
                    name_en = class_name_mapping.get(name_pt, name_pt) # Mapeia ou mantém original
                    try:
                        if section_name == 'Class Base Attributes' or section_name == 'Pure Breed Total Attributes':
                            attributes[name_en] = {
                                'HP': int(parts[1]),
                                'Velocidade': int(parts[2]),
                                'Habilidade': int(parts[3]),
                                'Moral': int(parts[4])
                            }
                        elif section_name == 'Body Part Bonus Attributes':
                            attributes[name_en] = {
                                'HP': int(parts[1].replace('+', '')),
                                'Velocidade': int(parts[2].replace('+', '')),
                                'Habilidade': int(parts[3].replace('+', '')),
                                'Moral': int(parts[4].replace('+', ''))
                            }
                    except ValueError as e:
                        print(f"[ERROR] Erro ao converter para int em {section_name}: {line.strip()} - {e}")
                        continue
                else:
                    print(f"[WARN] Skipping malformed line in {section_name}: {line}")
        else:
            print(f"[WARN] No table block found for {section_name} with regex: {table_header_regex}")
        print(f"[DEBUG] Finished parsing {section_name}. Found {len(attributes)} entries.")
        return attributes

    # Parse Class Base Attributes
    data['class_base_attributes'] = parse_generic_attribute_table(
        content,
        r'## Atributos Base de Cada Classe de Axie',
        r'\| Classe/Atributo \| HP \| Velocidade \| Habilidade \| Moral \|\n\|---+\|---+\|---+\|---+\|---+\|',
        5,
        'Class Base Attributes'
    )

    # Parse Body Part Bonus Attributes
    data['body_part_bonus_attributes'] = parse_generic_attribute_table(
        content,
        r'## Bônus de Atributos de Partes do Corpo do Axie',
        r'\| Parte do Corpo/Atributo \| HP \| Velocidade \| Habilidade \| Moral \|\n\|---+\|---+\|---+\|---+\|---+\|',
        5,
        'Body Part Bonus Attributes'
    )

    # Parse Pure Breed Total Attributes
    data['pure_breed_total_attributes'] = parse_generic_attribute_table(
        content,
        r'## Atributos Totais para Raças Puras',
        r'\| Classe/Atributo \| HP \| Velocidade \| Habilidade \| Moral \|\n\|---+\|---+\|---+\|---+\|---+\|',
        5,
        'Pure Breed Total Attributes'
    )

    # Parse Cards - Adjusted regex to be more robust
    print("[DEBUG] Parsing card sections...")
    card_sections_regex = r'## Cartas da Classe (.*?) \(Classic\)\s*\n(?:\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|\n\|---+\|(?:---+\|){5}\n((?:\|[^\n]*\n)+?))(?=\n## Cartas da Classe|\Z|\n\n\n)'
    card_sections = re.findall(card_sections_regex, content, re.DOTALL)

    data['cards'] = {}
    if not card_sections:
        print("[WARN] No card sections found with the current regex.")
    for class_name_pt, cards_table_content in card_sections:
        class_name_pt = class_name_pt.strip()
        class_name_en = class_name_mapping.get(class_name_pt, class_name_pt) # Mapeia para o nome em inglês
        print(f"[DEBUG] Processing cards for class: {class_name_en}")
        data['cards'][class_name_en] = [] # Usa o nome em inglês como chave

        # Split the captured table content by lines and process each card
        for line in cards_table_content.strip().split('\n'):
            if not line.strip() or line.strip().startswith('|---') or line.strip().startswith('| Nome da Carta'):
                continue
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) == 6: # Ensure it's a data row
                try:
                    card = {
                        'Nome': parts[0],
                        'Tipo': parts[1],
                        'Energia': int(parts[2]),
                        'Ataque': int(parts[3]),
                        'Escudo': int(parts[4]),
                        'Descricao': parts[5]
                    }
                    data['cards'][class_name_en].append(card)
                except ValueError as e:
                    print(f"[ERROR] Erro ao converter para int: {parts[2]} na linha: {line.strip()} - {e}")
                    continue
            else:
                print(f"[WARN] Skipping malformed card line in {class_name_en}: {line}")
    print("[DEBUG] Finished parsing card sections.")
    return data

if __name__ == '__main__':
    parsed_data = parse_classic_info('/home/ubuntu/upload/Classic_Info.md')
    with open('/home/ubuntu/axie_simulator/parsed_game_data.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=4, ensure_ascii=False)
    print("Dados do jogo parseados e salvos em parsed_game_data.json")


