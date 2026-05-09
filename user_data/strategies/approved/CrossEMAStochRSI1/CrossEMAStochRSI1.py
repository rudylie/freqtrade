import talib.abstract as ta
from pandas import DataFrame

from freqtrade.strategy import (
    CategoricalParameter,
    DecimalParameter,
    IntParameter,
    IStrategy,
)


class CrossEMAStochRSI1(IStrategy):
    INTERFACE_VERSION = 3

    can_short = False
    timeframe = "1h"
    startup_candle_count = 200
    process_only_new_candles = True

    minimal_roi = {
        "0": 1.0,
    }

    stoploss = -0.99
    trailing_stop = False
    use_exit_signal = True

    fast_ema_length = IntParameter(10, 40, default=28, space="buy")
    slow_ema_length = IntParameter(20, 80, default=48, space="buy")
    stoch_rsi_length = IntParameter(10, 30, default=14, space="buy")
    buy_stoch_rsi_max = DecimalParameter(0.55, 0.95, default=0.80, decimals=2, space="buy")
    require_cross = CategoricalParameter([False, True], default=False, space="buy")
    require_price_above_slow = CategoricalParameter([False, True], default=False, space="buy")
    require_slow_rising = CategoricalParameter([False, True], default=False, space="buy")
    adx_length = IntParameter(7, 28, default=14, space="buy")
    adx_min = DecimalParameter(0.0, 30.0, default=0.0, decimals=1, space="buy")
    atr_length = IntParameter(7, 28, default=14, space="buy")
    atr_pct_min = DecimalParameter(0.000, 0.030, default=0.000, decimals=3, space="buy")

    sell_stoch_rsi_min = DecimalParameter(0.05, 0.45, default=0.20, decimals=2, space="sell")
    use_price_below_fast_exit = CategoricalParameter([False, True], default=False, space="sell")
    use_fast_below_slow_exit = CategoricalParameter([False, True], default=True, space="sell")
    adx_exit_min = DecimalParameter(0.0, 40.0, default=0.0, decimals=1, space="sell")

    order_types = {
        "entry": "market",
        "exit": "market",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    plot_config = {
        "main_plot": {
            "ema_fast": {"color": "green"},
            "ema_slow": {"color": "blue"},
        },
        "subplots": {
            "StochRSI": {
                "stoch_rsi": {"color": "red"},
            },
            "ADX": {
                "adx": {"color": "black"},
                "plus_di": {"color": "green"},
                "minus_di": {"color": "red"},
            },
            "ATR": {
                "atr_pct": {"color": "brown"},
            },
        },
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema_fast"] = ta.EMA(dataframe, timeperiod=int(self.fast_ema_length.value))
        dataframe["ema_slow"] = ta.EMA(dataframe, timeperiod=int(self.slow_ema_length.value))

        dataframe["ema_bull"] = dataframe["ema_fast"] > dataframe["ema_slow"]
        dataframe["ema_cross_up"] = (
            (dataframe["ema_fast"] > dataframe["ema_slow"])
            & (dataframe["ema_fast"].shift(1) <= dataframe["ema_slow"].shift(1))
        )
        dataframe["ema_cross_down"] = (
            (dataframe["ema_fast"] < dataframe["ema_slow"])
            & (dataframe["ema_fast"].shift(1) >= dataframe["ema_slow"].shift(1))
        )

        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        stoch_window = int(self.stoch_rsi_length.value)
        rsi_min = dataframe["rsi"].rolling(stoch_window).min()
        rsi_max = dataframe["rsi"].rolling(stoch_window).max()
        rsi_range = (rsi_max - rsi_min).replace(0, None)
        dataframe["stoch_rsi"] = ((dataframe["rsi"] - rsi_min) / rsi_range).clip(0, 1)

        dataframe["trend_ok"] = True
        if self.require_price_above_slow.value:
            dataframe["trend_ok"] = dataframe["trend_ok"] & (dataframe["close"] > dataframe["ema_slow"])
        if self.require_slow_rising.value:
            dataframe["trend_ok"] = dataframe["trend_ok"] & (
                dataframe["ema_slow"] > dataframe["ema_slow"].shift(1)
            )

        dataframe["adx"] = ta.ADX(dataframe, timeperiod=int(self.adx_length.value))
        dataframe["plus_di"] = ta.PLUS_DI(dataframe, timeperiod=int(self.adx_length.value))
        dataframe["minus_di"] = ta.MINUS_DI(dataframe, timeperiod=int(self.adx_length.value))
        if self.adx_min.value > 0:
            dataframe["adx_ok"] = (
                (dataframe["adx"] >= self.adx_min.value)
                & (dataframe["plus_di"] > dataframe["minus_di"])
            )
        else:
            dataframe["adx_ok"] = True

        if self.adx_exit_min.value > 0:
            dataframe["adx_bearish_reversal"] = (
                (dataframe["adx"] >= self.adx_exit_min.value)
                & (dataframe["minus_di"] > dataframe["plus_di"])
            )
        else:
            dataframe["adx_bearish_reversal"] = False

        dataframe["atr"] = ta.ATR(dataframe, timeperiod=int(self.atr_length.value))
        dataframe["atr_pct"] = (dataframe["atr"] / dataframe["close"]).fillna(0)
        if self.atr_pct_min.value > 0:
            dataframe["atr_ok"] = dataframe["atr_pct"] >= self.atr_pct_min.value
        else:
            dataframe["atr_ok"] = True

        dataframe["volume_ok"] = dataframe["volume"] > 0
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        ema_condition = dataframe["ema_bull"]
        if self.require_cross.value:
            ema_condition = dataframe["ema_cross_up"]

        dataframe.loc[
            (
                dataframe["volume_ok"]
                & dataframe["trend_ok"]
                & dataframe["adx_ok"]
                & dataframe["atr_ok"]
                & ema_condition
                & (dataframe["stoch_rsi"] <= self.buy_stoch_rsi_max.value)
            ),
            ["enter_long", "enter_tag"],
        ] = (1, "cross_ema_stoch_long")

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        exit_condition = (
            dataframe["volume_ok"]
            & (dataframe["stoch_rsi"] >= self.sell_stoch_rsi_min.value)
        )

        if self.use_fast_below_slow_exit.value:
            exit_condition = exit_condition & (dataframe["ema_fast"] < dataframe["ema_slow"])
        else:
            exit_condition = exit_condition & dataframe["ema_cross_down"]

        if self.use_price_below_fast_exit.value:
            exit_condition = exit_condition | (
                dataframe["volume_ok"] & (dataframe["close"] < dataframe["ema_fast"])
            )

        exit_condition = exit_condition | (
            dataframe["volume_ok"] & dataframe["adx_bearish_reversal"]
        )

        dataframe.loc[
            exit_condition,
            ["exit_long", "exit_tag"],
        ] = (1, "cross_ema_stoch_exit")

        return dataframe
