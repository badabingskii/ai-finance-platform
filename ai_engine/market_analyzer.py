import pandas as pd
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class MarketAnalyzer:
    """Análise técnica de dados de mercado"""
    
    @staticmethod
    def prepare_analysis_text(df: pd.DataFrame, symbol: str) -> str:
        """Prepara texto com dados de mercado para Claude"""
        
        if df is None or len(df) == 0:
            return "Sem dados disponíveis"
        
        # Calcula indicadores básicos
        df = MarketAnalyzer._calculate_indicators(df)
        
        # Últimos 10 candles
        recent = df.tail(10).copy()
        
        # Formato legível para Claude
        analysis_text = f"""
SÍMBOLO: {symbol}

ÚLTIMOS 10 CANDLES (TimeFrame: 5 min):
{recent[['time', 'open', 'high', 'low', 'close', 'volume']].to_string()}

ESTATÍSTICAS:
- Preço Atual: {df['close'].iloc[-1]:.5f}
- Máxima (50 candles): {df['high'].tail(50).max():.5f}
- Mínima (50 candles): {df['low'].tail(50).min():.5f}
- Média Móvel 20: {df['sma20'].iloc[-1]:.5f}
- Média Móvel 50: {df['sma50'].iloc[-1]:.5f}
- RSI: {df['rsi'].iloc[-1]:.2f}
- MACD: {df['macd'].iloc[-1]:.5f}
- Signal Line: {df['signal'].iloc[-1]:.5f}
- Volume Médio: {df['volume'].tail(20).mean():.0f}

ANÁLISE TÉCNICA SUGERIDA:
- Preço vs SMA20: {'Acima' if df['close'].iloc[-1] > df['sma20'].iloc[-1] else 'Abaixo'}
- Preço vs SMA50: {'Acima' if df['close'].iloc[-1] > df['sma50'].iloc[-1] else 'Abaixo'}
- Tendência: {'Uptrend' if df['sma20'].iloc[-1] > df['sma50'].iloc[-1] else 'Downtrend'}
- RSI Status: {'Sobrecomprado' if df['rsi'].iloc[-1] > 70 else 'Sobrevendido' if df['rsi'].iloc[-1] < 30 else 'Neutro'}
        """
        
        return analysis_text
    
    @staticmethod
    def _calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """Calcula indicadores técnicos"""
        df = df.copy()
        
        # Média Móvel Simples
        df['sma20'] = df['close'].rolling(window=20).mean()
        df['sma50'] = df['close'].rolling(window=50).mean()
        
        # RSI (Relative Strength Index)
        df['rsi'] = MarketAnalyzer._calculate_rsi(df['close'])
        
        # MACD
        df['ema12'] = df['close'].ewm(span=12).mean()
        df['ema26'] = df['close'].ewm(span=26).mean()
        df['macd'] = df['ema12'] - df['ema26']
        df['signal'] = df['macd'].ewm(span=9).mean()
        
        return df
    
    @staticmethod
    def _calculate_rsi(prices, period=14):
        """Calcula RSI"""
        deltas = prices.diff()
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down if down != 0 else 0
        
        rsi = [100. - 100. / (1. + rs)]
        
        for i in range(period, len(prices)):
            delta = deltas.iloc[i]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
            
            up = (up * (period - 1) + upval) / period
            down = (down * (period - 1) + downval) / period
            rs = up / down if down != 0 else 0
            
            rsi.append(100. - 100. / (1. + rs))
        
        return pd.Series(rsi, index=prices.index)
    
    @staticmethod
    def identify_support_resistance(df: pd.DataFrame, window: int = 20) -> Dict:
        """Identifica suportes e resistências"""
        
        if len(df) < window:
            return {"error": "Dados insuficientes"}
        
        # Últimas N candles
        recent = df.tail(window * 2)
        
        # Suportes (mínimas locais)
        supports = []
        for i in range(1, len(recent) - 1):
            if recent['low'].iloc[i] < recent['low'].iloc[i-1] and \
               recent['low'].iloc[i] < recent['low'].iloc[i+1]:
                supports.append(recent['low'].iloc[i])
        
        # Resistências (máximas locais)
        resistances = []
        for i in range(1, len(recent) - 1):
            if recent['high'].iloc[i] > recent['high'].iloc[i-1] and \
               recent['high'].iloc[i] > recent['high'].iloc[i+1]:
                resistances.append(recent['high'].iloc[i])
        
        return {
            "supports": sorted(supports, reverse=True) if supports else [],
            "resistances": sorted(resistances) if resistances else [],
            "price_current": df['close'].iloc[-1]
        }
