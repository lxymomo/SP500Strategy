import pandas as pd
import numpy as np
import talib as ta

# 假设有一个 DataFrame 叫 `data`，它包含 OHLC 数据
# 示例： data = pd.read_csv('your_data.csv')

# 计算 ema200 和 ATR
data['ema200'] = ta.EMA(data['close'], timeperiod=200)
data['ATR'] = ta.ATR(data['high'], data['low'], data['close'], timeperiod=14)

# 计算上轨和下轨
data['upper_band'] = data['ema200'] + 20 * data['ATR']
data['lower_band'] = data['ema200'] - 20 * data['ATR']

# 初始化投资比例
data['investment'] = 0.0

# 基本功能1：本金投资
data.loc[data['close'] == data['upper_band'], 'investment'] = 0.5
data.loc[data['close'] == data['ema200'], 'investment'] = 1.0
data.loc[data['close'] == data['lower_band'], 'investment'] = 2.0

# 基本功能2：均仓投入
for i in range(len(data)):
    if data.at[i, 'close'] <= data.at[i, 'upper_band'] and data.at[i, 'close'] >= data.at[i, 'ema200']:
        atr_distance = (data.at[i, 'upper_band'] - data.at[i, 'close']) / data.at[i, 'ATR']
        data.at[i, 'investment'] = 0.5 + (atr_distance / 20) * 0.5
    elif data.at[i, 'close'] <= data.at[i, 'ema200'] and data.at[i, 'close'] >= data.at[i, 'lower_band']:
        atr_distance = (data.at[i, 'ema200'] - data.at[i, 'close']) / data.at[i, 'ATR']
        data.at[i, 'investment'] = 1.0 + (atr_distance / 20) * 1.0

# 输出策略结果
print(data[['close', 'ema200', 'ATR', 'upper_band', 'lower_band', 'investment']])
