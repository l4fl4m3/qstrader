# kalman_qstrader_backtest.py

import sys
sys.path.append('/Users/hassaannaeem/Documents/GitHub/qstrader')


import datetime
from qstrader import settings
from qstrader.strategy.base import AbstractStrategy
from qstrader.position_sizer.naive import NaivePositionSizer
from qstrader.event import SignalEvent, EventType
from qstrader.compat import queue
from qstrader.trading_session import TradingSession

from kalman_qstrader_strategy import KalmanPairsTradingStrategy


def run(config, testing, tickers, filename):
    # Backtest information

    title = [
        "Kalman Filter Pairs Trade on %s/%s" % (tickers[0],tickers[1])
    ]
    initial_equity = 100000.0
    start_date = datetime.datetime(2017, 1, 1)
    end_date = datetime.datetime(2018, 8, 19)

    # Use the KalmanPairsTrading Strategy
    events_queue = queue.Queue()
    strategy = KalmanPairsTradingStrategy(
        tickers, events_queue
    )

    # Use the Naive Position Sizer where
    # suggested quantities are followed
    position_sizer = NaivePositionSizer()

    # Set up the backtest
    backtest = TradingSession(
        config, strategy, tickers,
        initial_equity, start_date, end_date,
        events_queue, title=title,
        position_sizer=position_sizer
    )
    results = backtest.start_trading(testing=testing)
    return results



if __name__ == "__main__":
    # Configuration data

    testing = False
    config = settings.from_file(
        settings.DEFAULT_CONFIG_FILENAME, testing
    )
    tickers = ["FSBW", "RNST"]
    filename = ""
    run(config, testing, tickers, filename)
