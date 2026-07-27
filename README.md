# 🤖 AI Finance Platform - MetaTrader 5 + Claude AI

Robô de trading automatizado que utiliza **Claude AI** para análise técnica em tempo real e execução de trades no **MetaTrader 5**.

## ✨ Características

- 🧠 **Análise com Claude AI** - Análise técnica profissional alimentada por IA
- 📊 **MetaTrader 5 Integration** - Acesso direto a preços reais e execução de orders
- ⚡ **Automação Completa** - Análise → Decisão → Execução em segundos
- 💰 **Gestão de Risco** - Stop Loss e Take Profit automáticos
- 📈 **Histórico de Operações** - Rastreamento de todas as trades
- 🔐 **Seguro** - Limites de posições abertas para controle de risco

## 🛠️ Requisitos

- **Sistema**: macOS, Windows ou Linux
- **Python**: 3.8+
- **MetaTrader 5**: Instalado e conectado a uma conta real/demo
- **API Claude**: Chave da Anthropic (https://console.anthropic.com/)

### Especificações de Hardware

✅ Compatível com MacBook Pro 2019 Intel i7 9ª Gen + 16GB RAM
- Uso leve de CPU (~10-15% durante análise)
- Consumo RAM: ~200-300MB
- Sem requerimentos de GPU

## 📦 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/badabingskii/ai-finance-platform.git
cd ai-finance-platform
```

### 2. Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Editar `.env` com suas credenciais:

```env
# Claude AI
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxx

# MetaTrader 5
MT5_LOGIN=123456789
MT5_PASSWORD=seu_password
MT5_SERVER=seu_broker_server

# Trading (opcional)
SYMBOL=EURUSD
TIMEFRAME=5
LOT_SIZE=0.1
```

## 🚀 Como Usar

### Execução Básica

```bash
python main.py
```

O bot vai:
1. ✅ Conectar ao MetaTrader 5
2. 📊 Obter dados de mercado
3. 🧠 Solicitar análise ao Claude
4. 💡 Extrair recomendação (BUY/SELL/HOLD)
5. 📈 Executar ordem (se confiança > 60%)
6. ⏰ Repetir a cada 5 minutos

### Saída Esperada

```
2024-01-15 10:30:45 - __main__ - INFO - 🚀 Iniciando AI Trading Bot...
2024-01-15 10:30:46 - mt5_agent.client - INFO - ✅ Conectado ao MetaTrader 5
2024-01-15 10:30:46 - __main__ - INFO - ✅ Bot iniciado. Analisando EURUSD...

2024-01-15 10:35:00 - __main__ - INFO - 📊 Ciclo de análise - 10:35:00
2024-01-15 10:35:01 - __main__ - INFO - 🤖 Claude analisando dados...
2024-01-15 10:35:05 - __main__ - INFO - 
💡 RECOMENDAÇÃO: BUY (Confiança: 75%)
   Reasoning: Suporte testado, RSI em zona de compra, MACD positivo

2024-01-15 10:35:06 - mt5_agent.client - INFO - ✅ Ordem enviada: BUY 0.1 EURUSD
2024-01-15 10:35:07 - __main__ - INFO - ✅ ORDEM EXECUTADA!
   Tipo: BUY | Volume: 0.1 EURUSD
   Preço Entrada: 1.10234
   Stop Loss: 1.09984
   Take Profit: 1.10484
```

## 📋 Estrutura do Projeto

```
ai-finance-platform/
├── core/
│   ├── config.py              # Configuração centralizada
│   └── models.py              # Modelos de dados
├── mt5_agent/
│   ├── client.py              # Cliente MetaTrader 5
│   └── executor.py            # Executor de ordens
├── ai_engine/
│   ├── claude_client.py       # Cliente Claude API
│   └── market_analyzer.py     # Análise técnica
├── main.py                    # Bot principal
├── requirements.txt           # Dependências Python
├── .env.example               # Template de configuração
└── README.md                  # Este arquivo
```

## 🧠 Como Claude Funciona

O bot conversa com Claude em português, fornecendo:

1. **Dados de Mercado** - Últimos 10 candles com OHLCV
2. **Indicadores** - SMA, RSI, MACD
3. **Contexto** - Suportes, resistências, tendência

Claude retorna:
- Análise técnica detalhada
- Recomendação (BUY/SELL/HOLD)
- Confiança (0-100%)
- Níveis de Stop Loss e Take Profit

## ⚠️ Avisos Importantes

### Disclaimer
Este software é fornecido COMO ESTÁ, sem garantias. **Sempre teste em conta DEMO primeiro**.

### Boas Práticas

1. ✅ **Use Conta Demo** - Teste por pelo menos 1 semana antes de contas reais
2. ✅ **Monitore Inicialmente** - Não deixe 100% automatizado no início
3. ✅ **Defina Limites** - Configure `MAX_POSITIONS` com segurança
4. ✅ **Backup de API Keys** - Armazene credenciais com segurança
5. ✅ **Logs** - Verifique regularmente o arquivo de logs

### Riscos

- 📊 Trading tem risco total de perda
- 💰 Não inicie com valores que não possa perder
- 🔧 Bugs em software podem causar perdas
- ⚡ Falhas de conexão podem gerar operações indesejadas

## 🔧 Troubleshooting

### Erro: "MT5 init failed"

```
Solução:
1. Verifiue MT5_PATH está correto
2. Abra ManualMetaTrader 5
3. Verifique login/password/server
```

### Erro: "CLAUDE_API_KEY not configured"

```
Solução:
1. Copie .env.example para .env
2. Adicione sua API key em https://console.anthropic.com/
```

### Bot não executa ordens

```
Checklist:
- Conta está ativa/demo?
- Horário de funcionamento do mercado?
- Saldo suficiente para o lot_size?
- Símbolo está disponível? (EURUSD, GBPUSD, etc)
```

## 📚 Referências

- [MetaTrader 5 Python Docs](https://www.mql5.com/en/docs/integration/python_metatrader5)
- [Claude API Documentation](https://docs.anthropic.com/)
- [Análise Técnica - Investopedia](https://www.investopedia.com/articles/forex/09/technical-analysis-basics.asp)

## 💡 Próximos Passos

- [ ] Adicionar mais indicadores (Fibonacci, Ichimoku)
- [ ] Dashboard web em tempo real
- [ ] Sistema de backtest
- [ ] Múltiplos símbolos simultâneos
- [ ] Integração com mais brokers

## 📧 Suporte

Para problemas:
1. Verifique logs em `main.log`
2. Teste com `settings.debug = True`
3. Abra issue no GitHub

---

**Desenvolvido com ❤️ para traders que querem automação inteligente**
