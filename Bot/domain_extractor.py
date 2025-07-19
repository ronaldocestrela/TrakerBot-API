"""
Módulo para extração e processamento de domínios
"""

import re
import logging
import tldextract
from typing import List, Optional, Set
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class DomainExtractor:
    """Classe para extrair e processar domínios de mensagens"""
    
    def __init__(self):
        # Regex para encontrar URLs e domínios
        self.url_patterns = [
            # URLs completas (http/https)
            r'https?://(?:www\.)?([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)',
            # Domínios com www
            r'www\.([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)',
            # Domínios simples (pelo menos 2 partes separadas por ponto)
            r'(?<!\w)([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+)(?!\w)',
        ]
        
        # Lista de TLDs comuns para validação
        self.common_tlds = {
            'com', 'org', 'net', 'edu', 'gov', 'mil', 'int',
            'br', 'co', 'uk', 'de', 'fr', 'it', 'es', 'pt',
            'bet', 'casino', 'games', 'sport', 'sports'
        }
        
        # Palavras que podem indicar casas de apostas
        self.betting_keywords = {
            'bet', 'betting', 'casino', 'poker', 'sport', 'sports',
            'game', 'games', 'win', 'lucky', 'fortune', 'play'
        }
    
    def extract_domain_name(self, url_or_domain: str) -> Optional[str]:
        """
        Extrai o nome principal do domínio
        
        Args:
            url_or_domain: URL ou domínio para processar
            
        Returns:
            Nome do domínio principal (sem subdomínio e TLD)
        """
        try:
            # Limpar a entrada
            clean_input = self._clean_input(url_or_domain)
            
            if not clean_input:
                return None
            
            # Usar tldextract para obter as partes do domínio
            extracted = tldextract.extract(clean_input)
            
            # Retornar o domínio principal
            if extracted.domain:
                domain_name = extracted.domain.lower()
                
                # Validar se é um domínio válido
                if self._is_valid_domain_name(domain_name):
                    return domain_name
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao extrair domínio de '{url_or_domain}': {e}")
            return None
    
    def find_domains_in_message(self, message: str) -> List[str]:
        """
        Encontra todos os domínios válidos em uma mensagem
        
        Args:
            message: Texto da mensagem
            
        Returns:
            Lista de nomes de domínios encontrados
        """
        domains = set()
        
        # Aplicar cada padrão regex
        for pattern in self.url_patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            
            for match in matches:
                domain_name = self.extract_domain_name(match)
                if domain_name:
                    domains.add(domain_name)
        
        # Buscar também por palavras que podem ser nomes de casas de apostas
        betting_domains = self._find_betting_names(message)
        domains.update(betting_domains)
        
        return list(domains)
    
    def _clean_input(self, input_str: str) -> str:
        """
        Limpa e normaliza a entrada
        
        Args:
            input_str: String de entrada
            
        Returns:
            String limpa
        """
        if not input_str:
            return ""
        
        # Remover espaços extras
        clean = input_str.strip()
        
        # Remover protocolos
        if clean.startswith(('http://', 'https://')):
            clean = urlparse(clean).netloc or urlparse(f"http://{clean}").netloc
        
        # Remover paths, parâmetros e fragmentos
        clean = clean.split('/')[0].split('?')[0].split('#')[0]
        
        return clean
    
    def _is_valid_domain_name(self, domain_name: str) -> bool:
        """
        Valida se um nome de domínio é válido
        
        Args:
            domain_name: Nome do domínio
            
        Returns:
            True se válido, False caso contrário
        """
        if not domain_name:
            return False
        
        # Verificar comprimento
        if len(domain_name) < 2 or len(domain_name) > 63:
            return False
        
        # Verificar caracteres válidos
        if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$', domain_name):
            return False
        
        # Não pode começar ou terminar com hífen
        if domain_name.startswith('-') or domain_name.endswith('-'):
            return False
        
        return True
    
    def _find_betting_names(self, message: str) -> Set[str]:
        """
        Busca por nomes de casas de apostas conhecidas na mensagem
        
        Args:
            message: Texto da mensagem
            
        Returns:
            Set de nomes encontrados
        """
        betting_names = set()
        
        # Lista de casas de apostas conhecidas
        known_betting_houses = {
            'bet365', 'betfair', 'betano', 'sportingbet', 'rivalo',
            'betway', 'betwinner', 'parimatch', 'pinnacle', 'william',
            'ladbrokes', 'coral', 'paddy', 'sky', 'bwin', 'unibet',
            'poker', 'pokerstars', 'partypoker', 'betsson', 'netbet'
        }
        
        # Buscar nomes conhecidos na mensagem
        words = re.findall(r'\b[a-zA-Z0-9]+\b', message.lower())
        
        for word in words:
            if word in known_betting_houses:
                betting_names.add(word)
            
            # Verificar se contém palavras-chave de apostas
            for keyword in self.betting_keywords:
                if keyword in word and len(word) > len(keyword):
                    if self._is_valid_domain_name(word):
                        betting_names.add(word)
        
        return betting_names
    
    def get_domain_info(self, url_or_domain: str) -> dict:
        """
        Obtém informações detalhadas sobre um domínio
        
        Args:
            url_or_domain: URL ou domínio
            
        Returns:
            Dicionário com informações do domínio
        """
        try:
            clean_input = self._clean_input(url_or_domain)
            extracted = tldextract.extract(clean_input)
            
            return {
                'original': url_or_domain,
                'clean': clean_input,
                'subdomain': extracted.subdomain,
                'domain': extracted.domain,
                'suffix': extracted.suffix,
                'full_domain': f"{extracted.domain}.{extracted.suffix}" if extracted.domain and extracted.suffix else None,
                'domain_name': extracted.domain.lower() if extracted.domain else None,
                'is_valid': bool(extracted.domain and extracted.suffix)
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter informações do domínio '{url_or_domain}': {e}")
            return {
                'original': url_or_domain,
                'error': str(e),
                'is_valid': False
            }
