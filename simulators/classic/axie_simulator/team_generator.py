
import json
import itertools
import random

def calculate_axie_attributes(axie_class, body_parts_classes, game_data):
    base_attributes = game_data["class_base_attributes"].get(axie_class, {})
    hp = base_attributes.get("HP", 0)
    speed = base_attributes.get("Velocidade", 0)
    skill = base_attributes.get("Habilidade", 0)
    morale = base_attributes.get("Moral", 0)

    for part_name, part_class in body_parts_classes.items():
        bonus = game_data["body_part_bonus_attributes"].get(part_class, {})
        hp += bonus.get("HP", 0)
        speed += bonus.get("Velocidade", 0)
        skill += bonus.get("Habilidade", 0)
        morale += bonus.get("Moral", 0)
    return {"HP": hp, "Velocidade": speed, "Habilidade": skill, "Moral": morale}

def generate_axies(game_data, num_axies_per_class=10):
    all_axies = []
    classes = list(game_data["class_base_attributes"].keys())
    body_part_classes_options = list(game_data["body_part_bonus_attributes"].keys())

    for axie_class_en in classes: # Use as chaves em inglês diretamente
        available_cards_for_class = game_data["cards"].get(axie_class_en, []) # Acessa com a chave em inglês
        
        if not available_cards_for_class:
            print(f"[WARN] No cards found for class: {axie_class_en}")
            continue

        for i in range(num_axies_per_class):
            # Define body parts classes (simplifying to same as axie_class for attribute calculation)
            # For parts that don't give cards (ears, eyes), randomly pick a class
            body_parts_classes = {
                "Orelhas": random.choice(body_part_classes_options),
                "Olhos": random.choice(body_part_classes_options),
                "Chifre": axie_class_en,
                "Boca": axie_class_en,
                "Costas": axie_class_en,
                "Cauda": axie_class_en,
            }

            # Select 4 distinct cards for the Axie
            selected_cards = []
            # Prioritize cards from the axie's class
            if len(available_cards_for_class) >= 4:
                selected_cards = random.sample(available_cards_for_class, 4)
            else:
                selected_cards.extend(available_cards_for_class)
                # If not enough cards from its own class, pick from other classes
                all_other_cards = []
                for cls_en, cards in game_data["cards"].items(): # Itera sobre chaves em inglês
                    if cls_en != axie_class_en:
                        all_other_cards.extend(cards)
                
                remaining_needed = 4 - len(selected_cards)
                if len(all_other_cards) >= remaining_needed:
                    selected_cards.extend(random.sample(all_other_cards, remaining_needed))
                else:
                    selected_cards.extend(all_other_cards) # Add all if not enough
                    # If still not 4, it means there aren't enough unique cards in the entire game data.
                    # This scenario should be rare with real game data.
                    while len(selected_cards) < 4 and all_other_cards: # Added check for all_other_cards to prevent infinite loop if empty
                        selected_cards.append(random.choice(all_other_cards)) # Duplicate if necessary

            # Ensure cards are unique if possible, otherwise allow duplicates if not enough unique cards exist
            unique_cards = []
            seen_card_names = set()
            for card in selected_cards:
                if card["Nome"] not in seen_card_names:
                    unique_cards.append(card)
                    seen_card_names.add(card["Nome"])
            
            # If after trying to get unique cards, we still don't have 4, fill with duplicates
            while len(unique_cards) < 4 and selected_cards: # Added check for selected_cards to prevent infinite loop if empty
                unique_cards.append(random.choice(selected_cards)) # This might add duplicates if original list had them

            # Calculate attributes
            attributes = calculate_axie_attributes(axie_class_en, body_parts_classes, game_data)

            axie = {
                "id": f"axie_{axie_class_en}_{i}",
                "class": axie_class_en,
                "body_parts_classes": body_parts_classes,
                "cards": unique_cards,
                "attributes": attributes
            }
            all_axies.append(axie)
    return all_axies

def generate_teams(axies, num_teams=1000):
    all_teams = []
    if len(axies) < 3:
        print("Não há Axies suficientes para formar equipes.")
        return []

    # Generate unique combinations of 3 axies
    # Using random.sample on itertools.combinations for efficiency if axies list is large
    # and we only need a subset of all possible combinations.
    all_possible_combinations = list(itertools.combinations(axies, 3))
    
    if len(all_possible_combinations) <= num_teams:
        all_teams = all_possible_combinations
    else:
        all_teams = random.sample(all_possible_combinations, num_teams)
    
    # Convert tuples to lists for easier JSON serialization and manipulation
    return [[axie for axie in team] for team in all_teams]

if __name__ == "__main__":
    with open("/home/ubuntu/axie_simulator/parsed_game_data.json", "r", encoding="utf-8") as f:
        game_data = json.load(f)

    print("Gerando Axies...")
    generated_axies = generate_axies(game_data, num_axies_per_class=10)
    print(f"Total de Axies gerados: {len(generated_axies)}")

    print("Gerando equipes...")
    generated_teams = generate_teams(generated_axies, num_teams=1000)
    print(f"Total de equipes geradas: {len(generated_teams)}")

    with open("/home/ubuntu/axie_simulator/generated_axies.json", "w", encoding="utf-8") as f:
        json.dump(generated_axies, f, indent=4, ensure_ascii=False)
    print("Axies gerados salvos em generated_axies.json")

    with open("/home/ubuntu/axie_simulator/generated_teams.json", "w", encoding="utf-8") as f:
        json.dump(generated_teams, f, indent=4, ensure_ascii=False)
    print("Equipes geradas salvas em generated_teams.json")






