import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import style

import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc

import tkinter as tk
from tkinter import ttk

import urllib
import json

import pandas as pd
import numpy as np


LARGE_FONT = ("verdana", 12)
NORM_FONT = ("verdana", 10)
SMALL_FONT = ("verdana", 8)

style.use("ggplot")

fig, ax1 = plt.subplots(figsize = (12,6))

Strat = "None"
#counter to force a update
counter = 9000
ProgramName = "Bo"

resampleSize = "5Min"
DataPace = "tick"
candleWidth = 0.008

paneCount = 1

topIndicator = "none"
bottomIndicator = "none"
middleIndicator = "none"
chartLoad = True

lightColor = "00A3E0"
darkColor = "1883A54"

EMAs = []
SMAs = []

def loadChart(run):
	global chartLoad

	if run =="start":
		chartLoad = True

	elif run == "stop":
		chartLoad = False

def addMiddleIndicator(what):
    global middleIndicator
    global counter

    if what != "none":
    	if middleIndicator == "none":
    		if what == "sma":
    			midIQ = tk.Tk()
    			midIQ.wm_title("periods?")
    			label = ttk.Label(midIQ, text="choose how many periods you want your SMA to be")
    			label.pack(side="top", fill="x", pady=10)
    			e = ttk.Entry(midIQ)
    			e.insert(0, 20)
    			e.pack()
    			e.focus_set()

    			def callback():
    				global middleIndicator
    				global counter

    				middleIndicator = []
    				periods = (e.get())
    				group = []
    				group.append("sma")
    				group.append(int(periods))
    				middleIndicator.append(group)
    				counter = 9000
    				prtin("middle indicator set to: ", middleIndicator)
    				midIQ.destroy()

    			b = ttk.Button(midIQ, text="submit", width=10, command=callback)
    			b.pack()
    			tk.mainloop()

    		if what == "ema":
    			midIQ = tk.Tk()
    			midIQ.wm_title("periods?")
    			label = ttk.Label(midIQ, text="choose how many periods you want your EMA to be")
    			label.pack(side="top", fill="x", pady=10)
    			e = ttk.Entry(midIQ)
    			e.insert(0, 9)
    			e.pack()
    			e.focus_set()

    			def callback():
    				global middleIndicator
    				global counter

    				middleIndicator = []
    				periods = (e.get())
    				group = []
    				group.append("ema")
    				group.append(int(periods))
    				middleIndicator.append(group)
    				counter = 9000
    				prtin("middle indicator set to: ", middleIndicator)
    				midIQ.destroy()

    			b = ttk.Button(midIQ, text="submit", width=10, command=callback)
    			b.pack()
    			tk.mainloop()


    	else:
    		if what == "ema":
    			midIQ = tk.Tk()
    			midIQ.wm_title("periods?")
    			label = ttk.Label(midIQ, text="choose how many periods you want your EMA to be")
    			label.pack(side="top", fill="x", pady=10)
    			e = ttk.Entry(midIQ)
    			e.insert(0, 10)
    			e.pack()
    			e.focus_set()

    			def callback():
    				global middleIndicator
    				global counter

    				#middleIndicator = []
    				periods = (e.get())
    				group = []
    				group.append("sma")
    				group.append(int(periods))
    				middleIndicator.append(group)
    				counter = 9000
    				prtin("middle indicator set to: ", middleIndicator)
    				midIQ.destroy()

    			b = ttk.Button(midIQ, text="submit", width=10, command=callback)
    			b.pack()
    			tk.mainloop()

    else:
    	middleIndicator = "none"

def addTopIndicator(what):
    global topIndicator
    global counter

    if DataPace == "tick":
    	popupmsg("Indicators in Tick Data not available.")

    elif what == "none":
    	topIndicator = what
    	counter = 9000

#create a enter box can be used for stock entering 
    elif what == "rsi":
    	rsiQ = tk.Tk()
    	rsiQ.wm_title("Periods?")
    	label = ttk.Label(rsiQ, text = "Choose how many periods you want each RSI calculation to consider.")
    	label.pack(side="top", fill="x", pady=10)

    	e = ttk.Entry(rsiQ)
    	e.insert(0,14)
    	e.pack()
    	e.focus_set()

    	def callback():
    		global topIndicator
    		global counter

    		periods = (e.get())
    		group = []
    		group.append("rsi")
    		group.append(periods)

    		topIndicator = group
    		counter = 9000
    		print("Set top indicator to",group)
    		rsiQ.destroy()

    	b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
    	b.pack()
    	tk.mainloop()

    elif what == "macd":
    	topIndicator
    	counter
    	topIndicator = "macd"
    	counter = 9000

