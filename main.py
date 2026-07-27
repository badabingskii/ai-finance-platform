#!/usr/bin/env python3
"""
AI Finance Platform - MetaTrader 5 + Claude AI
Robô automatizado para análise e execução de trades
"""

import logging
import time
from datetime import datetime, timedelta
from core.config import settings
from mt5_agent.client import MT5Client
from ai_engine.claude_client import ClaudeAnalyzer
from ai_engine.market_analyzer import MarketAnalyzer

# Configurar logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AITradingBot:
    """Bot de trading automatizado com IA Claude"""
    
    def __init__(self):
        # Clientes
        self.mt5_client = MT5Client(
            login=settings.mt5_login,
            password=settings.mt5_password,
            server=settings.mt5_server,
            path=settings.mt5_path
        )
        
        self.claude = ClaudeAnalyzer(api_key=settings.claude_api_key)
        
        # Estado
        self.is_running = False
        self.last_analysis_time = None
        self.analysis_interval = 300  # 5 minutos entre análises
    
    def start(self):
        """Inicia o bot"""
        logger.info("🚀 Iniciando AI Trading Bot...")
        
        # Conecta ao MT5
        if not self.mt5_client.connect():
            logger.error("❌ Falha ao conectar no MT5")
            return False
        
        self.is_running = True
        logger.info(f"✅ Bot iniciado. Analisando {settings.symbol}...")
        
        # Loop principal
        try:
            while self.is_running:
                self.cycle()
                time.sleep(30)  # Verifica a cada 30 segundos
        except KeyboardInterrupt:
            logger.info("\n⏹️  Bot interrompido pelo usuário")
        finally:
            self.stop()
    
    def cycle(self):
        """Um ciclo de análise e decisão"""
        
        # Verificar se é hora de análise
        if self.last_analysis_time and \
           datetime.now() - self.last_analysis_time < timedelta(seconds=self.analysis_interval):
            return
        
        logger.info(f"\n📊 Ciclo de análise - {datetime.now().strftime('%H:%M:%S')}")
        
        # 1. Obter dados de mercado
        candles = self.mt5_client.get_candles(
            symbol=settings.symbol,
            timeframe=settings.timeframe,
            bars=100
        )
        
        if candles is None or len(candles) == 0:
            logger.warning("Sem dados de mercado disponíveis")
            return
        
        # 2. Preparar análise
        analysis_text = MarketAnalyzer.prepare_analysis_text(candles, settings.symbol)
        
        # 3. Claude analisa
        logger.info("🤖 Claude analisando dados...")
        analysis_result = self.claude.analyze_market(analysis_text, settings.symbol)
        
        if analysis_result['status'] != 'success':
            logger.error(f"Erro na análise: {analysis_result.get('error')}")
            return
        
        # 4. Extrair decisão
        decision_result = self.claude.extract_decision(analysis_result['analysis'])
        
        if decision_result['status'] != 'success':
            logger.warning("Não foi possível extrair decisão de trading")
            logger.info(f"\nAnálise Claude:\n{analysis_result['analysis']}")
            return
        
        decision = decision_result['decision']
        
        # 5. Executar decisão
        self._execute_decision(decision, candles)
        
        self.last_analysis_time = datetime.now()
    
    def _execute_decision(self, decision: dict, candles):
        """Executa decisão de trading"""
        
        recommendation = decision.get('recommendation', 'HOLD').upper()
        confidence = decision.get('confidence', 0)
        
        logger.info(f"\n💡 RECOMENDAÇÃO: {recommendation} (Confiança: {confidence}%)")
        logger.info(f"   Reasoning: {decision.get('reasoning', 'N/A')}")
        
        # Não executar se confiança baixa
        if confidence < 60:
            logger.info("⏭️  Confiança baixa, operação descartada")
            return
        
        # Verificar posições abertas
        positions = self.mt5_client.get_positions(settings.symbol)
        
        if len(positions) >= settings.max_positions:
            logger.warning(f"⚠️  Máximo de posições ({settings.max_positions}) atingido")
            return
        
        # Executar apenas BUY ou SELL com confiança alta
        if recommendation == 'HOLD' or confidence < 60:
            logger.info("Segurando posição...")
            return
        
        # Obter SL e TP
        current_price = candles['close'].iloc[-1]
        sl = decision.get('stop_loss')
        tp = decision.get('take_profit')
        
        # Se não tiver SL/TP da IA, calcular automático
        if not sl or not tp:
            point = 0.0001  # Para EURUSD (4 casas decimais)
            if recommendation == 'BUY':
                sl = sl or (current_price - 50 * point)
                tp = tp or (current_price + 100 * point)
            else:
                sl = sl or (current_price + 50 * point)
                tp = tp or (current_price - 100 * point)
        
        # Enviar ordem
        order_id = self.mt5_client.send_order(
            symbol=settings.symbol,
            order_type=recommendation,
            volume=settings.lot_size,
            price=None,  # Market
            sl=sl,
            tp=tp,
            comment=f"AI-Claude-{confidence}%"
        )
        
        if order_id:
            logger.info(f"✅ ORDEM EXECUTADA!")
            logger.info(f"   Tipo: {recommendation} | Volume: {settings.lot_size} {settings.symbol}")
            logger.info(f"   Preço Entrada: {current_price:.5f}")
            logger.info(f"   Stop Loss: {sl:.5f}")
            logger.info(f"   Take Profit: {tp:.5f}")
    
    def stop(self):
        """Para o bot"""
        logger.info("\n🛑 Encerrando...")
        self.is_running = False
        self.mt5_client.disconnect()
        logger.info("Bot desligado")

def main():
    """Entry point"""
    
    # Validar configuração
    if not settings.claude_api_key:
        logger.error("❌ CLAUDE_API_KEY não configurada em .env")
        return
    
    if not settings.mt5_login or not settings.mt5_password:
        logger.error("❌ MT5_LOGIN ou MT5_PASSWORD não configurados em .env")
        return
    
    # Iniciar bot
    bot = AITradingBot()
    bot.start()

if __name__ == "__main__":
    main()
