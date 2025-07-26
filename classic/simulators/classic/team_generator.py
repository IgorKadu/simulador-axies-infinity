
import json
import itertools
import random
import os

def calculate_axie_attributes(axie_class, body_parts_classes, game_data):
    """Calcula os atributos totais de um Axie com base em sua classe, partes do corpo e dados do jogo.

    Args:
        axie_class (str): A classe do Axie (em inglês).
        body_parts_classes (dict): Um dicionário onde as chaves são nomes das partes do corpo
                                   e os valores são as classes dessas partes.
        game_data (dict): Dados do jogo contendo informações sobre atributos base e bônus de partes.

    Returns:
        dict: Um dicionário com os atributos calculados (HP, Velocidade, Habilidade, Moral).
    """
    # Obtém atributos base da classe do Axie
    base_attributes = game_data.get("class_base_attributes", {}).get(axie_class, {})
    hp = base_attributes.get("HP", 0)
    speed = base_attributes.get("Velocidade", 0)
    skill = base_attributes.get("Habilidade", 0)
    morale = base_attributes.get("Moral", 0)

    # Adiciona bônus de atributos de cada parte do corpo
    for part_name, part_class in body_parts_classes.items():
        bonus = game_data.get("body_part_bonus_attributes", {}).get(part_class, {})
        hp += bonus.get("HP", 0)
        speed += bonus.get("Velocidade", 0)
        skill += bonus.get("Habilidade", 0)
        morale += bonus.get("Moral", 0)
        
    return {"HP": hp, "Velocidade": speed, "Habilidade": skill, "Moral": morale}

def generate_axies(game_data, num_axies_per_class=10):
    """Gera uma lista de Axies com atributos e cartas aleatórios com base nos dados do jogo.

    Args:
        game_data (dict): Dados do jogo contendo informações sobre classes, partes do corpo e cartas.
        num_axies_per_class (int): O número de Axies a gerar para cada classe disponível.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa um Axie gerado.
    """
    all_axies = []
    # Obtém as classes de Axies e as classes de partes do corpo disponíveis nos dados do jogo
    classes = list(game_data.get("class_base_attributes", {}).keys())
    body_part_classes_options = list(game_data.get("body_part_bonus_attributes", {}).keys())

    # Itera sobre cada classe para gerar Axies
    for axie_class_en in classes: 
        # Obtém as cartas disponíveis para a classe atual
        available_cards_for_class = game_data.get("cards", {}).get(axie_class_en, []) 
        
        # Pula a classe se não houver cartas disponíveis para ela
        if not available_cards_for_class:
            print(f"[WARN] No cards found for class: {axie_class_en}. Skipping generation for this class.")
            continue

        # Gera o número especificado de Axies para a classe
        for i in range(num_axies_per_class):
            # Define as classes das partes do corpo para o Axie.
            # Simplificado: partes que dão cartas (Chifre, Boca, Costas, Cauda) têm a mesma classe do Axie.
            # Partes que não dão cartas (Orelhas, Olhos) têm uma classe aleatória.
            body_parts_classes = {
                "Orelhas": random.choice(body_part_classes_options) if body_part_classes_options else 'Unknown',
                "Olhos": random.choice(body_part_classes_options) if body_part_classes_options else 'Unknown',
                "Chifre": axie_class_en,
                "Boca": axie_class_en,
                "Costas": axie_class_en,
                "Cauda": axie_class_en,
            }

            # Seleciona 4 cartas para o Axie.
            # Prioriza cartas da própria classe do Axie.
            selected_cards = []
            if len(available_cards_for_class) >= 4:
                # Se houver 4 ou mais cartas da própria classe, seleciona 4 aleatoriamente
                selected_cards = random.sample(available_cards_for_class, 4)
            else:
                # Se não houver 4 cartas da própria classe, adiciona todas as disponíveis
                selected_cards.extend(available_cards_for_class)
                
                # Busca cartas de outras classes para completar as 4
                all_other_cards = []
                for cls_en, cards in game_data.get("cards", {}).items(): 
                    if cls_en != axie_class_en:
                        all_other_cards.extend(cards)
                
                remaining_needed = 4 - len(selected_cards)
                # Se houver cartas de outras classes suficientes para completar
                if len(all_other_cards) >= remaining_needed:
                    selected_cards.extend(random.sample(all_other_cards, remaining_needed))
                else:
                    # Se não houver cartas de outras classes suficientes, adiciona todas as disponíveis de outras classes
                    selected_cards.extend(all_other_cards) 
                    # Se ainda não tiver 4 cartas, pode ser necessário duplicar cartas existentes
                    # Esta situação indica que não há 4 cartas únicas suficientes em todo o conjunto de dados.
                    # Adiciona cartas aleatórias das já selecionadas para atingir 4 cartas.
                    while len(selected_cards) < 4 and selected_cards: 
                         selected_cards.append(random.choice(selected_cards))

            # Garante que a lista final de cartas tenha exatamente 4 elementos.
            # Isso pode resultar em cartas duplicadas se não houver 4 cartas únicas suficientes.
            while len(selected_cards) < 4:
                # Se por algum motivo a selected_cards estiver vazia e ainda precisar de cartas,
                # pode indicar um problema nos dados de entrada ou na lógica anterior.
                # Adiciona um placeholder ou lida com erro de forma mais robusta se necessário.
                 print(f"[WARN] Não foi possível selecionar 4 cartas para o Axie {axie_class_en}_{i}. Completando com placeholders ou cartas duplicadas.")
                 # Para evitar loop infinito em casos extremos com dados ruins, adicione uma carta placeholder
                 if not selected_cards:
                     selected_cards.append({'Nome': 'Placeholder Card', 'Tipo': 'N/A', 'Energia': 0, 'Ataque': 0, 'Escudo': 0, 'Descricao': 'Carta genérica.'})
                 else:
                     selected_cards.append(random.choice(selected_cards)) # Duplica uma carta existente



            # Calcula os atributos finais do Axie com base nas partes do corpo
            attributes = calculate_axie_attributes(axie_class_en, body_parts_classes, game_data)

            # Cria o dicionário representando o Axie gerado
            axie = {
                "id": f"axie_{axie_class_en}_{i}",
                "class": axie_class_en,
                "body_parts_classes": body_parts_classes,
                "cards": selected_cards, # Usa a lista de cartas selecionadas
                "attributes": attributes # Adiciona os atributos calculados
            }
            all_axies.append(axie)
            
    return all_axies