def addBottomIndicator(what):
    global bottomIndicator
    global counter

    if DataPace == "tick":
    	popupmsg("Indicators in Tick Data not available.")

    elif what == "none":
    	bottomIndicator = what
    	counter = 9000

#create a enter box can be used for stock entering 
    elif what == "rsi":
    	rsiQ = tk.Tk()
    	rsiQ.wm_title("Periods?")
    	label = ttk.Label(rsiQ, text = "Choose how many periods you want each RSI calculation to consider.")
    	label.pack(side="top", fill="x", pady=10)

    	e = ttk.Entry(rsiQ)
    	e.insert(0,14)
    	e.pack()
    	e.focus_set()

    	def callback():
    		global bottomIndicator
    		global counter

    		periods = (e.get())
    		group = []
    		group.append("rsi")
    		group.append(periods)

    		bottomIndicator = group
    		counter = 9000
    		print("Set bottom indicator to",group)
    		rsiQ.destroy()

    	b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
    	b.pack()
    	tk.mainloop()

    elif what == "macd":
    	bottomIndicator
    	counter
    	bottomIndicator = "macd"
    	counter = 9000




def changeTimeFrame(tf):
	global DataPace
	if tf =="7d" and resampleSize == "1Min":
		popupmsg("Too much data chosen, choose a smaller time frame or higher OHLC interval")
	else:
		DataPace = tf
		counter = 9000


def changeSampleSize(size,width):
	global resampleSize
	global candleWidth
	if DataPace == "7d" and resampleSize =="1Min":
		popupmsg("Too much data chosen, choose a smaller time frame or higher OHLC interval")
	elif DataPace == "tick":
		popupmsg("You're currently viewing tick data, not OHLC")
	else:
		resampleSize = size
		counter = 9000
		candleWidth = width

#pn stands for program name
def changeStrategy(StratName, Pn):
	global Strat
	global counter
	global programName

	Strat = StratName
	ProgramName = Pn
	counter= 9000

def popupmsg(msg):
	popup = tk.Tk()
	popup.wm_title("!")
	label = ttk.Label(popup, text=msg, font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10)
	B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
	B1.pack()
	popup.mainloop()

