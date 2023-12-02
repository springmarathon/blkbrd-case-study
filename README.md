# blkbrd-case-study
All timestamps below are US local time during summer hours, before daylight saving change.

Hypothesis: During US hours, i.e., 9:30 to 16:00, international equity index futures move together with US market.
            Take SPX and XP1 as an example, if SPX goes up, XP1 most likely will go up during US trading hours. Then SPX closes and XP1 stops trading 1 hour after that at 17:00. And XP1 normally doesn't move much during that 1 hour since no major markets open and short time frame.
            When XP1 reopens at 19:00 PM with ASX. Same assumption as above that no major markets open so little new information. The positive return on SPX of the prior night will take time to reflect on ASX market and creating short term arbitrage opportunities.

Potential Triggers: 1) SPX returns, i.e., Close Price / Open Price - 1, normalize it to a z-score. Assuming that right at ASX open, the market hasn't fully comprehended what happend overnight, and will underreact.
                       If z-score is greater than 1, there was very positive news and we sell XP1 at SPX close and buy it back at ASX open. If z-score is less than -1, there was very negative news and we buy XP1 at SPX close and sell it at ASX open.

                    2) Run a regression of XP1 return on SPX return and get beta coefficient, y_hat and residuals. The idea is y_hat should be fair value of XP1 if the market has consolidated all information and fully understood the impact on ASX market.
                       But if the actual value of XP1 return deviates too much from its fair value, y_hat, measured by normalized residual, then we'd expect XP1 will return to its fair value shortly after ASX opens since the market will have enough time to absort all the information by then.

Sensitivity Test: 1) Market Volatility
