import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from datetime import timedelta


y_instrument = "XP1" # "NK1" # "ES1"
x_index = "SX5E" # SPX
hedge = "VG1" # ES1
threshold = 1 # 0.75

x_df = pd.read_csv("index/{}.csv".format(x_index))
x_df["Dates"] = pd.to_datetime(x_df["Dates"])

x_start = x_df.loc[x_df.groupby(x_df.Dates.dt.date, as_index=False).Dates.idxmin().Dates, ["Dates", "Open"]]
x_start.rename(columns={"Dates": "Start Time"}, inplace=True)
x_start["Dates"] = x_start["Start Time"].dt.date
x_start.set_index("Dates", inplace=True)

x_end = x_df.loc[x_df["Dates"].isin(x_start["Start Time"] + timedelta(hours=6)).values, ["Dates", "Close"]]
x_end.rename(columns={"Dates": "End Time"}, inplace=True)
x_end["Dates"] = x_end["End Time"].dt.date
x_end.set_index("Dates", inplace=True)

x_ret = pd.merge(left=x_start, right=x_end, left_index=True, right_index=True, how="inner")
x_ret["IntradayRet"] = x_ret["Close"] / x_ret["Open"] - 1

y_df = pd.read_csv("futures/{}.csv".format(y_instrument))
y_df["Dates"] = pd.to_datetime(y_df["Dates"])

overlap_df = pd.merge(left=x_ret, right=y_df, left_on="Start Time", right_on="Dates", how="inner", suffixes=["", "_y_start"])
overlap_df = pd.merge(left=overlap_df, right=y_df, left_on="End Time", right_on="Dates", how="inner", suffixes=["", "_y_end"])
overlap_df = overlap_df[["Dates", "Start Time", "Open", "End Time", "Close", "IntradayRet", "Open_y_start", "Close_y_end"]]
overlap_df["IntradayRet_y"] = overlap_df["Close_y_end"] / overlap_df["Open_y_start"] - 1

y = overlap_df.IntradayRet_y
X = overlap_df.IntradayRet
model = sm.OLS(y, X)
results = model.fit()
# print(results.summary())

overlap_df["y_hat"] = results.fittedvalues
overlap_df["residual"] = overlap_df["IntradayRet_y"] - overlap_df["y_hat"]
beta = results.params[0]
m = overlap_df["residual"].mean()
s = overlap_df["residual"].std()
vol_y = np.sqrt(252) * overlap_df["IntradayRet_y"].std()
vol_x = np.sqrt(252) * overlap_df["IntradayRet"].std()

hedge_df = pd.read_csv("futures/{}.csv".format(hedge))
hedge_df["Dates"] = pd.to_datetime(hedge_df["Dates"])
data = pd.merge(left=x_df, right=y_df, left_on="Dates", right_on="Dates", suffixes=["", "_y"])
data = pd.merge(left=data, right=hedge_df, left_on="Dates", right_on="Dates", suffixes=["", "_hedge"])
# Poor assumption of constant holding period of 30 minutes
data["x_Ret"] = data["Close"] / data["Open"] - 1
data["y_Ret"] = data["Close_y"] / data["Open_y"] - 1
data["y_hat"] = data["x_Ret"] * beta
data["Residual"] = data["y_Ret"] - data["y_hat"]
data["z-score"] = (data["Residual"] - m) / s

triggers = data.loc[((data["z-score"] > threshold) | (data["z-score"] < -1 * threshold))] # & (data["Dates"].dt.hour <= 8)]
trades = data.iloc[triggers.index + 1]

y_pnl = (trades["Open_y"] - trades["Close_y"]) * np.sign(triggers["z-score"].values)
hedge_pnl = (trades["Close_hedge"] - trades["Open_hedge"]) * np.sign(triggers["z-score"].values)

pnl_df = triggers.loc[:, ["Dates", "z-score"]]
pnl_df["y_pnl"] = y_pnl.values
pnl_df["hedge_pnl"] = hedge_pnl.values * vol_y / vol_x
pnl_df["total_pnl"] = pnl_df["y_pnl"] + pnl_df["hedge_pnl"]
print(pnl_df.head(50))
print(sum(y_pnl) + sum(hedge_pnl) * vol_y / vol_x)
win_rate = pnl_df[pnl_df["total_pnl"] > 0].shape[0] / pnl_df.shape[0]
print(win_rate)
# print(pnl_df[pnl_df["total_pnl"] > 0]["total_pnl"].mean() * win_rate / (1 - win_rate) / pnl_df[pnl_df["total_pnl"] < 0]["total_pnl"].mean())

# plt.scatter(pnl_df["z-score"], pnl_df["total_pnl"])
# plt.show()
print("Done")