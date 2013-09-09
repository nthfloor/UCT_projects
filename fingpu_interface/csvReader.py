"""
    CSV file reader
    stores the file data for the options and provides getters to retrieve relevant data

    by Nathan Floor
    flrnat001@cs.uct.ac.za
"""

import csv

class Reader():
    def __init__(self):
        self.stock_price_data = []
        self.put_option_data = []
        self.call_option_data = []

    def loadSettingsFile(self, filename, path):
        self.data_path = ''.join(path+'/')
        myfile = open(filename, "rb")

        # reads in number input and output files
        self.num_input_files = myfile.next().split(':')[1].split(';')
        self.num_output_files = myfile.next().split(':')[1].split(';')

        myfile.close()

    def loadOutputFile(self, filename):
        ifile = open(''.join(self.data_path+filename), "rb")
        myfile = csv.reader(ifile)
        self.put_option_data = []
        self.call_option_data = []
        counter = 0

        # reads in alternate lines to relevant arrays(splitting call and put option data)
        for row in myfile:
            row.pop(1)
            if counter % 2 == 0:
                self.put_option_data.append(row)
            else:
                self.call_option_data.append(row)
            counter += 1
        self.put_option_data.pop(0) # remove headers for each column
        # map(float, put_option_data)
        # map(float, call_option_data)
        # print(put_option_data)
        ifile.close()

    def loadInputFile(self, filename):
        ifile = open(''.join(self.data_path+filename), "rb")
        myfile = csv.reader(ifile)
        self.stock_price_data = []
        counter = 0

        # retrieve input data
        for row in myfile:
            # get stock prices
            if counter >= 13 and counter <= 42:
                self.stock_price_data.append(row[0].split(' ')[1])
            counter += 1
        map(float, self.stock_price_data)
        ifile.close()

    def getOptionPrice(self, useCallOptionData=True):
        temp = []
        if useCallOptionData:
            for call_option in self.call_option_data:
                temp.append(call_option[1])
        else:
            for put_option in self.put_option_data:
                temp.append(put_option[1])
        return temp

    def getDeltaValues(self, useCallOptionData, viewDeltaValues=True):
        temp = []
        if viewDeltaValues:
            if useCallOptionData:
                for call_option in self.call_option_data:
                    stock_index = map(int, call_option[0])[0]
                    # print(call_option[2])
                    # delta = map(float, call_option[2])[0] TODO

                    t = self.stock_price_data[stock_index+1]
                    x = self.stock_price_data[stock_index]
                    delta = call_option[2]*x*t
                    # print(delta)
                    temp.append(delta)
                    # print(stock_price_data[call_option[0]+1])
            else:
                for put_option in self.put_option_data:
                    temp.append(put_option[3]*(self.stock_price_data[put_option[0]+1]-
                        self.stock_price_data[put_option[0]]))
        return temp

    def getGammaValues(self, useCallOptionData, viewGammaValues=True):
        temp = []
        if viewGammaValues:
            if useCallOptionData:
                for call_option in self.call_option_data:
                    temp.append(call_option[3])
            else:
                for put_option in self.put_option_data:
                    temp.append(put_option[3])
        return temp

    def getVegaValues(self, useCallOptionData, viewVegaValues=True):
        temp = []
        if viewVegaValues:
            if useCallOptionData:
                for call_option in self.call_option_data:
                    temp.append(call_option[5])
            else:
                for put_option in self.put_option_data:
                    temp.append(put_option[5])
        return temp

    def getThetaValues(self, useCallOptionData, viewThetaValues=True):
        temp = []
        if viewThetaValues:
            if useCallOptionData:
                for call_option in self.call_option_data:
                    temp.append(call_option[6])
            else:
                for put_option in self.put_option_data:
                    temp.append(put_option[6])
        return temp

    def getRhoValues(self, useCallOptionData, viewRhoValues=True):
        temp = []
        if viewRhoValues:
            if useCallOptionData:
                for call_option in self.call_option_data:
                    temp.append(call_option[7])
            else:
                for put_option in self.put_option_data:
                    temp.append(put_option[7])
        return temp
