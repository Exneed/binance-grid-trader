inance Grid Trading Bot + Backtest System
This project includes a fully functional Grid Trading bot for Binance and a backtesting module for simulating performance on historical data.

The grid trading strategy places buy and sell limit orders at predefined price intervals, aiming to profit from market volatility. The backtest engine allows you to test and optimize the strategy using real historical market data before deploying it with live funds.

Features
Real-time grid trading on Binance Spot
Full Testnet support for safe testing without risking real funds
 Historical backtesting with CSV data
Fully configurable strategy parameters (grid range, levels, order size, etc.)
Modular Python code, easy to modify or extend

 Project Structure
config.py – API keys and strategy parameters

grid_bot.py – Executes real-time grid trading on Binance

veri_cek.py – Downloads historical data and saves it as historical_data.csv

backtest.py – Runs a simulation using historical price data

💻 How to Run
Install dependencies:

pip install pandas python-binance
Edit your API keys and strategy in config.py.

To place grid orders on Binance (Testnet or live):

python grid_bot.py
To download historical data:


python veri_cek.py
To run the backtest:

Make sure historical_data.csv is in the project folder.

Update the file path in the backtest script if needed.
python backtest.py

⚠️ Disclaimer
This project is for educational and research purposes. Use it at your own risk. Always test thoroughly with a Binance Testnet account before using real funds.




















<img width="1337" height="975" alt="image" src="https://github.com/user-attachments/assets/bc6e13b6-e323-4575-bb04-03cb6405ad76" /># binance-grid-trader
Automated grid trading strategy for Binance spot/futures markets.


open the powershell and text this  streamlit run grid_streamlit.py
or you can do it for backtest python backtest.py 
<img width="883" height="432" alt="image" src="https://github.com/user-attachments/assets/0d89e7d6-870e-4ddc-8638-0130d150aa28" />
<img width="465" height="125" alt="image" src="https://github.com/user-attachments/assets/4fa48728-ff5c-45f8-af4a-d5212239ecf7" />






