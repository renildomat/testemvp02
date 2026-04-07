"""
Análise de Ações B3 - MVP
Homepage da aplicação Streamlit
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Análise de Ações B3",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar CSS customizado
css_file = Path(__file__).parent / "assets" / "styles.css"
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Imports locais
from src.database import get_session, Stock, OpportunityScore, JobLog
from components.cards import stat_box, alert_card, info_card
from components.charts import create_bar_chart
from src.utils.helpers import format_currency


def load_dashboard_data():
    """Carrega dados para o dashboard"""
    session = get_session()
    
    try:
        # Total de ações
        total_stocks = session.query(Stock).count()
        
        # Scores mais recentes
        today = datetime.now().date()
        recent_scores = session.query(OpportunityScore).filter(
            OpportunityScore.date == today
        ).all()
        
        # Distribuição de sinais
        buy_count = sum(1 for s in recent_scores if s.signal == 'BUY')
        sell_count = sum(1 for s in recent_scores if s.signal == 'SELL')
        hold_count = sum(1 for s in recent_scores if s.signal == 'HOLD')
        
        # Último job executado
        last_job = session.query(JobLog).order_by(
            JobLog.finished_at.desc()
        ).first()
        
        return {
            'total_stocks': total_stocks,
            'total_analyzed': len(recent_scores),
            'buy_count': buy_count,
            'sell_count': sell_count,
            'hold_count': hold_count,
            'last_update': last_job.finished_at if last_job else None,
            'recent_scores': recent_scores
        }
        
    finally:
        session.close()


def main():
    """Página principal"""
    
    # Header
    st.title("📊 Análise de Ações B3")
    st.markdown("### Plataforma Automatizada de Análise Fundamentalista")
    
    st.markdown("---")
    
    # Carregar dados
    try:
        data = load_dashboard_data()
    except Exception as e:
        alert_card(
            f"Erro ao carregar dados: {e}. Execute 'python scripts/seed_data.py' para popular o banco.",
            "error"
        )
        st.stop()
    
    # Verificar se tem dados
    if data['total_stocks'] == 0:
        st.warning("⚠️ Banco de dados vazio!")
        info_card(
            "Primeiros Passos",
            """
            1. Execute: `python scripts/init_database.py`
            2. Execute: `python scripts/seed_data.py`
            3. Recarregue esta página
            """,
            "🚀"
        )
        st.stop()
    
    # KPIs principais
    st.subheader("📈 Visão Geral")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        stat_box(
            "Ações Monitoradas",
            str(data['total_stocks']),
            "📊",
            "#1E40AF"
        )
    
    with col2:
        stat_box(
            "Oportunidades (BUY)",
            str(data['buy_count']),
            "🚀",
            "#10B981"
        )
    
    with col3:
        stat_box(
            "Alertas (SELL)",
            str(data['sell_count']),
            "⚠️",
            "#EF4444"
        )
    
    with col4:
        stat_box(
            "Neutras (HOLD)",
            str(data['hold_count']),
            "➡️",
            "#F59E0B"
        )
    
    st.markdown("---")
    
    # Seção de destaques
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Top Oportunidades")
        
        if data['recent_scores']:
            # Filtrar apenas BUY e ordenar por score
            buy_scores = [s for s in data['recent_scores'] if s.signal == 'BUY']
            buy_scores.sort(key=lambda x: x.score, reverse=True)
            
            if buy_scores:
                # Top 10
                top_10 = buy_scores[:10]
                
                # Criar DataFrame
                df_top = pd.DataFrame([{
                    'Ticker': s.stock.ticker,
                    'Empresa': s.stock.company_name[:30] + '...' if len(s.stock.company_name) > 30 else s.stock.company_name,
                    'Score': s.score,
                    'Setor': s.stock.sector
                } for s in top_10])
                
                st.dataframe(
                    df_top,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        'Score': st.column_config.ProgressColumn(
                            'Score',
                            min_value=0,
                            max_value=100,
                            format='%d'
                        )
                    }
                )
            else:
                st.info("Nenhuma oportunidade identificada no momento.")
        else:
            st.info("Execute o cálculo de scores para ver oportunidades.")
    
    with col2:
        st.subheader("⚠️ Value Traps")
        
        if data['recent_scores']:
            # Filtrar apenas SELL e ordenar por score (menor primeiro)
            sell_scores = [s for s in data['recent_scores'] if s.signal == 'SELL']
            sell_scores.sort(key=lambda x: x.score)
            
            if sell_scores:
                # Top 5 piores
                top_5 = sell_scores[:5]
                
                for score in top_5:
                    st.markdown(f"""
                        <div style="
                            background: #FEE2E2;
                            border-left: 4px solid #EF4444;
                            padding: 10px;
                            margin: 10px 0;
                            border-radius: 5px;
                        ">
                            <strong style="color: #991B1B;">{score.stock.ticker}</strong>
                            <br/>
                            <small style="color: #6B7280;">Score: {score.score}/100</small>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Nenhum alerta identificado.")
        else:
            st.info("Aguardando cálculo de scores.")
    
    st.markdown("---")
    
    # Distribuição de sinais (gráfico)
    if data['total_analyzed'] > 0:
        st.subheader("📊 Distribuição de Sinais")
        
        dist_df = pd.DataFrame({
            'Sinal': ['BUY', 'HOLD', 'SELL'],
            'Quantidade': [data['buy_count'], data['hold_count'], data['sell_count']],
            'Color': ['#10B981', '#F59E0B', '#EF4444']
        })
        
        fig = create_bar_chart(
            dist_df,
            'Sinal',
            'Quantidade',
            'Distribuição de Sinais de Mercado'
        )
        
        # Colorir barras
        import plotly.graph_objects as go
        fig.data[0].marker.color = dist_df['Color']
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Rodapé com informações
    col1, col2, col3 = st.columns(3)
    
    with col1:
        info_card(
            "💡 Como Funciona",
            "Analisamos divergências entre preço e fundamentos para identificar oportunidades de compra e value traps.",
            "💡"
        )
    
    with col2:
        info_card(
            "🤖 Automação",
            "Dados atualizados automaticamente: Cotações (19h), Scores (20h), CVM (Domingos 2h).",
            "🤖"
        )
    
    with col3:
        if data['last_update']:
            update_time = data['last_update'].strftime('%d/%m/%Y %H:%M')
            info_card(
                "🕐 Última Atualização",
                f"Sistema atualizado em {update_time}",
                "🕐"
            )
        else:
            info_card(
                "🕐 Sistema",
                "Primeira execução - aguardando dados",
                "🕐"
            )
    
    # Sidebar com navegação
    with st.sidebar:
        st.title("📑 Navegação")
        st.markdown("---")
        
        st.page_link("app.py", label="🏠 Home", icon="🏠")
        st.page_link("pages/1_📊_Ações.py", label="📊 Listagem de Ações", icon="📊")
        st.page_link("pages/2_🎯_Oportunidades.py", label="🎯 Scanner de Oportunidades", icon="🎯")
        st.page_link("pages/3_📈_Análise.py", label="📈 Análise Detalhada", icon="📈")
        st.page_link("pages/4_⚙️_Configurações.py", label="⚙️ Configurações", icon="⚙️")
        
        st.markdown("---")
        
        st.markdown("""
            ### ℹ️ Sobre
            
            **Versão:** 1.0.0  
            **Fontes de Dados:**
            - Yahoo Finance (Cotações)
            - CVM (Fundamentalistas)
            - Banco Central (Macro)
            
            ---
            
            ⚠️ **Disclaimer:** Esta plataforma é apenas para fins educacionais. Não constitui recomendação de investimento.
        """)


if __name__ == "__main__":
    main()
