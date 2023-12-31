# blkbrd-case-study
All timestamps below are US local time during summer hours, before daylight saving change.

Starting Point: During US hours, i.e., 9:30 to 16:00, international equity index futures move together with US market.
                Take SPX/ES1 and XP1 as an example, if SPX/ES1 goes up during the day, XP1 most likely will go up during US trading hours too (~0.8 correlation).
                Given the correlation, we can run a regression analysis of XP1 returns on SPX/ES1 returns. The idea is y_hat (when beta is statistically significant) should be the "fair value" of XP1 if the market has consolidated all information and fully understood the impact on ASX.
                The residual from the regression analysis then measures over or under reaction of the instrument to news and other market movements which might create some short term arbitrage opportunities if the deviation is large enough, i.e., more than one standard deviation away.
                
Special Case: SPX closes at 16:00 and XP1 stops trading 1 hour after that at 17:00. And XP1 normally doesn't move much during that 1 hour since no major markets open and short time frame.
              When XP1 reopens at 19:00 with ASX or 18:50 to be exact, same assumption as above that no major markets open during the gap and little new information (even if there is sentiment change, we cannot measure it with equity index move and position at XP1 close), there is still a price gap between 17:00 and 18:50 on most days.
              ![IMG_0540](https://github.com/springmarathon/blkbrd-case-study/assets/7278877/3c7330a1-bab2-4bab-baa6-8894c25fc6ca)
              The gap can be explained in different ways: 1) XP1 went up too much (very positive residual) during US session and the open price at 19:00 is fairer value since the market has had the time to consolidate and update stale prices. Movements after that are new information coming in from Australia already.
                                                          2) XP1 movement during US session was fair but it takes time for Australian traders to absort the overnight information and adjust well to new price levels especially when the prior day's return is significant, i.e., Fed didn't hike as expected.

Potential Triggers
1) Run a regression of XP1 return on SPX return (potentially can include CL1 and TSX as regressors too) and normalize residuals to z-scores. Long term wise the correlation should be stable and significant but short term wise prices deviate.
   Specifically, we sell XP1 and buy ES1 as hedge when residual z-score > 1 std and buy XP1 and sell ES1 as hedge when residual z-score < -1 std, hoping the gap will close. Might also need to stop loss at +/-2 std meaning structure temporarily breaks.   
2) Just use intraday SPX returns as the trigger, i.e., Close Price / Open Price - 1, normalize it to a z-score. Assuming that right at ASX open, the market hasn't fully comprehended what happend overnight, and will underreact.
   If z-score is greater than 1, there was very positive news and we sell XP1 at SPX close and buy it back at ASX open. If z-score is less than -1, there was very negative news and we buy XP1 at SPX close and sell it at ASX open.

There are clearly many cases where SPX went down overnight and ASX goes up once market opens. And even if the second trigger makes any sense, this cannot be converted to a 24hrs strategy, since mostly all equity index futures stop trading with US and resumes after a few hours. And the longer the gap, the more unpredictable the open price is. So maybe instead of just fasicating on the trading gap, we treat the gap as an exaggerated case of price anomaly and try trigger 1) first. And this way, the strategy is not constrained at US close.

Implementation Steps
1) For a given future contract ES1/XP1, identify a set of equity indices as regressors to cover its all trading hours, i.e., ASX - Nikkei - HSI/Kospi - India - Euro Stoxx - SPX/Nasdaq
2) Run rolling piecewise regression of historical ES1/XP1 returns independently on different equity index historical returns and look for reliable and meaningful correlations during same trading hours, beta coefficients and residual distributions per se.
   Use previous 2-3 days data to generate parameters. These parameters seem to be stable over short period of time, meaning can be used on the trading day itself.
4) Use these to calculate real time y_hat and residual and z-score of residual and use this as main signal. This can also be used as certainty measure, meaning the wider the gap, the more likely it will come back. T-stats on beta coefficient is also measure of certainty, higher t-stat means more stability.
5) For example, ES1 tracks Euro Stoxx closely before US opens, if residual is greater than 1 std we can sell ES1 and buy VG1 as hedge and exit the trade when the gap disappears. Hedge ratio cen be determined by beta.
   ES1 tracks Nikkie/Topix/Kospi/HSI more or less too during Asia hours, if residual is greater than maybe 1.5 std we can sell ES1 and buy NK1/TP1/KM1/HI1 as hedge.
6) Replicate this to other indices. Use SX5E as regressor during EU session to trade XP1/ES1/NK1 etc.

Sensitivity Test
1) Market Volatility: regression assume constant variance, changing volatility impacts accuracy and certainty of y_hat and residual. Higher volatility means more opportunities but probably shorter execution window.
2) Liquidity / Volume: how much capacity there is for this trade, how much can we trade without significant market impact
3) Entry Threshold: tested 1 std vs 0.5 std, 1 std threshold should have higher win rate but less triggered trades and 0.5 std threshold should have lower win rate and more triggered trades
4) Exit Strategy: I used 30 minutes bar as sample input data in this exercise, so assumed once the signal is triggered, we can enter at next 30 minutes' open and exit at its close. In reality, such a strategy should work with minute bars or even more granular data.
5) Transaction Cost: bid-ask spread and slippage cost that can eat the profit
6) Real time modeling and execution capabilities

Questions for myself:
1) How to evaluate this is the right way to convert the idea? It first makes some sense. Second, this needs to work with real data. We need to see a clear pattern of price deviation and then mean reversion. This needs to be verified with more days and more pairs.
   ![image](https://github.com/springmarathon/blkbrd-case-study/assets/7278877/cfef1570-de89-4869-8941-67b34d62def9)
2）When does it not work, i.e., keep diverging instead of mean reverting? Some news impacting XP1 more than US/EU.
3) The strategy needs some parameters generated from historical data, i.e., beta coefficients. What should be the look back period to use? This doesn't work with long term data.
4) What else can be used to measure price divergence? Maybe not run regression with returns, run regression with price series, then this becomes a cointegration trade.
