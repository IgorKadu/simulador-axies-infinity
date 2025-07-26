
import json
import os
from battle_simulator import BattleSimulator, Axie, Card

def load_game_data(filepath):
    """Carrega os dados do jogo a partir de um arquivo JSON.

    Args:
        filepath (str): O caminho para o arquivo JSON com os dados do jogo.

    Returns:
        dict or None: Um dicionário contendo os dados do jogo se o arquivo for carregado com sucesso,
                      ou None se ocorrer um erro (ex: arquivo não encontrado).
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Arquivo de dados do jogo não encontrado: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"[ERROR] Erro ao decodificar o arquivo JSON: {filepath}. Verifique a sintaxe do JSON.")
        return None
    except Exception as e:
        print(f"[ERROR] Ocorreu um erro inesperado ao carregar {filepath}: {e}")
        return None

def load_generated_teams(filepath):
    """Carrega as equipes geradas a partir de um arquivo JSON.

    Args:
        filepath (str): O caminho para o arquivo JSON com as equipes geradas.

    Returns:
        list or None: Uma lista de dicionários representando as equipes se o arquivo for carregado com sucesso,
                      ou None se ocorrer um erro.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Arquivo de equipes geradas não encontrado: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"[ERROR] Erro ao decodificar o arquivo JSON: {filepath}. Verifique a sintaxe do JSON.")
        return None
    except Exception as e:
        print(f"[ERROR] Ocorreu um erro inesperado ao carregar {filepath}: {e}")
        return None

def create_axie_objects(axie_data, game_data):
    """Cria uma lista de objetos Axie a partir dos dados de uma equipe.

    Args:
        axie_data (list): Uma lista de dicionários, onde cada dicionário representa um Axie.
        game_data (dict): Dados do jogo necessários para inicializar os objetos Axie.

    Returns:
        list: Uma lista de objetos Axie criados.
    """
    axie_objects = []
    for axie_info in axie_data:
        # Cria objetos Card para as cartas do Axie
        cards = [Card(c) for c in axie_info.get('cards', [])] # Usa .get para evitar KeyError se 'cards' não existir
        
        # Cria o objeto Axie
        axie = Axie(
            axie_info.get('id'),
            axie_info.get('class'),
            axie_info.get('body_parts_classes', {}), # Usa .get para evitar KeyError
            cards,
            game_data
        )
        axie_objects.append(axie)
    return axie_objects

def run_simulations(teams, game_data, num_battles_per_matchup=10):
    """Executa simulações de batalha entre todas as equipes geradas.

    Simula batalhas entre cada par de equipes geradas um determinado número de vezes
    e registra os resultados.

    Args:
        teams (list): Uma lista de dicionários, onde cada dicionário representa uma equipe
                      e contém uma lista de dicionários de Axies.
        game_data (dict): Dados do jogo necessários para a simulação.
        num_battles_per_matchup (int): O número de batalhas a simular para cada par de equipes.

    Returns:
        dict: Um dicionário onde as chaves são IDs das equipes e os valores são dicionários
              contendo os resultados da simulação para aquela equipe (vitórias, derrotas, etc.).
    """
    results = {}
    num_teams = len(teams)

    # Inicializa o BattleSimulator uma vez com os dados do jogo
    simulator = BattleSimulator(game_data)

    # Itera sobre cada equipe como Equipe 1
    for i in range(num_teams):
        team1_data = teams[i]
        team1_id = f'team_{i}'
        
        # Cria objetos Axie para a Equipe 1
        team1_objects = create_axie_objects(team1_data, game_data)
        
        # Inicializa os resultados para a Equipe 1
        results[team1_id] = {
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'total_damage_dealt': 0, # Dano causado pela Equipe 1
            'total_damage_taken': 0, # Dano sofrido pela Equipe 1
            'team_composition': team1_data # Mantém a composição original da equipe nos resultados
        }

        # Itera sobre cada equipe como Equipe 2 (incluindo a própria equipe 1, que será ignorada)
        for j in range(num_teams):
            if i == j: # Não simula batalhas de uma equipe contra si mesma
                continue
            
            team2_data = teams[j]
            team2_id = f'team_{j}'
            
            # Cria objetos Axie para a Equipe 2
            team2_objects = create_axie_objects(team2_data, game_data)

            # Executa múltiplas batalhas para esta combinação de equipes
            for battle_num in range(num_battles_per_matchup):
                # Chama o simulador de batalha
                winner, damage_dealt_t1, damage_taken_t1 = simulator.simulate_battle(team1_objects, team2_objects)

                # Atualiza os contadores de vitórias, derrotas e empates
                if winner == 'Team 1 Wins':
                    results[team1_id]['wins'] += 1
                elif winner == 'Team 2 Wins':
                    results[team1_id]['losses'] += 1
                else:
                    results[team1_id]['draws'] += 1
                
                # Acumula o dano total causado e sofrido pela Equipe 1
                results[team1_id]['total_damage_dealt'] += damage_dealt_t1
                results[team1_id]['total_damage_taken'] += damage_taken_t1

                # Reseta o estado dos Axies para a próxima batalha (necessário se os objetos são reutilizados)
                # Embora o simulate_battle já resete, garantir aqui pode ser uma camada extra
                for axie in team1_objects + team2_objects:
                     axie.reset_for_battle()

    return results

