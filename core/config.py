import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Claude AI
    claude_api_key: str = os.getenv("CLAUDE_API_KEY")
    claude_model: str = "claude-3-5-sonnet-20241022"  # Melhor custo-benefício
    
    # MetaTrader 5
    mt5_login: int = int(os.getenv("MT5_LOGIN", 0))
    mt5_password: str = os.getenv("MT5_PASSWORD", "")
    mt5_server: str = os.getenv("MT5_SERVER", "")
    mt5_path: str = os.getenv("MT5_PATH", "C:/Program Files/MetaTrader 5/terminal64.exe")
    
    # Trading
    symbol: str = os.getenv("SYMBOL", "EURUSD")
    timeframe: int = int(os.getenv("TIMEFRAME", 5))
    lot_size: float = float(os.getenv("LOT_SIZE", 0.1))
    risk_percent: float = float(os.getenv("RISK_PERCENT", 2.0))
    max_positions: int = int(os.getenv("MAX_POSITIONS", 3))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    class Config:
        env_file = ".env"

settings = Settings()
