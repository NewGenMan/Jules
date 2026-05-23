import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data_loader import download_data, get_closing_prices
from src.pair_finder import find_cointegrated_pairs, calculate_hedge_ratio
from src.strategy import calculate_spread, calculate_zscore
from src.backtester import run_backtest, calculate_returns
import datetime

def main():
    st.set_page_config(page_title="Simons Scalping Dashboard", layout="wide")
    st.title("📈 Simons Scalping System - Real-time Monitoring")

    # Sidebar - Parameters
    st.sidebar.header("Strategy Parameters")
    tickers_input = st.sidebar.text_input("Tickers (comma separated)", "SPY,IVV,GLD,GDX,AAPL,MSFT,META,GOOGL")
    tickers = [t.strip() for t in tickers_input.split(",")]

    interval = st.sidebar.selectbox("Interval", ["5m", "15m", "30m", "1h", "1d"], index=0)
    lookback_days = st.sidebar.slider("Lookback Days", 1, 59, 30)

    z_threshold = st.sidebar.slider("Z-Score Entry Threshold", 1.0, 3.0, 2.0, 0.1)
    z_exit = st.sidebar.slider("Z-Score Exit Threshold", 0.0, 1.0, 0.0, 0.1)
    window = st.sidebar.slider("Z-Score Window", 10, 100, 20)

    # Data Loading
    end_dt = datetime.datetime.now()
    start_dt = end_dt - datetime.timedelta(days=lookback_days)

    if st.sidebar.button("Run Analysis"):
        with st.spinner("Downloading data and identifying pairs..."):
            data_dict = download_data(tickers, start_dt.strftime('%Y-%m-%d'), end_dt.strftime('%Y-%m-%d'), interval=interval)
            closing_prices = get_closing_prices(data_dict)

            scores, pvalues, pairs = find_cointegrated_pairs(closing_prices)

            if not pairs:
                st.error("No cointegrated pairs found with the current parameters.")
                return

            st.success(f"Found {len(pairs)} cointegrated pairs!")

            # Display Pairs
            pair_df = pd.DataFrame(pairs, columns=['Stock 1', 'Stock 2', 'P-Value'])
            st.write("### Cointegrated Pairs", pair_df)

            # Analysis for the best pair
            best_pair = pairs[0]
            s1_name, s2_name = best_pair[0], best_pair[1]
            st.header(f"Detailed Analysis: {s1_name} & {s2_name}")

            S1 = closing_prices[s1_name]
            S2 = closing_prices[s2_name]
            hedge_ratio = calculate_hedge_ratio(S1, S2)
            spread = calculate_spread(S1, S2, hedge_ratio)
            zscore = calculate_zscore(spread, window)
            signals = run_backtest(S1, S2, zscore, entry_threshold=z_threshold, exit_threshold=z_exit)
            results = calculate_returns(signals, S1, S2, hedge_ratio)

            # Visualizations
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Price Series")
                fig_price = go.Figure()
                fig_price.add_trace(go.Scatter(x=S1.index, y=S1, name=s1_name))
                fig_price.add_trace(go.Scatter(x=S2.index, y=S2, name=s2_name))
                st.plotly_chart(fig_price, use_container_width=True)

            with col2:
                st.subheader("Spread Z-Score")
                fig_z = go.Figure()
                fig_z.add_trace(go.Scatter(x=zscore.index, y=zscore, name="Z-Score"))
                fig_z.add_hline(y=z_threshold, line_dash="dash", line_color="red")
                fig_z.add_hline(y=-z_threshold, line_dash="dash", line_color="red")
                fig_z.add_hline(y=0, line_color="white")
                st.plotly_chart(fig_z, use_container_width=True)

            st.subheader("Cumulative Returns")
            fig_ret = go.Figure()
            fig_ret.add_trace(go.Scatter(x=results.index, y=results['cumulative_returns'], name="Returns"))
            st.plotly_chart(fig_ret, use_container_width=True)

            st.metric("Final Return", f"{(results['cumulative_returns'].iloc[-1]-1)*100:.2f}%")

if __name__ == "__main__":
    main()