def analyze_results(simulation_results):
    """Analisa os resultados da simulação e classifica as equipes.

    Calcula a taxa de vitórias e uma pontuação para cada equipe com base nos resultados
    da simulação e retorna uma lista das equipes classificadas.

    Args:
        simulation_results (dict): O dicionário contendo os resultados da simulação por equipe,
                                   gerado pela função run_simulations.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa uma equipe com seus
              resultados calculados (taxa de vitória, pontuação) e a composição original,
              ordenada pela pontuação em ordem decrescente.
    """
    team_scores = []
    # Itera sobre os resultados de cada equipe
    for team_id, data in simulation_results.items():
        total_battles = data['wins'] + data['losses'] + data['draws']
        # Calcula a taxa de vitórias, evitando divisão por zero
        win_rate = (data['wins'] / total_battles) * 100 if total_battles > 0 else 0
        
        # Fórmula de pontuação simples: prioriza taxa de vitória, depois dano causado, minimiza dano sofrido
        score = (win_rate * 100) + (data['total_damage_dealt'] * 0.1) - (data['total_damage_taken'] * 0.05)
        
        # Adiciona os resultados analisados à lista
        team_scores.append({
            'team_id': team_id,
            'wins': data['wins'],
            'losses': data['losses'],
            'draws': data['draws'],
            'win_rate': win_rate,
            'score': score,
            'team_composition': data['team_composition'] # Inclui a composição da equipe
        })
    
    # Classifica as equipes pela pontuação em ordem decrescente
    team_scores.sort(key=lambda x: x['score'], reverse=True)
    return team_scores

