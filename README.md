# blkbrd-case-study
All timestamps below are US local time during summer hours, before daylight saving change.

Starting Point: During US hours, i.e., 9:30 to 16:00, international equity index futures move together with US market.
                Take SPX and XP1 as an example, if SPX goes up during the day, XP1 most likely will go up during US trading hours too (~0.8 correlation).
                Given the correlation, we can run a regression analysis of XP1 returns on SPX returns. The idea is y_hat (when beta is statistically significant) should be the "fair value" of XP1 if the market has consolidated all information and fully understood the impact on ASX.
                The residual from the regression analysis then measures over or under reaction of the instrument to news and other market movements which might create some short term arbitrage opportunities if the deviation is large enough, i.e., more than one standard deviation away.
                
Special Case: SPX closes at 16:00 and XP1 stops trading 1 hour after that at 17:00. And XP1 normally doesn't move much during that 1 hour since no major markets open and short time frame (low vol assumption).
              When XP1 reopens at 19:00 with ASX or 18:50 to be exact, same assumption as above that no major markets open during the gap and little new information, there is still a price gap between 17:00 and 18:50 on most days.
              ![IMG_0540](https://github.com/springmarathon/blkbrd-case-study/assets/7278877/3c7330a1-bab2-4bab-baa6-8894c25fc6ca)
              The gap can be explained in different ways: 1) XP1 went up too much (very positive residual) during US session and the open price at 19:00 is fairer value since the market has had the time to consolidate and update stale prices. Movements after that are new information coming in from Australia already.
                                                          2) XP1 movement during US session was fair but it takes time for Australian traders to absort the overnight information and adjust well to new price levels especially when the prior day's return is significant, i.e., Fed didn't hike as expected.

Potential Triggers: 1) Run a regression of XP1 return on SPX return (potentially can include CL1 and TSX as regressors too) and normalize residuals to z-scores. Long term wise the correlation should be stable and significant but short term wise prices deviate.
                       Specifically, we sell XP1 and buy ES1 as hedge when residual z-score > 1 std and buy XP1 and sell ES1 as hedge when residual z-score < -1 std, hoping the gap will close. Might also need to stop loss at +/-2 std meaning structure temporarily breaks.   
                    2) Just use intraday SPX returns as the trigger, i.e., Close Price / Open Price - 1, normalize it to a z-score. Assuming that right at ASX open, the market hasn't fully comprehended what happend overnight, and will underreact.
                       If z-score is greater than 1, there was very positive news and we sell XP1 at SPX close and buy it back at ASX open. If z-score is less than -1, there was very negative news and we buy XP1 at SPX close and sell it at ASX open.

There are clearly cases where SPX went down overnight and ASX goes up once market opens. And even if the second trigger makes any sense, this cannot be converted to a 24hrs strategy, since mostly all equity index futures stop trading with US and resumes after a few hours. And the longer the gap, the more unpredictable the open price is.
So maybe instead of fasicating on the trading gap, which maybe just an exaggerated case for price anomaly, we try trigger 1) first.

Implementation Steps: 1) For a given future contract ES1/XP1, identify a set of equity indices as regressors to cover its all trading hours, i.e., ASX - Nikkie - HSI/Kospi - India - Euro Stoxx - SPX/Nasdaq
                      2) Run piecewise regression of historical ES1/XP1 returns independently on different equity index historical returns and look for stable and significant correlations during same trading hours, beta coefficients and residual distributions per se.
                      3) Use these to calculate real time y_hat and residual and z-score of residual and use this as main signal. This can also be used as certainty measure, meaning the wider the gap, the more likely it will come back soon. T-stats on beta coefficient is also measure of certainty, higher t-stat means more stability.
                      4) For example, ES1 tracks Euro Stoxx closely before US opens, if residual is greater than 1 std we can sell ES1 and buy VG1 as hedge and exit the trade when the gap disappears. Hedge ratio determined by beta.
                                      ES1 tracks Nikkie/Topix/Kospi/HSI more or less too during Asia hours, if residual is greater than maybe 1.5 std we can sell ES1 and buy NK1/TP1/KM1/HI1 as hedge.
                      5) Replicate this to other indices.

Sensitivity Test: 1) Market Volatility: regression assume constant variance, changing volatility impacts accuracy and certainty of y_hat and residual. Higher volatility means more opportunities but probably shorter execution window.
                  2) Liquidity / Volume: how much capacity there is for this trade, can we really execute the trade without moving the market
                  3) Model responce speed, execution algo
                  4) Entry/exit signal threshold
