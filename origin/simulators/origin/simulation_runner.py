import random
import json
from .game_model import GameData
from .team_generator import TeamGenerator
from .battle_simulator import BattleSimulator

class SimulationRunner:
    def __init__(self, game_data):
        self.game_data = game_data
        self.team_generator = TeamGenerator(game_data)
        self.battle_simulator = BattleSimulator([], [], game_data) # Inicializa com times vazios temporariamente
        self.team_performance = {}

    def run_simulations(self, num_teams_per_composition=5, battles_per_matchup=10):
        teams = self.team_generator.generate_teams_for_simulation(num_teams_per_composition)
        print(f"Iniciando simulações com {len(teams)} equipes geradas.")

        # Initialize performance tracking for each team
        for i, team in enumerate(teams):
            team_name = f"Team_{i+1}"
            self.team_performance[team_name] = {
                "team_object": team,
                "wins": 0,
                "losses": 0,
                "ties": 0,
                "total_battles": 0
            }

        # Run battles between all unique pairs of teams
        team_names = list(self.team_performance.keys())
        for i in range(len(team_names)):
            for j in range(i + 1, len(team_names)):
                team1_name = team_names[i]
                team2_name = team_names[j]
                team1_obj = self.team_performance[team1_name]["team_object"]
                team2_obj = self.team_performance[team2_name]["team_object"]

                print(f"Simulando batalhas entre {team1_name} e {team2_name}...")
                for _ in range(battles_per_matchup):
                    # Cria cópias independentes para cada batalha
                    import copy
                    team1_copy = copy.deepcopy(team1_obj)
                    team2_copy = copy.deepcopy(team2_obj)
                    battle_simulator = BattleSimulator(team1_copy, team2_copy, self.game_data)
                    winner = battle_simulator.simulate_battle()
                    # Determina o vencedor baseado nos times originais
                    winner_original = team1_obj if winner == team1_copy else team2_obj if winner == team2_copy else None
                    if winner_original == team1_obj:
                        self.team_performance[team1_name]["wins"] += 1
                        self.team_performance[team2_name]["losses"] += 1
                    elif winner_original == team2_obj:
                        self.team_performance[team2_name]["wins"] += 1
                        self.team_performance[team1_name]["losses"] += 1
                    else:
                        self.team_performance[team1_name]["ties"] += 1
                        self.team_performance[team2_name]["ties"] += 1
                    
                    self.team_performance[team1_name]["total_battles"] += 1
                    self.team_performance[team2_name]["total_battles"] += 1

        print("Simulações concluídas.")

    def get_ranked_teams(self, top_n=10):
        # Calculate win rate and rank teams
        ranked_teams = []
        for team_name, data in self.team_performance.items():
            total = data["total_battles"]
            if total > 0:
                win_rate = (data["wins"] + 0.5 * data["ties"]) / total # Consider ties as half-wins
            else:
                win_rate = 0.0
            ranked_teams.append({
                "team_name": team_name,
                "team_object": data["team_object"],
                "wins": data["wins"],
                "losses": data["losses"],
                "ties": data["ties"],
                "total_battles": total,
                "win_rate": win_rate
            })
        
        ranked_teams.sort(key=lambda x: x["win_rate"], reverse=True)
        return ranked_teams[:top_n]

    def generate_report(self, filename="simulation_report.txt", top_n=10):
        ranked_teams = self.get_ranked_teams(top_n)
        with open(filename, "w") as f:
            f.write("Relatório de Simulação de Batalhas Axie Infinity Origin\n")
            f.write("=====================================================\n\n")
            f.write(f"Top {top_n} Equipes:\n")
            for i, team_data in enumerate(ranked_teams):
                f.write(f"\n{i+1}. Equipe: {team_data['team_name']}\n")
                f.write(f"   Taxa de Vitória: {team_data['win_rate']:.2f} (Vitórias: {team_data['wins']}, Derrotas: {team_data['losses']}, Empates: {team_data['ties']})\n")
                f.write("   Composição:\n")
                for axie in team_data["team_object"]:
                    f.write(f"     - {axie.axie_id} (Classe: {axie.axie_class}, Papel: {axie.role})\n")
                    f.write(f"       Cartas: {[c.name for p_type, p in axie.parts.items() for c in p.cards]}\n")
            
            f.write("\n\nDetalhes Completos das Simulações:\n")
            f.write("=====================================\n")
            for team_name, data in self.team_performance.items():
                f.write(f"\nEquipe: {team_name}\n")
                f.write(f"  Vitórias: {data['wins']}\n")
                f.write(f"  Derrotas: {data['losses']}\n")
                f.write(f"  Empates: {data['ties']}\n")
                f.write(f"  Total de Batalhas: {data['total_battles']}\n")
                f.write("  Composição:\n")
                for axie in data["team_object"]:
                    f.write(f"    - {axie.axie_id} (Classe: {axie.axie_class}, Papel: {axie.role})\n")
                    f.write(f"      Cartas: {[c.name for p_type, p in axie.parts.items() for c in p.cards]}\n")

        print(f"Relatório gerado em {filename}")

if __name__ == '__main__':
    # Use relative path to load data from the new structure
    # Path to the parsed data file
    data_path = "simulators/data/origin/parsed_origin_info.json"
    game_data = GameData(data_path)
    runner = SimulationRunner(game_data)
    runner.run_simulations(num_teams_per_composition=2, battles_per_matchup=5) # Increased for more meaningful results
    runner.generate_report(top_n=10)
