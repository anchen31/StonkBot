import datetime
from ib_insync import *
import math

import pandas as pd

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

#gets the total account and the availible funds
for v in ib.accountValues():
    if v.tag == 'NetLiquidationByCurrency' and v.currency == 'USD':
        netLiquidationValue = float(v.value)
        print('Net Liquidation Value: ', netLiquidationValue)
    elif  v.tag == 'AvailableFunds' and v.currency == 'USD':
        availableFunds = float(v.value)
        print('Account Cash Value: ', availableFunds)

#create a method that makes a contract from user input

contract1 = Stock('TSLA', 'SMART', 'USD')

# do stock analysis with pandas here #######################################################################

bars = ib.reqHistoricalData(
        contract1,
        endDateTime='',
        durationStr='900 S',
        barSizeSetting='10 secs',
        whatToShow='MIDPOINT',
        useRTH=True,
        formatDate=1,
        keepUpToDate=True)

#pandas df
df1 = pd.DataFrame(bars, columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'average'])

#save to csv
csv = df1.to_csv(contract1.symbol + '.csv')





#float that takes in supp/ resistance aka stop loss
stopLoss = 0

#write something that takes risk size from people and appends it to the graph
riskSize = 0.02

#calculates how much the price of the stock is 
def SharePrc():
    ib.reqMktData(contract1, '', False, False)
    ticker = ib.ticker(contract1)
    ib.sleep(1)
    sPrice = ticker.marketPrice()
    return sPrice


#calculates short position size
def LpositionSize():
    #loss per share
    LPs = (SharePrc() - stopLoss)
    #how much willing to risk per trade
    maxLoss = (netLiquidationValue * riskSize)
    #still haveto test this method out with SharePrc
    Shrs = (maxLoss / LPs)
    shares = math.floor(Shrs / 10.0) * 10.0

    return shares

#calculates short position size
def SpositionSize():
    #loss per share
    LPs = (stopLoss - SharePrc())
    #how much willing to risk per trade
    maxLoss = (netLiquidationValue * riskSize)
    #still haveto test this method out with SharePrc
    Shrs = (maxLoss / LPs)
    shares = math.floor(Shrs / 10.0) * 10.0

    return shares

#stop losses
def LstopOrder(stopLoss):
    ib.qualifyContracts(contract1)
    LstopOrder.order = LimitOrder('SELL', LpositionSize(), stopLoss)
    ib.placeOrder(contract1, LstopOrder.order)

def SstopOrder(stopLoss):
    ib.qualifyContracts(contract1)
    SstopOrder.order = LimitOrder('BUY', SpositionSize(), stopLoss)
    ib.placeOrder(contract1, SstopOrder.order)

#long and short orders
def LngOrder(pSize):
    ib.qualifyContracts(contract1)
    LngOrder.order = MarketOrder('BUY', pSize)
    ib.placeOrder(contract1, LngOrder.order)

def ShrOrder(pSize):
    ib.qualifyContracts(contract1)
    ShrOrder.order = MarketOrder('SELL', pSize)
    ib.placeOrder(contract1, ShrOrder.order)


def main():
    #get stop loss from user
    #float that takes in supp/ resistance ##########################################################################
    stopLoss = input("enter your stop loss")
    x = True
    while x == True:
        print("'b' to buy, 's' to sell, 'disconnect' to stop program and liquidate assets")
        #loop through options
        y = input()
        if y == 's':
            pSize = SpositionSize()
            ShrOrder(pSize)
            SstopOrder(stopLoss)
            #the user can cancel order, exit the trade, or stop program after liquidating positions
            #try to eventually check by pct gain 
            user = True
            print("'e' to exit the trade and liquidate assets")
            while user == True:
                if user == 'e':
                    print("trade exited")
                    LngOrder(pSize)
                    user == False
                else:
                    print("enter a valid order")
            #after the loop is finished, it removes the stop loss
            ib.cancelOrder(SstopOrder.order)

        elif y == 'b':
            pSize = LpositionSize()
            LngOrder(pSize)
            LstopOrder(stopLoss)
            #the user can cancel order, exit the trade, or stop program after liquidating positions
            user = True 
            print("'c' to cancel order, 'e' to exit the trade and liquidate assets")
            while user == True:
                if user == 'e':
                    print("trade cancelled")
                    ib.cancelOrder(LngOrder.order)
                    user == False
                else:
                    print("enter a valid order")
            #after the loop is finished, it removes the stop loss
            ib.cancelOrder(LstopOrder.order)

        elif y == 'disconnect':
            ib.disconnect()
            x = False


if __name__ == "__main__":
    main()








