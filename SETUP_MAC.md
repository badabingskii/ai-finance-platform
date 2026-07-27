# 🚀 Guia Completo de Setup - MacBook Pro Intel i7

## ⚠️ IMPORTANTE: MetaTrader 5 no macOS

**MetaTrader 5 NÃO funciona nativamente no macOS**. Você tem 3 opções:

### Opção 1: Usar MetaTrader 5 via Parallels/VMware (RECOMENDADO)
```bash
# Se tiver Parallels Desktop ou VMware instalado
# Configure uma VM Windows dentro do Parallels/VMware
# Instale MT5 dentro da VM Windows
# Use as APIs de rede para se conectar
```

### Opção 2: Usar Wine/CrossOver (mais complexo)
```bash
# Instale Wine ou CrossOver
# Instale MT5 via Wine (resultado inconsistente)
```

### Opção 3: Adaptar para API de Broker (RECOMENDADO para Mac puro)
```bash
# Use a API REST do seu broker diretamente
# Exemplo: IQ Option, Binance, ou seu broker tem API?
```

---

## 📦 Instalação das Dependências Python (Mac puro)

### 1️⃣ Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Instalar dependências (SEM MetaTrader5)

```bash
pip install --upgrade pip
pip install anthropic==0.28.0 \
    python-dotenv==1.0.0 \
    requests==2.31.0 \
    pandas==2.0.3 \
    numpy==1.24.3 \
    pytz==2023.3 \
    pydantic==2.0.3
```

### 3️⃣ Verificar instalação

```bash
python -c "import anthropic; print('✅ Anthropic OK')"
python -c "import pandas; print('✅ Pandas OK')"
python -c "import dotenv; print('✅ dotenv OK')"
```

---

## 🔌 Solução para Mac: Adaptar para API do Broker

Se você quer rodar **100% no Mac sem VM**, adapte para usar a **API REST do seu broker** em vez de MetaTrader5:

### Opção A: IQ Option (tem API Python)
```bash
pip install iq-option
```

### Opção B: Binance (tem API pública)
```bash
pip install python-binance
```

### Opção C: Seu Broker (verificar documentação)

---

## 🛠️ Setup Final - Configurar Claude AI

### 1️⃣ Obter chave Claude

1. Acesse https://console.anthropic.com/
2. Crie uma conta (pode usar Google)
3. Vá em **API Keys**
4. Clique em **Create Key**
5. Copie a chave gerada

### 2️⃣ Configurar .env

```bash
cp .env.example .env
```

Edite `.env`:

```env
# Claude AI (OBRIGATÓRIO)
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx

# MetaTrader 5 (deixe vazio por enquanto)
MT5_LOGIN=
MT5_PASSWORD=
MT5_SERVER=

# Trading Settings
SYMBOL=EURUSD
TIMEFRAME=5
LOT_SIZE=0.1
MAX_POSITIONS=3
```

---

## 💻 Testar Funcionamento (sem MT5)

### Criar arquivo de teste: `test_claude.py`

```python
#!/usr/bin/env python3
from ai_engine.claude_client import ClaudeAnalyzer
from ai_engine.market_analyzer import MarketAnalyzer
import pandas as pd
from core.config import settings

# Testar Claude AI
print("🧪 Testando Claude AI...")

analyzer = ClaudeAnalyzer(api_key=settings.claude_api_key)

# Dados fictícios de teste
test_data = """
SÍMBOLO: EURUSD

ÚLTIMOS 10 CANDLES:
2024-01-15 10:00  O: 1.1020  H: 1.1050  L: 1.1015  C: 1.1045  V: 1000
2024-01-15 10:05  O: 1.1045  H: 1.1055  L: 1.1040  C: 1.1052  V: 1200
2024-01-15 10:10  O: 1.1052  H: 1.1065  L: 1.1048  C: 1.1062  V: 1500

ESTATÍSTICAS:
- Preço Atual: 1.1062
- SMA20: 1.1040
- SMA50: 1.1020
- RSI: 65
- MACD: 0.0015
"""

result = analyzer.analyze_market(test_data, "EURUSD")
print("\n✅ Resposta Claude:")
print(result['analysis'])
```

Execute:

```bash
python test_claude.py
```

Se aparecer análise técnica, **tudo OK!** ✅

---

## 🎯 Próximos Passos (3 Opções)

### Opção 1: Usar Parallels + MT5
```
1. Instale Parallels Desktop ($100)
2. Configure VM Windows
3. Instale MT5 na VM
4. Use as APIs de rede do script Python
```

### Opção 2: Usar IQ Option (MAIS FÁCIL)
```bash
# Editar main.py para usar IQ Option em vez de MT5
# Substituir mt5_agent por iq_option_agent
```

### Opção 3: Esperar usar em Windows/Linux
```
Deploy em servidor Linux (DigitalOcean, AWS)
```

---

## 🔧 Se decidir usar MetaTrader 5 no Mac via Parallels

### Passo 1: Instalar MT5 na VM Windows
1. Abra Parallels
2. Ative VM Windows
3. Baixe MT5: https://www.metatrader5.com/en/download
4. Instale normalmente

### Passo 2: Conectar Python à MT5 na VM
```python
# Em vez de:
mt5.initialize(path="local")

# Use:
import paramiko  # SSH para a VM
# Conectar na VM e chamar API MT5 remotamente
```

### Passo 3: Usar ODBC/RPC (avançado)
```bash
pip install rpyc
# Rodar servidor Python na VM Windows
# Cliente Python no Mac se conecta via RPC
```

---

## ✅ Checklist de Setup

- [ ] Python 3.8+ instalado (`python3 --version`)
- [ ] Venv criado e ativado (`source venv/bin/activate`)
- [ ] Dependências instaladas (`pip install -r requirements-mac.txt`)
- [ ] Chave Claude obtida em console.anthropic.com
- [ ] `.env` configurado com CLAUDE_API_KEY
- [ ] `test_claude.py` executado com sucesso
- [ ] Decisão tomada: MT5 via VM ou API Broker?

---

## 📚 Referências

- [Anthropic Claude Docs](https://docs.anthropic.com/)
- [MetaTrader 5 - Não suporta macOS nativamente](https://www.metatrader5.com/en/download)
- [Parallels Desktop para Mac](https://www.parallels.com/)
- [IQ Option Python API](https://github.com/iqoptionapi/iqoptionapi)

---

## 🆘 Troubleshooting

### Erro: "CLAUDE_API_KEY not found"
```bash
# Verifique se .env existe e tem a chave
cat .env | grep CLAUDE_API_KEY
```

### Erro: "ModuleNotFoundError: No module named 'anthropic'"
```bash
# Reinstale dependências
pip install --upgrade anthropic
```

### Erro: "No module named 'MetaTrader5'"
```bash
# Esperado no macOS - use uma das 3 opções acima
# Ou instale em Linux/Windows
```

---

**Desenvolvido com ❤️ para traders em Mac**