def animate(i):
	global refreshRate
	global counter

	if chartLoad:
		if paneCount ==1:
			if DataPace =="tick":
				try:
					if Strat == "None":
						ax1 = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
						ax2 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex=ax1)
						#eventually going to pull the csv from ib
						datafile = 'C:/Users/andyc/AppData/Roaming/Sublime Text 3/Packages/User/pp for finance/tsla.csv'
						data = pd.read_csv(datafile, index_col = 'Date')
						data.index = pd.to_datetime(data.index)
						dvalues = data[['Open', 'High', 'Low', 'Close', 'Volume']].values.tolist()
						vol = data['Volume']
						price = data['Close']
						pdates = mdates.date2num(data.index)
						ohlc = [ [pdates[i]] + dvalues[i] for i in range(len(pdates)) ]
						sma20 = data['Close'].rolling(20).mean()
						ema9 = data['Close'].ewm(9).mean()

						ax1.clear()
						#ax1.plot_date(date, price, "g", label="open")
						candlestick_ohlc(ax1, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')
						ax1.plot_date(data.index, sma20, "g", label="SMA20")
						ax1.plot_date(data.index, ema9, "b", label="EMA9")
						ax2.fill_between(pdates, 0, vol)

						ax1.xaxis.set_major_locator(mticker.MaxNLocator(5))
						plt.setp(ax1.get_xticklabels(), visible = False)
						ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %y'))




						title = "Tsla open prices\nLast Price : " + str(price[-1])
						ax1.set_title(title)					
					elif Strat == "Breakout":
						#will eventually have an automated strategy
						popupmsg("not available yet")

					elif Strat == "PullBack":
						#will eventually have an automated strategy
						popupmsg("not available yet")

					elif Strat == "Supernova":
						#will eventually have an automated strategy
						popupmsg("not available yet")

				except Exception as e:
					print("failed because of: ", e)


					#this is the reason why the graph changes when its other than tick data
			else:
				if counter > 12:
					try:
						
						if topIndicator != "none" and bottomIndicator != "none":
							# Main Graph
							ax1 = plt.subplot2grid((6,4), (1,0), rowspan=3, colspan=4)
							# Volume
							ax2 = plt.subplot2grid((6,4), (4,0), sharex=ax1, rowspan=1, colspan=4)
							# Bottom Indicator
							ax3 = plt.subplot2grid((6,4), (5,0), sharex=ax1, rowspan=1, colspan=4)
							# Top Indicator
							ax0 = plt.subplot2grid((6,4), (0,0), sharex=ax1, rowspan=1, colspan=4)

						elif topIndicator != "none":
							# Main Graph
							ax1 = plt.subplot2grid((6,4), (1,0), rowspan=3, colspan=4)
							# Volume
							ax2 = plt.subplot2grid((6,4), (4,0), sharex=ax1, rowspan=1, colspan=4)
							# Top Indicator
							ax0 = plt.subplot2grid((6,4), (0,0), sharex=ax1, rowspan=1, colspan=4)

						elif bottomIndicator != "none":
							# Main Graph
							ax1 = plt.subplot2grid((6,4), (1,0), rowspan=3, colspan=4)
							# Volume
							ax2 = plt.subplot2grid((6,4), (4,0), sharex=ax1, rowspan=1, colspan=4)
							# Bottom Indicator
							ax3 = plt.subplot2grid((6,4), (5,0), sharex=ax1, rowspan=1, colspan=4)
						else:
							# Main Graph
							ax1 = plt.subplot2grid((6,4), (1,0), rowspan=3, colspan=4)
							# Volume
							ax2 = plt.subplot2grid((6,4), (4,0), sharex=ax1, rowspan=1, colspan=4)

						#get the csv file from the api
						ax1 = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
						ax2 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex=ax1)
						#eventually going to pull the csv from ib
						datafile = 'C:/Users/andyc/AppData/Roaming/Sublime Text 3/Packages/User/pp for finance/tsla.csv'
						data = pd.read_csv(datafile, index_col = 'Date')
						data.index = pd.to_datetime(data.index)
						dvalues = data[['Open', 'High', 'Low', 'Close', 'Volume']].values.tolist()
						vol = data['Volume']
						pdates = mdates.date2num(data.index)
						ohlc = [ [pdates[i]] + dvalues[i] for i in range(len(pdates)) ]
						sma20 = data['Close'].rolling(20).mean()
						ema9 = data['Close'].ewm(9).mean()


						ax1.clear()
						#ax1.plot_date(date, price, "g", label="open")
						candlestick_ohlc(ax1, ohlc, width=0.4)
						ax1.plot_date(data.index, sma20, "g", label="SMA20")
						ax1.plot_date(data.index, ema9, "b", label="EMA9")
						ax2.fill_between(pdates, 0, vol, facecolor = "#138A54")

						ax1.xaxis.set_major_locator(mticker.MaxNLocator(5))
						plt.setp(ax1.get_xticklabels(), visible = False)
						ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %y'))
					

					except Exception as e:
						print("failed in the non-tick animate:", str(e))


