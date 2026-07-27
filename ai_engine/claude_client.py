import logging
from anthropic import Anthropic

logger = logging.getLogger(__name__)

class ClaudeAnalyzer:
    """Analisador de mercado usando Claude AI"""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.client = Anthropic()
        self.api_key = api_key
        self.model = model
        self.conversation_history = []
    
    def analyze_market(self, market_data: str, symbol: str = "EURUSD") -> dict:
        """Analisa dados de mercado com Claude"""
        try:
            # Prepara mensagem para Claude
            user_message = f"""
Você é um expert em análise técnica e trading forex. 
Analise os seguintes dados do símbolo {symbol} e forneça uma recomendação de trading.

Dados de Mercado:
{market_data}

Por favor, forneça:
1. **Análise Técnica**: Identifique suportes, resistências, tendências
2. **Sentimento**: Bullish, Bearish ou Neutral?
3. **Recomendação**: BUY, SELL ou HOLD?
4. **Preço Alvo**: Se houver operação recomendada
5. **Stop Loss**: Nível de proteção
6. **Confiança**: 1-100% na recomendação

Formato de resposta: Use linhas separadas e seja conciso.
            """
            
            # Mantém histórico de conversa para contexto
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Chama Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system="""Você é um expert trader de forex com 15 anos de experiência. 
Suas análises são baseadas em:
- Análise técnica (suportes, resistências, tendências, padrões)
- Indicadores (RSI, MACD, Bandas de Bollinger)
- Gestão de risco
- Controle de emoções

Sempre recomende operações com risco/recompensa mínimo de 1:2.""",
                messages=self.conversation_history
            )
            
            assistant_message = response.content[0].text
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            logger.info("✅ Análise Claude concluída")
            
            return {
                "status": "success",
                "analysis": assistant_message,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
        
        except Exception as e:
            logger.error(f"Erro analisando com Claude: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def extract_decision(self, analysis_text: str) -> dict:
        """Extrai decisão de trading da análise Claude"""
        try:
            decision_message = f"""
Com base na análise anterior, extraia e retorne NO FORMATO JSON VÁLIDO:
{{
    "recommendation": "BUY|SELL|HOLD",
    "confidence": (0-100),
    "entry_price": (número ou null),
    "stop_loss": (número ou null),
    "take_profit": (número ou null),
    "reasoning": "breve explicação"
}}

Análise anterior:
{analysis_text}
            """
            
            self.conversation_history.append({
                "role": "user",
                "content": decision_message
            })
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=self.conversation_history
            )
            
            assistant_message = response.content[0].text
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Parse JSON da resposta
            import json
            import re
            
            # Tenta extrair JSON da resposta
            json_match = re.search(r'\{.*\}', assistant_message, re.DOTALL)
            if json_match:
                decision = json.loads(json_match.group())
                return {
                    "status": "success",
                    "decision": decision
                }
            
            return {
                "status": "error",
                "error": "Não consegui extrair decisão no formato JSON"
            }
        
        except Exception as e:
            logger.error(f"Erro extraindo decisão: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def clear_history(self):
        """Limpa histórico de conversa"""
        self.conversation_history = []
