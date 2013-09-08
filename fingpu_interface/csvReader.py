"""
    CSV file reader
    stores the file data for the options and provides getters to retrieve relevant data

    by Nathan Floor
    flrnat001@cs.uct.ac.za
"""

import csv

class Reader():
    global put_option_data
    global call_option_data
    global stock_price_data

    stock_price_data = []
    put_option_data = []
    call_option_data = []

    def loadOutputFile(self, filename):
        ifile = open(filename, "rb")
        myfile = csv.reader(ifile)
        global put_option_data, call_option_data
        put_option_data = []
        call_option_data = []
        counter = 0

        # reads in alternate lines to relevant arrays(splitting call and put option data)
        for row in myfile:
            row.pop(1)
            if counter % 2 == 0:
                put_option_data.append(row)
            else:
                call_option_data.append(row)
            counter += 1
        put_option_data.pop(0) # remove headers for each column
        # map(float, put_option_data)
        # map(float, call_option_data)
        # print(put_option_data)
        ifile.close()

    def loadInputFile(self, filename):
        ifile = open(filename, "rb")
        myfile = csv.reader(ifile)
        global stock_price_data
        stock_price_data = []
        counter = 0

        # retrieve input data
        for row in myfile:
            # get stock prices
            if counter >= 13 and counter <= 42:
                stock_price_data.append(row[0].split(' ')[1])
            counter += 1
        map(float, stock_price_data)
        ifile.close()

    def getCount(self):
        global put_option_data
        global call_option_data
        return len(put_option_data)+len(call_option_data)

    def getOptionPrice(self, useCallOptionData=True):
        global call_option_data, put_option_data
        temp = []
        if useCallOptionData:
            for call_option in call_option_data:
                temp.append(call_option[1])
        else:
            for put_option in put_option_data:
                temp.append(put_option[1])
        return temp

    def getDeltaValues(self, useCallOptionData, viewDeltaValues=True):
        global stock_price_data
        temp = []
        if viewDeltaValues:
            global call_option_data, put_option_data
            if useCallOptionData:
                for call_option in call_option_data:
                    stock_index = map(int, call_option[0])[0]
                    # print(call_option[3])
                    # delta = map(float, call_option[3])[0]

                    t = stock_price_data[stock_index+1]
                    x = stock_price_data[stock_index]
                    delta = call_option[3]*(0)
                    temp.append(delta)
                    # print(stock_price_data[call_option[0]+1])
            else:
                for put_option in put_option_data:
                    temp.append(put_option[3]*(stock_price_data[put_option[0]+1]-
                        stock_price_data[put_option[0]]))
        return temp

    def getGammaValues(self, useCallOptionData, viewGammaValues=True):
        temp = []
        if viewGammaValues:
            global call_option_data, put_option_data
            if useCallOptionData:
                for call_option in call_option_data:
                    temp.append(call_option[4])
            else:
                for put_option in put_option_data:
                    temp.append(put_option[4])
        return temp

    def getVegaValues(self, useCallOptionData, viewVegaValues=True):
        temp = []
        if viewVegaValues:
            global call_option_data, put_option_data
            if useCallOptionData:
                for call_option in call_option_data:
                    temp.append(call_option[5])
            else:
                for put_option in put_option_data:
                    temp.append(put_option[5])
        return temp

    def getThetaValues(self, useCallOptionData, viewThetaValues=True):
        temp = []
        if viewThetaValues:
            global call_option_data, put_option_data
            if useCallOptionData:
                for call_option in call_option_data:
                    temp.append(call_option[6])
            else:
                for put_option in put_option_data:
                    temp.append(put_option[6])
        return temp

    def getRhoValues(self, useCallOptionData, viewRhoValues=True):
        temp = []
        if viewRhoValues:
            global call_option_data, put_option_data
            if useCallOptionData:
                for call_option in call_option_data:
                    temp.append(call_option[7])
            else:
                for put_option in put_option_data:
                    temp.append(put_option[7])
        return temp
