Imagine that you have started at a new trading company and they want to try trading Bitcoin. The trader has an idea for a simple strategy: for each day, calculate the 3-day moving average (MA) and 7-day moving average of the closing price. When the averages cross-over, the trader will buy or sell: if they cross-over and the 3-day MA is higher than the 7-day MA the trader will buy; if they cross over and the 3-day MA is lower then the 7-days MA the trader will sell; otherwise the trader will take no action.

To help test whether their strategy could succeed the trader needs to know the days in 2020 when they would have bought or sold. This is where you come in.

You should write a script in python that downloads the daily bitcoin prices. You can do this for free, without having to sign-up, at alphavantage.co
The script should calculate the 3-day and 7-day moving averages of the close prices for every day in 2020 and plot a chart of the closing price, 3-day MA and 7-day MA.
The script should also print a table of the BUY and SELL signals to the console in the following format:

```
|       Date | Signal |
|------------|--------|
| 2020-01-01 |    BUY |
| 2020-01-30 |   SELL |
|------------|--------|
```

We expect this task to take about 1 hour and you should spend no more than 2 hours on this task.

If you get to 2 hours and haven't finished, don't worry, just send us what you have so far and a note outlining what you were trying to do and how you approached the problem.

Send us your code and a `requirements.txt` file for any modules you need that aren't in the standard library.