class StonkBot(tk.Tk):
#init will always run first thing when a class is called
#args is arguments
#kwargs is keyword arguments, passing through dictionaries
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		tk.Tk.wm_title(self, "Stonk Bot")

		container = ttk.Frame(self)

		container.pack(side="top", fill="both", expand = True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)


		menuBar = tk.Menu(container)
		fileMenu = tk.Menu(menuBar, tearoff=0)
		fileMenu.add_command(label='Save settings', command = lambda: popupmsg("Not supported just yet!"))
		fileMenu.add_separator()
		fileMenu.add_command(label="Exit", command=quit)
		menuBar.add_cascade(label="File", menu=fileMenu)

		stratChoice = tk.Menu(menuBar, tearoff=1)

		stratChoice.add_command(label="None", command=lambda: popupmsg("This will result in manual trading"))


		#stratChoice.add_command(label="Breakout", command=lambda: changeStrategy("Breakout", "Bo"))
		stratChoice.add_command(label="Breakout", command=lambda: popupmsg("not available yet"))
		#stratChoice.add_command(label="PullBack", command=lambda: changeStrategy("PullBack", "Pb"))
		stratChoice.add_command(label="PullBack", command=lambda: popupmsg("not available yet"))
		#stratChoice.add_command(label="Supernova", command=lambda: changeStrategy("Supernova", "Sn"))
		stratChoice.add_command(label="Supernova", command=lambda: popupmsg("not available yet"))


		menuBar.add_cascade(label="Strat", menu=stratChoice)

		dataTF = tk.Menu(menuBar, tearoff=1)
		dataTF.add_command(label = "Tick",
							command=lambda: changeTimeFrame('tick'))
		dataTF.add_command(label = "1 Day",
							command=lambda: changeTimeFrame('1d'))
		dataTF.add_command(label = "3 Day",
							command=lambda: changeTimeFrame('3d'))
		dataTF.add_command(label = "1 Week",
							command=lambda: changeTimeFrame('7d'))
		menuBar.add_cascade(label = "Data Time Frame", menu = dataTF)

		OHLC = tk.Menu(menuBar, tearoff=1)
		OHLC.add_command(label = "Tick",
							command=lambda: changeTimeFrame('tick'))
		OHLC.add_command(label = "1 minute",
							command=lambda: changeSampleSize('1Min', 0.0005))
		OHLC.add_command(label = "5 minute",
							command=lambda: changeSampleSize('5Min', 0.0005))
		OHLC.add_command(label = "1 hour",
							command=lambda: changeSampleSize('60Min', 0.0005))

		menuBar.add_cascade(label="OHLC Interval", menu=OHLC)

		topIndi = tk.Menu(menuBar, tearoff=1)
		topIndi.add_command(label="None",
							command = lambda: addTopIndicator('none'))
		topIndi.add_separator()
		topIndi.add_command(label = "RSI",
								command=lambda: addTopIndicator('rsi'))
		topIndi.add_command(label = "MACD",
								command=lambda: addTopIndicator('macd'))

		menuBar.add_cascade(label = "Top Indicator", menu = topIndi)


		mainI = tk.Menu(menuBar, tearoff=1)
		mainI.add_command(label="None",
							command = lambda: addMiddleIndicator('none'))
		mainI.add_separator()
		mainI.add_command(label = "SMA",
								command=lambda: addMiddleIndicator('sma'))
		mainI.add_command(label = "EMA",
								command=lambda: addMiddleIndicator('ema'))
		
		menuBar.add_cascade(label = "Main/middle Indicator", menu = mainI)

		bottomI = tk.Menu(menuBar, tearoff=1)
		bottomI.add_command(label="None",
							command = lambda: addBottomIndicator('none'))
		bottomI.add_separator()
		bottomI.add_command(label = "RSI",
								command=lambda: addBottomIndicator('rsi'))
		bottomI.add_command(label = "MACD",
								command=lambda: addBottomIndicator('macd'))
		
		menuBar.add_cascade(label = "Bottom Indicator", menu = bottomI)


		tradeButton = tk.Menu(menuBar, tearoff=1)
		tradeButton.add_command(label = "Manual Trading",
								command=lambda: popupmsg("This is not live yet"))
		tradeButton.add_command(label = "Automated Trading",
								command=lambda: popupmsg("This is not live yet"))

		tradeButton.add_separator()
		tradeButton.add_command(label = "Quick Buy",
								command=lambda: popupmsg("This is not live yet"))
		tradeButton.add_command(label = "Quick Sell",
								command=lambda: popupmsg("This is not live yet"))

		tradeButton.add_separator()
		tradeButton.add_command(label = "set-up Quick Buy/Sell",
								command=lambda: popupmsg("This is not live yet"))

		menuBar.add_cascade(label="Trading", menu=tradeButton)

		startStop = tk.Menu(menuBar, tearoff = 1)
		startStop.add_command(label="Resume",
								command=lambda: loadChart('start'))
		startStop.add_command(label="Rause",
								command=lambda: loadChart('start'))
		menuBar.add_cascade(label = "Resume/Pause client", menu = startStop)






		tk.Tk.config(self, menu=menuBar)

		self.frames = {}

		for F in (StartPage, PageOne ,GraphPage):

			frame = F(container, self)

			self.frames[F] = frame

			#sticky is where it stretches nor sou ea w	
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	def show_frame(self, cont):

		frame = self.frames[cont]
		frame.tkraise()
		#####everything above here sets up for adding windows

class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text="Stonk Bot", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button = ttk.Button(self, text='View Trade History', 
							command=lambda: controller.show_frame(PageOne))
		button.pack()

		button3 = ttk.Button(self, text='Visit Graph Page', 
							command=lambda: controller.show_frame(GraphPage))
		button3.pack()

class PageOne(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text="Trade History", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button1 = ttk.Button(self, text='Back to Home', 
							command=lambda: controller.show_frame(StartPage))
		button1.pack()

class GraphPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text="Graph Page", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button1 = ttk.Button(self, text='Back to Home', 
							command=lambda: controller.show_frame(StartPage))
		button1.pack()

		canvas = FigureCanvasTkAgg(fig, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		toolbar = NavigationToolbar2Tk(canvas, self)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = StonkBot()
app.geometry("1000x800")
ani = animation.FuncAnimation(fig, animate, interval=5000)
app.mainloop()


