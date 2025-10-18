import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="FinPlan AI Insights", 
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to improve embedding
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stApp > header {
        background-color: transparent;
    }
    .stApp {
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🧠 FinPlan AI Insights")
st.markdown("**Advanced Financial Analytics Dashboard**")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Portfolio Analysis", "📈 Market Trends", "🎯 Goal Tracking", "💡 Recommendations"])

with tab1:
    st.subheader("Portfolio Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sample portfolio data
        portfolio_data = {
            'Asset': ['Stocks', 'Bonds', 'Real Estate', 'Commodities', 'Cash'],
            'Allocation': [45, 25, 15, 10, 5],
            'Performance': [8.5, 4.2, 6.8, 2.1, 1.5]
        }
        
        df_portfolio = pd.DataFrame(portfolio_data)
        
        # Pie chart for allocation
        fig_pie = px.pie(df_portfolio, values='Allocation', names='Asset', 
                        title="Current Portfolio Allocation",
                        color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Performance chart
        fig_bar = px.bar(df_portfolio, x='Asset', y='Performance', 
                        title="Asset Performance (%)",
                        color='Performance',
                        color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.subheader("Market Trends")
    
    # Generate sample market data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    market_data = pd.DataFrame({
        'Date': dates,
        'S&P 500': np.cumsum(np.random.randn(len(dates)) * 0.01) + 100,
        'NASDAQ': np.cumsum(np.random.randn(len(dates)) * 0.015) + 100,
        'DOW': np.cumsum(np.random.randn(len(dates)) * 0.008) + 100
    })
    
    fig_line = px.line(market_data, x='Date', y=['S&P 500', 'NASDAQ', 'DOW'],
                      title="Market Index Performance (2024)")
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Market metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("S&P 500", "4,567.89", "2.34%")
    with col2:
        st.metric("NASDAQ", "14,432.12", "1.89%")
    with col3:
        st.metric("DOW", "35,678.90", "0.76%")
    with col4:
        st.metric("VIX", "18.45", "-2.1%")

with tab3:
    st.subheader("Financial Goal Tracking")
    
    # Sample goals data
    goals_data = {
        'Goal': ['Emergency Fund', 'House Down Payment', 'Retirement', 'Education', 'Vacation'],
        'Target': [50000, 200000, 1000000, 80000, 15000],
        'Current': [35000, 85000, 250000, 25000, 12000]
    }
    
    df_goals = pd.DataFrame(goals_data)
    df_goals['Progress'] = (df_goals['Current'] / df_goals['Target'] * 100).round(1)
    df_goals['Remaining'] = df_goals['Target'] - df_goals['Current']
    
    # Goal progress chart
    fig_goals = go.Figure()
    fig_goals.add_trace(go.Bar(name='Current', x=df_goals['Goal'], y=df_goals['Current']))
    fig_goals.add_trace(go.Bar(name='Remaining', x=df_goals['Goal'], y=df_goals['Remaining']))
    fig_goals.update_layout(barmode='stack', title="Goal Progress Tracking")
    st.plotly_chart(fig_goals, use_container_width=True)
    
    # Progress table
    st.dataframe(df_goals[['Goal', 'Target', 'Current', 'Progress', 'Remaining']], use_container_width=True)

with tab4:
    st.subheader("AI Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Personalized Insights")
        st.info("**Risk Assessment**: Your current portfolio shows moderate risk tolerance with good diversification.")
        st.success("**Goal Achievement**: You're on track to meet your emergency fund goal by Q2 2024.")
        st.warning("**Optimization**: Consider increasing your stock allocation by 5% to maximize long-term growth.")
        
    with col2:
        st.markdown("### 📋 Action Items")
        st.checkbox("Increase monthly savings by $500", value=False)
        st.checkbox("Rebalance portfolio allocation", value=False)
        st.checkbox("Review insurance coverage", value=True)
        st.checkbox("Set up automatic investments", value=False)
        
        if st.button("Generate New Recommendations", type="primary"):
            st.balloons()
            st.success("New recommendations generated based on your latest financial data!")

# Footer
st.markdown("---")
st.markdown("*Powered by FinPlan AI - Your Intelligent Financial Assistant*")