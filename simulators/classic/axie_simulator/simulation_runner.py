
import json
from battle_simulator import BattleSimulator, Axie, Card

def load_game_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_generated_teams(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_axie_objects(axie_data, game_data):
    # Pass the entire card dictionary to the Card constructor
    cards = [Card(c) for c in axie_data['cards']]
    return Axie(
        axie_data['id'],
        axie_data['class'],
        axie_data['body_parts_classes'], # Pass body_parts_classes as 'parts'
        cards, # Pass list of Card objects
        game_data
    )

def run_simulations(teams, game_data, num_battles_per_matchup=10):
    results = {}
    num_teams = len(teams)

    # Initialize BattleSimulator once with game_data
    simulator = BattleSimulator(game_data)

    for i in range(num_teams):
        team1_data = teams[i]
        team1_id = f'team_{i}'
        team1_objects = [create_axie_objects(a, game_data) for a in team1_data]
        
        results[team1_id] = {'wins': 0, 'losses': 0, 'draws': 0, 'total_damage_dealt': 0, 'total_damage_taken': 0, 'team_composition': team1_data}

        for j in range(num_teams):
            if i == j: # Don't battle against self
                continue
            
            team2_data = teams[j]
            team2_id = f'team_{j}'
            team2_objects = [create_axie_objects(a, game_data) for a in team2_data]

            for _ in range(num_battles_per_matchup):
                # Pass Axie objects directly to simulate_battle
                winner, damage_dealt_t1, damage_taken_t1 = simulator.simulate_battle(team1_objects, team2_objects)

                if winner == 'Team 1 Wins':
                    results[team1_id]['wins'] += 1
                elif winner == 'Team 2 Wins':
                    results[team1_id]['losses'] += 1
                else:
                    results[team1_id]['draws'] += 1
                
                results[team1_id]['total_damage_dealt'] += damage_dealt_t1
                results[team1_id]['total_damage_taken'] += damage_taken_t1

    return results

def analyze_results(simulation_results):
    team_scores = []
    for team_id, data in simulation_results.items():
        total_battles = data['wins'] + data['losses'] + data['draws']
        win_rate = (data['wins'] / total_battles) * 100 if total_battles > 0 else 0
        
        # Simple scoring: prioritize win rate, then damage dealt, then less damage taken
        score = (win_rate * 100) + (data['total_damage_dealt'] * 0.1) - (data['total_damage_taken'] * 0.05)
        
        team_scores.append({
            'team_id': team_id,
            'wins': data['wins'],
            'losses': data['losses'],
            'draws': data['draws'],
            'win_rate': win_rate,
            'score': score,
            'team_composition': data['team_composition']
        })
    
    # Sort by score in descending order
    team_scores.sort(key=lambda x: x['score'], reverse=True)
    return team_scores

if __name__ == '__main__':
    # Use relative paths to load data from the new structure
    game_data = load_game_data('../../data/classic/parsed/parsed_game_data.json')
    # For now, assume other generated files are in the same directory as the script
    teams = load_generated_teams('generated_teams.json')

    print(f'Iniciando simulações para {len(teams)} equipes...')
    # Limitar o número de equipes para simulação para testes iniciais
    # Simular todas as combinações pode levar muito tempo
    # Para o projeto final, este limite pode ser removido ou ajustado
    teams_to_simulate = teams[:50] # Simular apenas as primeiras 50 equipes para começar

    simulation_results = run_simulations(teams_to_simulate, game_data, num_battles_per_matchup=5)
    print('Simulações concluídas. Analisando resultados...')

    ranked_teams = analyze_results(simulation_results)

    top_10_teams = ranked_teams[:10]

    # Save output files in the same directory as the script
    with open('simulation_results.json', 'w', encoding='utf-8') as f:
        json.dump(ranked_teams, f, indent=4, ensure_ascii=False)
    print('Resultados da simulação salvos em simulation_results.json')

    with open('top_10_teams.json', 'w', encoding='utf-8') as f:
        json.dump(top_10_teams, f, indent=4, ensure_ascii=False)
    print('Top 10 equipes salvas em top_10_teams.json')

    # Gerar relatório de texto
    report_content = "# Relatório de Simulação de Batalhas Axie Infinity\n\n"
    report_content += "## Top 10 Equipes\n\n"
    for i, team in enumerate(top_10_teams):
        report_content += f"### Equipe {i+1} (ID: {team['team_id']})\n"
        report_content += f"- Taxa de Vitórias: {team['win_rate']:.2f}%\n"
        report_content += f"- Pontuação: {team['score']:.2f}\n"
        report_content += "- Composição:\n"
        for axie in team['team_composition']:
            report_content += f"  - Axie ID: {axie['id']}, Classe: {axie['class']}, HP: {axie['attributes']['HP']}, Velocidade: {axie['attributes']['Velocidade']}, Habilidade: {axie['attributes']['Habilidade']}, Moral: {axie['attributes']['Moral']}\n"
            report_content += "    Cartas:\n"
            for card in axie['cards']:
                report_content += f"      - {card['Nome']} (Ataque: {card['Ataque']}, Escudo: {card['Escudo']}, Energia: {card['Energia']})\n"
        report_content += "\n"

    with open('simulation_report.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
    print('Relatório de simulação salvo em simulation_report.md')
