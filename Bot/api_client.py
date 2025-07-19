"""
Módulo para integração com API de casas de apostas
"""

import requests
import logging
from typing import Dict, Optional, Any
from config import API_ENDPOINTS

logger = logging.getLogger(__name__)

class BettingHouseAPI:
    """Cliente para API de casas de apostas"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        # Configurar headers padrão
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'TelegramBot-BettingHouseChecker/1.0'
        })
        
        if self.api_key:
            # Ajuste o header de autorização conforme sua API
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}'
                # ou 'X-API-Key': self.api_key
            })
    
    async def check_betting_house(self, house_name: str) -> Dict[str, Any]:
        """
        Verifica se uma casa de apostas existe na API
        
        Args:
            house_name: Nome da casa de apostas
            
        Returns:
            Dicionário com resultado da verificação
        """
        try:
            endpoint = API_ENDPOINTS['check_betting_house'].format(house_name=house_name)
            url = f"{self.base_url}{endpoint}"
            
            logger.info(f"Consultando API: {url}")
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'found': True,
                    'data': data,
                    'message': f"✅ Casa de apostas '{house_name}' encontrada!",
                    'status_code': 200
                }
            elif response.status_code == 404:
                return {
                    'found': False,
                    'data': None,
                    'message': f"❌ Casa de apostas '{house_name}' não encontrada na base de dados.",
                    'status_code': 404
                }
            else:
                logger.warning(f"Status inesperado da API: {response.status_code}")
                return {
                    'found': False,
                    'data': None,
                    'message': f"⚠️ Erro ao consultar API para '{house_name}'. Status: {response.status_code}",
                    'status_code': response.status_code
                }
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao consultar API para {house_name}")
            return {
                'found': False,
                'data': None,
                'message': f"⏱️ Timeout ao consultar API para '{house_name}'",
                'status_code': None
            }
        except requests.exceptions.ConnectionError:
            logger.error(f"Erro de conexão ao consultar API para {house_name}")
            return {
                'found': False,
                'data': None,
                'message': f"🚫 Erro de conexão ao consultar '{house_name}'",
                'status_code': None
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição para {house_name}: {e}")
            return {
                'found': False,
                'data': None,
                'message': f"🚫 Erro de conexão ao consultar '{house_name}'",
                'status_code': None
            }
        except Exception as e:
            logger.error(f"Erro inesperado ao consultar {house_name}: {e}")
            return {
                'found': False,
                'data': None,
                'message': f"🚫 Erro interno ao consultar '{house_name}'",
                'status_code': None
            }
    
    async def search_betting_houses(self, query: str) -> Dict[str, Any]:
        """
        Busca casas de apostas por nome
        
        Args:
            query: Termo de busca
            
        Returns:
            Dicionário com resultados da busca
        """
        try:
            endpoint = API_ENDPOINTS['search_betting_houses'].format(query=query)
            url = f"{self.base_url}{endpoint}"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'data': data,
                    'count': len(data) if isinstance(data, list) else 0
                }
            else:
                return {
                    'success': False,
                    'data': None,
                    'count': 0,
                    'error': f"Status: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Erro ao buscar casas de apostas: {e}")
            return {
                'success': False,
                'data': None,
                'count': 0,
                'error': str(e)
            }
    
    async def list_all_betting_houses(self) -> Dict[str, Any]:
        """
        Lista todas as casas de apostas disponíveis
        
        Returns:
            Dicionário com lista de casas de apostas
        """
        try:
            endpoint = API_ENDPOINTS['list_betting_houses']
            url = f"{self.base_url}{endpoint}"
            
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'data': data,
                    'count': len(data) if isinstance(data, list) else 0
                }
            else:
                return {
                    'success': False,
                    'data': None,
                    'count': 0,
                    'error': f"Status: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Erro ao listar casas de apostas: {e}")
            return {
                'success': False,
                'data': None,
                'count': 0,
                'error': str(e)
            }
    
    def __del__(self):
        """Cleanup da sessão"""
        if hasattr(self, 'session'):
            self.session.close()
