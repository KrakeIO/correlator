# The Correlator
A simple python service that establishes correlations between different categories of time series. In this scenario, it is applied to sentiment of name entities covered in news and price movement of publicly traded companies on NYSE and Nasdaq.

# Resources
- [daily trades data file](https://s3.amazonaws.com/correlator.getdata.io/test-files/daily_trades.csv)
- [daily summaries data file](https://s3.amazonaws.com/correlator.getdata.io/test-files/daily_summaries.csv)

# Setting up
Installing virtual environment
```
pip install virtualenv 

# Run to make sure its been installed
which virtualenv
```

Setting up virtual environment
```
mkdir venv
virtualenv venv
```

Activating into virtual environment
```
source venv/bin/activate
```

Installing libraries used within package
```
pip install -r requirements.txt
```