if __name__ == '__main__':
    # Bloco principal para executar o runner da simulação
    
    # Define os caminhos dos arquivos de dados de entrada e saída
    game_data_filepath = 'classic/data/parsed/parsed_game_data.json' # Caminho para os dados do jogo parseados
    teams_filepath = 'classic/simulators/classic/generated_teams.json' # Caminho para as equipes geradas
    simulation_results_filepath = 'classic/simulators/classic/simulation_results.json' # Caminho para salvar os resultados completos
    top_10_teams_filepath = 'classic/simulators/classic/top_10_teams.json' # Caminho para salvar o top 10
    report_filepath = 'classic/simulators/classic/simulation_report.md' # Caminho para salvar o relatório em Markdown

    # Carrega os dados do jogo
    game_data = load_game_data(game_data_filepath)
    if not game_data:
        print("Não foi possível carregar os dados do jogo. Encerrando.")
        exit() # Sai do script se os dados do jogo não puderem ser carregados
        
    # Carrega as equipes geradas
    teams = load_generated_teams(teams_filepath)
    if not teams:
        print("Não foi possível carregar as equipes geradas. Encerrando.")
        exit() # Sai do script se as equipes não puderem ser carregadas

    print(f'Iniciando simulações para {len(teams)} equipes...')
    
    # Limita o número de equipes para simulação para testes iniciais ou simulações parciais.
    # Para simular todas as combinações (num_teams * num_teams), remova ou ajuste este limite.
    # Simular N equipes contra todas as outras N equipes pode ser computacionalmente caro (N^2 * num_battles_per_matchup * battle_complexity).
    teams_to_simulate = teams[:50] # Exemplo: Simular apenas as primeiras 50 equipes

    # Executa as simulações de batalha
    print(f"Simulando {len(teams_to_simulate)} equipes contra outras {len(teams)} equipes...")
    simulation_results = run_simulations(teams_to_simulate, game_data, num_battles_per_matchup=5)
    print('Simulações concluídas. Analisando resultados...')

    # Analisa os resultados e classifica as equipes
    ranked_teams = analyze_results(simulation_results)

    # Seleciona as top 10 equipes
    top_10_teams = ranked_teams[:10]

    # Salva os resultados completos da simulação em JSON
    try:
        with open(simulation_results_filepath, 'w', encoding='utf-8') as f:
            json.dump(ranked_teams, f, indent=4, ensure_ascii=False)
        print(f'Resultados completos da simulação salvos em {simulation_results_filepath}')
    except IOError as e:
        print(f"[ERROR] Erro ao escrever no arquivo de resultados da simulação {simulation_results_filepath}: {e}")

    # Salva as top 10 equipes em JSON
    try:
        with open(top_10_teams_filepath, 'w', encoding='utf-8') as f:
            json.dump(top_10_teams, f, indent=4, ensure_ascii=False)
        print(f'Top 10 equipes salvas em {top_10_teams_filepath}')
    except IOError as e:
        print(f"[ERROR] Erro ao escrever no arquivo do top 10 equipes {top_10_teams_filepath}: {e}")

    # Gerar relatório em formato Markdown
    report_content = "# Relatório de Simulação de Batalhas Axie Infinity Classic

"
    report_content += "Este relatório apresenta os resultados da simulação de batalhas entre equipes geradas no Axie Infinity Classic.

"
    report_content += f"Total de Equipes Geradas: {len(teams)}
"
    report_content += f"Equipes Simuladas: {len(teams_to_simulate)}
"
    report_content += f"Número de Batalhas por Confronto: {num_battles_per_matchup}

"
    report_content += "## Top 10 Equipes Classificadas

"
    
    # Adiciona informações sobre as top 10 equipes ao relatório
    for i, team in enumerate(top_10_teams):
        report_content += f"### {i+1}. Equipe ID: {team['team_id']}
"
        report_content += f"- Taxa de Vitórias: {team['win_rate']:.2f}%
"
        report_content += f"- Pontuação (Score): {team['score']:.2f}
"
        report_content += "- Composição da Equipe:
"
        # Detalhes da composição de cada Axie na equipe
        for axie in team['team_composition']:
            # Usa .get para acessar atributos caso a estrutura do JSON mude inesperadamente
            attributes = axie.get('attributes', {})
            report_content += f"  - Axie ID: {axie.get('id', 'N/A')}, Classe: {axie.get('class', 'N/A')}, HP: {attributes.get('HP', 'N/A')}, Velocidade: {attributes.get('Velocidade', 'N/A')}, Habilidade: {attributes.get('Habilidade', 'N/A')}, Moral: {attributes.get('Moral', 'N/A')}
"
            report_content += "    Cartas:
"
            # Detalhes das cartas de cada Axie
            for card in axie.get('cards', []):
                 report_content += f"      - {card.get('Nome','N/A')} (Ataque: {card.get('Ataque','N/A')}, Escudo: {card.get('Escudo','N/A')}, Energia: {card.get('Energia','N/A')})
"
        report_content += "
"

    # Salva o relatório em Markdown
    try:
        with open(report_filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f'Relatório de simulação salvo em {report_filepath}')
    except IOError as e:
        print(f"[ERROR] Erro ao escrever no arquivo de relatório {report_filepath}: {e}")

