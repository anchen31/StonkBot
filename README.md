(Work in Progress)
This uses Ib_insync which is a 3rd party API for Interactive brokers. 

Stonk bot implements the use of pulling data from the API and storing it in a pandas dataframe for easy manipulation.
Alongside Pandas, Stonk bot also usese matplot lib for visualization of the data and graphs.
With all of this data, it will be wrapped into a tkinter GUI for easy use

What it can currently do-
*connect to interactive brokers via API
*pull live data and buy and sell
*have proper risk management and position sizing abilities
*live data and updating graphs that are up to date.

What I am currently working on-
*create pivot points for the graphs and use those points for machine learning
*will use linear regression on these pivot points to create support and resistance lines
*will implement a nerual network or an artifical intelligence solution to buy/sell automatically.

How it looks, hope you enjoy!

![Screenshot (77)](https://user-images.githubusercontent.com/42586375/101235017-85489000-3679-11eb-958d-c3782484d2f9.png)
