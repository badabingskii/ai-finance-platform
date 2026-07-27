import MetaTrader5 as mt5
import pandas as pd
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class MT5Client:
    """Cliente para integração com MetaTrader 5"""
    
    def __init__(self, login: int, password: str, server: str, path: str):
        self.login = login
        self.password = password
        self.server = server
        self.path = path
        self.connected = False
    
    def connect(self) -> bool:
        """Conecta ao MetaTrader 5"""
        try:
            if not mt5.initialize(login=self.login, password=self.password, 
                                 server=self.server, path=self.path):
                logger.error(f"MT5 init failed: {mt5.last_error()}")
                return False
            
            self.connected = True
            logger.info("✅ Conectado ao MetaTrader 5")
            return True
        except Exception as e:
            logger.error(f"Erro conectando MT5: {e}")
            return False
    
    def disconnect(self):
        """Desconecta do MetaTrader 5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            logger.info("Desconectado do MT5")
    
    def get_candles(self, symbol: str, timeframe: int, bars: int = 100) -> Optional[pd.DataFrame]:
        """Obtém candles (OHLCV) do símbolo"""
        try:
            timeframes = {
                1: mt5.TIMEFRAME_M1,
                5: mt5.TIMEFRAME_M5,
                15: mt5.TIMEFRAME_M15,
                30: mt5.TIMEFRAME_M30,
                60: mt5.TIMEFRAME_H1,
                240: mt5.TIMEFRAME_H4,
                1440: mt5.TIMEFRAME_D1
            }
            
            tf = timeframes.get(timeframe, mt5.TIMEFRAME_M5)
            rates = mt5.copy_rates_from_pos(symbol, tf, 0, bars)
            
            if rates is None:
                logger.warning(f"Sem dados para {symbol} TF{timeframe}")
                return None
            
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df = df[['time', 'open', 'high', 'low', 'close', 'tick_volume', 'real_volume']]
            df.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'real_volume']
            
            return df
        except Exception as e:
            logger.error(f"Erro obtendo candles: {e}")
            return None
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict]:
        """Obtém informações do símbolo"""
        try:
            info = mt5.symbol_info(symbol)
            if info is None:
                return None
            
            return {
                'symbol': info.name,
                'bid': info.bid,
                'ask': info.ask,
                'spread': info.ask - info.bid,
                'digits': info.digits,
                'point': info.point,
                'contract_size': info.trade_contract_size
            }
        except Exception as e:
            logger.error(f"Erro obtendo info do símbolo: {e}")
            return None
    
    def send_order(self, symbol: str, order_type: str, volume: float, 
                   price: Optional[float] = None, sl: Optional[float] = None, 
                   tp: Optional[float] = None, comment: str = "") -> Optional[int]:
        """Envia ordem para MT5
        
        Args:
            order_type: "BUY" ou "SELL"
            volume: tamanho do lote
            price: preço (None = market)
            sl: stop loss
            tp: take profit
        """
        try:
            action = mt5.ORDER_TYPE_BUY if order_type == "BUY" else mt5.ORDER_TYPE_SELL
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": action,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
            }
            
            if price:
                request["price"] = price
            if sl:
                request["sl"] = sl
            if tp:
                request["tp"] = tp
            
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"Ordem falhou: {result.comment}")
                return None
            
            logger.info(f"✅ Ordem enviada: {order_type} {volume} {symbol}")
            return result.order
        except Exception as e:
            logger.error(f"Erro enviando ordem: {e}")
            return None
    
    def get_positions(self, symbol: Optional[str] = None) -> List[Dict]:
        """Obtém posições abertas"""
        try:
            positions = mt5.positions_get(symbol=symbol)
            if positions is None:
                return []
            
            return [
                {
                    'ticket': pos.ticket,
                    'symbol': pos.symbol,
                    'type': 'BUY' if pos.type == 0 else 'SELL',
                    'volume': pos.volume,
                    'open_price': pos.price_open,
                    'current_price': pos.price_current,
                    'profit': pos.profit,
                    'open_time': datetime.fromtimestamp(pos.time)
                }
                for pos in positions
            ]
        except Exception as e:
            logger.error(f"Erro obtendo posições: {e}")
            return []
    
    def close_position(self, ticket: int, symbol: str) -> bool:
        """Fecha posição aberta"""
        try:
            position = mt5.positions_get(ticket=ticket)
            if not position:
                return False
            
            pos = position[0]
            order_type = mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": pos.volume,
                "type": order_type,
                "position": ticket,
                "type_time": mt5.ORDER_TIME_GTC,
            }
            
            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"Erro fechando posição: {result.comment}")
                return False
            
            logger.info(f"✅ Posição {ticket} fechada")
            return True
        except Exception as e:
            logger.error(f"Erro fechando posição: {e}")
            return False