def generate_teams(axies, num_teams=1000):
    """Gera uma lista de equipes combinando Axies gerados.

    Gera um número especificado de equipes, onde cada equipe consiste em 3 Axies únicos
    selecionados a partir da lista de Axies gerados.

    Args:
        axies (list): Uma lista de dicionários, onde cada dicionário representa um Axie gerado.
        num_teams (int): O número desejado de equipes a gerar.

    Returns:
        list: Uma lista de listas, onde cada lista interna representa uma equipe de 3 Axies.
              Retorna uma lista vazia se não houver Axies suficientes para formar equipes.
    """
    all_teams = []
    
    # Verifica se há Axies suficientes para formar pelo menos uma equipe de 3
    if len(axies) < 3:
        print("[WARN] Não há Axies suficientes para formar equipes (necessário pelo menos 3).")
        return []

    # Gera todas as combinações únicas de 3 Axies.
    # NOTA: Para um número muito grande de Axies, generating all combinations might be memory-intensive.
    # Uma abordagem alternativa seria selecionar 3 Axies aleatoriamente repetidamente até obter o número desejado de equipes.
    all_possible_combinations = list(itertools.combinations(axies, 3))
    
    print(f"[DEBUG] Total de combinações possíveis de 3 Axies: {len(all_possible_combinations)}")

    # Seleciona um subconjunto aleatório de combinações se o total for maior que o número desejado de equipes.
    if len(all_possible_combinations) <= num_teams:
        # Se o número de combinações possíveis for menor ou igual ao desejado, usa todas as combinações.
        all_teams = all_possible_combinations
    else:
        # Caso contrário, seleciona aleatoriamente o número desejado de equipes.
        all_teams = random.sample(all_possible_combinations, num_teams)
    
    # Converte as tuplas de combinações em listas para facilitar a serialização JSON e manipulação futura.
    return [[axie for axie in team] for team in all_teams]

if __name__ == "__main__":
    # Bloco principal para executar o gerador de equipes
    
    # Define os caminhos dos arquivos de dados de entrada e saída
    game_data_filepath = 'classic/data/parsed/parsed_game_data.json' # Caminho para os dados do jogo parseados
    generated_axies_filepath = 'classic/simulators/classic/generated_axies.json' # Caminho para salvar os Axies gerados
    generated_teams_filepath = 'classic/simulators/classic/generated_teams.json' # Caminho para salvar as equipes geradas

    # Carrega os dados do jogo
    print(f"Carregando dados do jogo de: {game_data_filepath}")
    game_data = None
    try:
        with open(game_data_filepath, "r", encoding="utf-8") as f:
            game_data = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Arquivo de dados do jogo não encontrado: {game_data_filepath}")
        exit() # Sai do script se os dados do jogo não puderem ser carregados
    except json.JSONDecodeError:
        print(f"[ERROR] Erro ao decodificar o arquivo JSON: {game_data_filepath}. Verifique a sintaxe do JSON.")
        exit() # Sai do script em caso de erro de sintaxe JSON
    except Exception as e:
        print(f"[ERROR] Ocorreu um erro inesperado ao carregar {game_data_filepath}: {e}")
        exit() # Sai do script em caso de outros erros inesperados

    if not game_data:
        print("Dados do jogo não foram carregados com sucesso. Encerrando.")
        exit()

    # Gera os Axies aleatórios
    print("Gerando Axies...")
    # Define quantos Axies gerar por classe (ex: 10 de cada classe)
    num_axies_to_generate_per_class = 10 
    generated_axies = generate_axies(game_data, num_axies_per_class=num_axies_to_generate_per_class)
    print(f"Total de Axies gerados: {len(generated_axies)}")

    # Gera as equipes a partir dos Axies gerados
    print("Gerando equipes...")
    # Define o número desejado de equipes a gerar
    num_teams_to_generate = 1000
    generated_teams = generate_teams(generated_axies, num_teams=num_teams_to_generate)
    print(f"Total de equipes geradas: {len(generated_teams)}")

    # Salva os Axies gerados em um arquivo JSON
    print(f"Salvando Axies gerados em {generated_axies_filepath}")
    try:
        with open(generated_axies_filepath, "w", encoding="utf-8") as f:
            json.dump(generated_axies, f, indent=4, ensure_ascii=False)
        print("Axies gerados salvos com sucesso.")
    except IOError as e:
        print(f"[ERROR] Erro ao escrever no arquivo de Axies gerados {generated_axies_filepath}: {e}")

    # Salva as equipes geradas em um arquivo JSON
    print(f"Salvando equipes geradas em {generated_teams_filepath}")
    try:
        with open(generated_teams_filepath, "w", encoding="utf-8") as f:
            json.dump(generated_teams, f, indent=4, ensure_ascii=False)
        print("Equipes geradas salvas com sucesso.")
    except IOError as e:
        print(f"[ERROR] Erro ao escrever no arquivo de equipes geradas {generated_teams_filepath}: {e}")




