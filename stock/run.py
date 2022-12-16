import predict
# Uber, Bitcoin, Ethereum, NASDAQ, Gold
stocks = ['UBER','BTC-USD','ETH-USD','^IXIC','GC=F']

# X - labels for x axis, 21 values
# Y - last value in the list is predicted, first 20 values are actual data
x, y = predict.predict('UBER')



print(x)
print(y)