from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from game_model import GameData
from team_generator import TeamGenerator
from battle_simulator import BattleSimulator
from simulation_runner import SimulationRunner

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables to store simulation state
simulation_runner = None
last_results = None

@app.route('/api/simulate', methods=['POST'])
def run_simulation():
    global simulation_runner, last_results
    
    try:
        data = request.get_json()
        num_teams_per_composition = data.get('num_teams_per_composition', 2)
        battles_per_matchup = data.get('battles_per_matchup', 5)
        top_n = data.get('top_n', 10)
        
        # Initialize simulation
        game_data = GameData("parsed_origin_info.json")
        simulation_runner = SimulationRunner(game_data)
        
        # Run simulation
        simulation_runner.run_simulations(
            num_teams_per_composition=num_teams_per_composition,
            battles_per_matchup=battles_per_matchup
        )
        
        # Get results
        top_teams = simulation_runner.get_ranked_teams(top_n=top_n)
        
        # Convert to JSON-serializable format
        results = []
        for team_data in top_teams:
            team_result = {
                'team_name': team_data['team_name'],
                'win_rate': team_data['win_rate'],
                'wins': team_data['wins'],
                'losses': team_data['losses'],
                'ties': team_data['ties'],
                'total_battles': team_data['total_battles'],
                'composition': []
            }
            
            for axie in team_data['team_object']:
                axie_data = {
                    'id': axie.axie_id,
                    'class': axie.axie_class,
                    'role': getattr(axie, 'role', 'Mixed'),
                    'hp': axie.hp,
                    'speed': axie.speed,
                    'skill': axie.skill,
                    'morale': axie.morale,
                    'cards': [c.name for p_type, p in axie.parts.items() for c in p.cards]
                }
                team_result['composition'].append(axie_data)
            
            results.append(team_result)
        
        last_results = results
        
        return jsonify({
            'success': True,
            'results': results,
            'total_teams': len(simulation_runner.team_performance),
            'total_battles': sum(data['total_battles'] for data in simulation_runner.team_performance.values())
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/results', methods=['GET'])
def get_results():
    global last_results
    
    if last_results is None:
        return jsonify({
            'success': False,
            'error': 'No simulation results available. Run a simulation first.'
        }), 404
    
    return jsonify({
        'success': True,
        'results': last_results
    })

@app.route('/api/team/<team_id>', methods=['GET'])
def get_team_details(team_id):
    global simulation_runner
    
    if simulation_runner is None:
        return jsonify({
            'success': False,
            'error': 'No simulation data available.'
        }), 404
    
    if team_id not in simulation_runner.team_performance:
        return jsonify({
            'success': False,
            'error': f'Team {team_id} not found.'
        }), 404
    
    team_data = simulation_runner.team_performance[team_id]
    
    result = {
        'team_name': team_id,
        'wins': team_data['wins'],
        'losses': team_data['losses'],
        'ties': team_data['ties'],
        'total_battles': team_data['total_battles'],
        'win_rate': (team_data['wins'] + 0.5 * team_data['ties']) / team_data['total_battles'] if team_data['total_battles'] > 0 else 0,
        'composition': []
    }
    
    for axie in team_data['team_object']:
        axie_data = {
            'id': axie.axie_id,
            'class': axie.axie_class,
            'role': getattr(axie, 'role', 'Mixed'),
            'hp': axie.hp,
            'speed': axie.speed,
            'skill': axie.skill,
            'morale': axie.morale,
            'cards': [c.name for p_type, p in axie.parts.items() for c in p.cards]
        }
        result['composition'].append(axie_data)
    
    return jsonify({
        'success': True,
        'team': result
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'success': True,
        'message': 'Axie Battle Simulator API is running'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

