# 📊 Análise de Ações B3 - MVP

Plataforma automatizada de análise fundamentalista de ações da B3, com detecção inteligente de oportunidades e value traps.

## 🎯 Funcionalidades

- **Análise Automatizada**: Dados atualizados diariamente via Yahoo Finance e CVM
- **Scanner de Oportunidades**: Detecta divergências entre fundamentos e preço
- **Indicadores Fundamentalistas**: P/L, P/VP, ROE, Margem Líquida e mais
- **Score Proprietário**: Sistema de pontuação 0-100 para cada ação
- **Interface Intuitiva**: Design inspirado em stockanalysis.com e statusinvest.com.br

## 🚀 Como Rodar Localmente

### Pré-requisitos
- Python 3.11+
- Git

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/analise-acoes-mvp.git
cd analise-acoes-mvp

# 2. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Inicialize o banco de dados
python scripts/init_database.py

# 5. (Opcional) Popule dados iniciais
python scripts/seed_data.py

# 6. Execute a aplicação
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
analise-acoes-mvp/
├── app.py                    # Arquivo principal
├── pages/                    # Páginas Streamlit
├── src/                      # Código fonte
│   ├── database/            # Modelos e conexão
│   ├── scrapers/            # Coletores de dados
│   ├── analysis/            # Algoritmos de análise
│   ├── jobs/                # Jobs automatizados
│   └── utils/               # Utilitários
├── components/              # Componentes reutilizáveis
├── scripts/                 # Scripts de manutenção
└── data/                    # Banco de dados (gitignore)
```

## 🤖 Automação

O sistema atualiza dados automaticamente:
- **19h diariamente**: Cotações (Yahoo Finance)
- **20h diariamente**: Cálculo de scores
- **Domingos 2h**: Dados fundamentalistas (CVM)
- **3h diariamente**: Backup do banco de dados

## 🛠️ Tecnologias

- **Frontend/Backend**: Streamlit
- **Banco de Dados**: SQLite (dev) / PostgreSQL (prod)
- **Scraping**: yfinance, BeautifulSoup4, pdfplumber
- **Análise**: pandas, numpy, scipy
- **Visualização**: Plotly
- **Automação**: APScheduler

## 📊 Fontes de Dados

- **Cotações**: Yahoo Finance API
- **Fundamentalistas**: CVM (DFP/ITR via XBRL)
- **Macroeconômicos**: Banco Central do Brasil

## 🔧 Configuração Avançada

### Variáveis de Ambiente (opcional)

Crie arquivo `.env` na raiz:

```env
DATABASE_URL=sqlite:///data/stocks.db
LOG_LEVEL=INFO
ENABLE_SCHEDULER=true
```

### Deploy no Streamlit Cloud

1. Faça push para GitHub
2. Conecte em [share.streamlit.io](https://share.streamlit.io)
3. Selecione o repositório
4. Deploy automático!

## 📝 Licença

MIT License - veja arquivo LICENSE

## 🤝 Contribuindo

Contribuições são bem-vindas! Abra uma issue ou pull request.

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no GitHub.

---

**Disclaimer**: Esta plataforma é apenas para fins educacionais e informativos. Não constitui recomendação de investimento. Sempre consulte um profissional antes de investir.
