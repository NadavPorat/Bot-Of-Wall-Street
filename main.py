from value_result_tracker import stock_bought_value, num_of_stocks_value, total_money_spent_value
from value_algorithm import rv_dataframe_results
from momentum_algorithm import hqm_dataframe_results
from momentum_result_tracker import stock_bought, num_of_stocks, total_money_spent
import streamlit as st
import numpy as np
import time
import requests
import pandas as pd
import sys
sys.path.insert(1, '/app/botofwallstreet/')

portfolio_size = 100000
start = False
IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'
if start == False:
    st.header("Welcome to my trading algorithm simulation!")
    st.subheader(
        "There are two algorithm profiles - momentum and value based.")
    st.subheader("The default portfolio size is set to 100,000$")
    st.subheader("Enjoy!")

selected_algorithm = st.selectbox('Select Trading Algorithm', [
                                  'Quantitative Momentum', 'Quantitative Value'])

start = st.button('Start Trading Simulation')
if start:
    st.header("Top Ranked Stocks")
    if selected_algorithm == 'Quantitative Momentum':
        st.write(hqm_dataframe_results)
    else:
        st.write(rv_dataframe_results)


def updated_results(shares_ammount, shares_bought, total_investment):
    owned_stock_prices = 0
    latest_price = 0
    for i in range(0, 10):
        api_url = f'https://sandbox.iexapis.com/stable/stock/{shares_bought[i]}/quote/?token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(api_url).json()
        latest_price = int(data['latestPrice'])
        owned_stock_prices += (latest_price * shares_ammount[i])
    if (owned_stock_prices - total_investment) > 0:
        st.balloons()
        st.success('Congratulation! You Have Beaten The Market!')
    return (owned_stock_prices - total_investment)


st.header("Algorithm Real-Time Results")
if start and selected_algorithm == 'Quantitative Momentum':
    gains = updated_results(num_of_stocks, stock_bought, total_money_spent)
    prices_array = np.array([gains])
    with st.beta_container():
        result_chart = st.line_chart(prices_array)
        st.write("Profit/Loss in $ (Ticks Every 5 seconds)")
    for i in range(0, 30):
        new_rows = np.append(prices_array, updated_results(
            num_of_stocks, stock_bought, total_money_spent))
        result_chart.add_rows(new_rows)
        prices_array = new_rows
        time.sleep(1)
elif start == False:
    st.info('Please choose trading algorithm')
elif start and portfolio_size and selected_algorithm == 'Quantitative Value':
    gains = updated_results(num_of_stocks_value,
                            stock_bought_value, total_money_spent_value)
    prices_array = np.array([gains])
    with st.beta_container():
        result_chart = st.line_chart(prices_array)
        st.write("Profit/Loss in $ (Ticks Every 5 seconds)")
    for i in range(0, 30):
        new_rows = np.append(prices_array, updated_results(
            num_of_stocks_value, stock_bought_value, total_money_spent_value))
        result_chart.add_rows(new_rows)
        prices_array = new_rows
        time.sleep(1)
