"""
API Mock para testes do bot
Execute este script para simular uma API de casas de apostas
"""

from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base de dados simulada de casas de apostas
BETTING_HOUSES = {
    'bet365': {
        'name': 'Bet365',
        'domain': 'bet365.com',
        'license': 'Malta Gaming Authority',
        'country': 'Malta',
        'status': 'Ativo',
        'website': 'https://www.bet365.com',
        'founded': '2000'
    },
    'betfair': {
        'name': 'Betfair',
        'domain': 'betfair.com',
        'license': 'UK Gambling Commission',
        'country': 'Reino Unido',
        'status': 'Ativo',
        'website': 'https://www.betfair.com',
        'founded': '1999'
    },
    'sportingbet': {
        'name': 'Sportingbet',
        'domain': 'sportingbet.com',
        'license': 'Isle of Man Gambling Supervision Commission',
        'country': 'Reino Unido',
        'status': 'Ativo',
        'website': 'https://www.sportingbet.com',
        'founded': '1998'
    },
    'betano': {
        'name': 'Betano',
        'domain': 'betano.com',
        'license': 'Malta Gaming Authority',
        'country': 'Malta',
        'status': 'Ativo',
        'website': 'https://www.betano.com',
        'founded': '2018'
    },
    'rivalo': {
        'name': 'Rivalo',
        'domain': 'rivalo.com',
        'license': 'Curacao eGaming',
        'country': 'Curacao',
        'status': 'Ativo',
        'website': 'https://www.rivalo.com',
        'founded': '2012'
    },
    'betway': {
        'name': 'Betway',
        'domain': 'betway.com',
        'license': 'Malta Gaming Authority',
        'country': 'Malta',
        'status': 'Ativo',
        'website': 'https://www.betway.com',
        'founded': '2006'
    },
    'pokerstars': {
        'name': 'PokerStars',
        'domain': 'pokerstars.com',
        'license': 'Isle of Man Gambling Supervision Commission',
        'country': 'Reino Unido',
        'status': 'Ativo',
        'website': 'https://www.pokerstars.com',
        'founded': '2001'
    }
}

@app.route('/betting-houses/<house_name>', methods=['GET'])
def check_betting_house(house_name):
    """Endpoint para verificar uma casa de apostas específica"""
    logger.info(f"Verificando casa de apostas: {house_name}")
    
    # Converter para lowercase para busca
    house_name_lower = house_name.lower()
    
    if house_name_lower in BETTING_HOUSES:
        return jsonify(BETTING_HOUSES[house_name_lower]), 200
    else:
        return jsonify({'error': f'Casa de apostas "{house_name}" não encontrada'}), 404

@app.route('/betting-houses', methods=['GET'])
def list_betting_houses():
    """Endpoint para listar todas as casas de apostas"""
    logger.info("Listando todas as casas de apostas")
    
    houses_list = list(BETTING_HOUSES.values())
    return jsonify(houses_list), 200

@app.route('/betting-houses/search', methods=['GET'])
def search_betting_houses():
    """Endpoint para buscar casas de apostas por termo"""
    query = request.args.get('q', '').lower()
    logger.info(f"Buscando casas de apostas com termo: {query}")
    
    if not query:
        return jsonify({'error': 'Parâmetro "q" é obrigatório'}), 400
    
    # Buscar casas que contenham o termo no nome ou domínio
    results = []
    for house in BETTING_HOUSES.values():
        if (query in house['name'].lower() or 
            query in house['domain'].lower() or
            query in house.get('country', '').lower()):
            results.append(house)
    
    return jsonify(results), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'OK',
        'message': 'API Mock funcionando',
        'total_houses': len(BETTING_HOUSES)
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Endpoint raiz com informações da API"""
    return jsonify({
        'message': 'API Mock - Casas de Apostas',
        'version': '1.0',
        'endpoints': {
            'check_house': '/betting-houses/{house_name}',
            'list_houses': '/betting-houses',
            'search_houses': '/betting-houses/search?q={query}',
            'health': '/health'
        },
        'total_houses': len(BETTING_HOUSES),
        'available_houses': list(BETTING_HOUSES.keys())
    }), 200

if __name__ == '__main__':
    print("🚀 Iniciando API Mock para casas de apostas...")
    print("📍 Acesse: http://localhost:5000")
    print("📋 Endpoints disponíveis:")
    print("   GET /betting-houses/{house_name}")
    print("   GET /betting-houses")
    print("   GET /betting-houses/search?q={query}")
    print("   GET /health")
    print("   GET /")
    print("\n📊 Casas de apostas disponíveis:")
    for house in BETTING_HOUSES.keys():
        print(f"   - {house}")
    print("\n🔧 Configure seu .env com:")
    print("   API_BASE_URL=http://localhost:5000")
    print("\n⏹️  Pressione Ctrl+C para parar")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
