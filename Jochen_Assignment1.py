#!/usr/bin/env python 
# api documentation: 
# using 

from tkinter import *
from tkinter import Tk
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 

        
# master belongs to the root, so the TK class. We renamed it master
class StockPrice:
    def __init__(self, master, api_key):
        self.master = master
        self.master.title("Stock Price")
        self.api_key = api_key
        self.master.config(bg='white')
        self.master.geometry("450x300") 

        self.stock_label = Label(self.master, text = 'Please Enter Desired Stock Price',  bg='white', fg='pink',\
            font=('comic sans ms', 16, 'bold'))
        self.stock_label.grid(column=1, row=1, padx=8, pady=10)

        self.symbol = StringVar()
        self.symbol_entry = Entry(self.master, width=8, textvariable=self.symbol, bd='4')
        self.symbol_entry.grid(column=2, row=1, sticky=(N, W, E, S), padx=8, pady=10)


        self.get_priceButton = Button(self.master, text="Get Price", command=self.return_price, height=2, bd='2',\
             highlightbackground='pink',activebackground='pink',activeforeground='pink',bg='pink', fg='white',font=('comic sans ms', 16, 'bold'))
        self.get_priceButton.grid(column=1, row=2, rowspan=3, columnspan=2, sticky=N+S+E+W, padx=20, pady=20)
        self.get_priceButton.bind("<Return>", self.return_price)

        self.get_plotButton = Button(self.master, text="Get Plot", command=self.return_plot, height=2, bd='2',\
             highlightbackground='pink',activeforeground='pink',bg='pink', fg='white',font=('comic sans ms', 16, 'bold'))
        self.get_plotButton.grid(column=1, row=6, rowspan=3, columnspan=2, sticky=N+S+E+W, padx=20, pady=20)
        self.get_plotButton.bind("<Return>", self.return_plot)

    def get_price(self, symbol):
        url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&interval=5min&apikey={}'.format(symbol, self.api_key)
        result =  requests.get(url) 
        result = result.json() 

        x = result['Global Quote']
        s = pd.Series(x)
        return s

    def return_price(self):
        
        symbol = '{}'.format(self.symbol.get())
        symbol = symbol.upper()
        self.s = self.get_price(symbol)
        price = self.s.loc['05. price']
        price = price[:-2]
        msg = 'Most recent closing price for {}: ${} USD.'.format(symbol, price)
        
        self.txt = Tk()
        self.txt.title('{} Stock Price'.format(symbol))
        mframe = Frame(self.txt)
        mframe.config(bg='white')
        mframe.grid(column=0, row=0, sticky=(N, W, E, S))
        Label(mframe, text=msg, bg='white', fg='pink',\
            font=('comic sans ms', 16, 'bold')).grid(column=0, row=1, padx=10, pady=20)
        

    def get_plot(self, symbol):
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(symbol, self.api_key)
        result =  requests.get(url) 
        result = result.json()
        data = result['Time Series (Daily)']
        df = pd.DataFrame(data)
        df = df.T
        df = df.reset_index().sort_values(by='index', ascending=True)

        fig = plt.figure(figsize=(5,5), dpi=100)
        price_plot = fig.add_subplot(111, label='FB', title='Daily Closing Price Over Last 100 Days')
        price_plot.plot(df['4. close'].astype('float').values)
        price_plot.set_xlabel('Time')
        price_plot.legend()

        return fig

    def return_plot(self):
        symbol = '{}'.format(self.symbol.get())
        symbol = symbol.upper()
        self.fig = self.get_plot(symbol)

        self.window = Tk()
        self.window.title('{} Stock Price'.format(symbol))
        self.window.config(bg='white')
        self.window.geometry("600x450")
        canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        

# this instantiates the "root" window - the main window in our app
# TK is a class that we are instantiating and naming it root
root = Tk()
#root.geometry("400x250") 
api_key = 'DV3EJEJUX8WGYPRW'
# must include root 
my_gui = StockPrice(root, api_key)
# method on the mainloop used to execute app. This method will loop forever waiting for events from
# the user until user exits the program or we terminate the program from the console
root.mainloop()

