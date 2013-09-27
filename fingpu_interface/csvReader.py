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
        self.interest_rate_data = []

    def loadSettingsFile(self, filename, path, statusBar):
        self.data_path = ''.join(path+'/')
        #~ print(self.data_path)
        myfile = open(filename, "rb")

        # reads in number input and output files
        self.num_input_files = int(myfile.next().split(':')[1].split(';')[0].strip())
        self.num_output_files = int(myfile.next().split(':')[1].split(';')[0].strip())
        # print(self.num_output_files)

        self.time_span = []
        for x in xrange(1,32):
            self.time_span.append(x)
        myfile.close()

        # Read in all data for greeks
        for x in xrange(0, self.num_output_files):
            self.loadOutputFile('outputs_'+str(x)+'.csv')

        self.loadInputFile('inputs.csv')
        statusBar.SetStatusText("Importing data complete.")
        return self.time_span

    def loadOutputFile(self, filename):
        ifile = open(''.join(self.data_path+filename), "rb")
        myfile = csv.reader(ifile)
        put_temp_data = []
        call_temp_data = []
        counter = 0

        # reads in alternate lines to relevant arrays(splitting call and put option data)
        for row in myfile:
            row.pop(1)
            if counter % 2 == 0:
                put_temp_data.append(row)
            else:
                call_temp_data.append(row)
            counter += 1
        put_temp_data.pop(0) # remove headers for each column

        self.put_option_data.append(put_temp_data)
        self.call_option_data.append(call_temp_data)

        # put_option_data = map(float, put_option_data)
        # call_option_data = map(float, call_option_data)
        # print(self.put_option_data)
        ifile.close()

    def loadInputFile(self, filename):
        ifile = open(''.join(self.data_path+filename), "rb")
        myfile = csv.reader(ifile)
        self.stock_price_data = []
        self.interest_rate_data = []
        counter = 0

        # retrieve input data
        for row in myfile:
            # get stock prices
            if counter >= 15 and counter <= 45:
                self.stock_price_data.append(row[0].split(' ')[1])

            # get interest rates
            if counter >= 46 and counter <= 76:
                self.interest_rate_data.append(row[0].split(' ')[1])

            counter += 1
        # map(float, self.stock_price_data)
        # print(self.interest_rate_data)
        ifile.close()

    def getOptionPrice(self, useCallOptionData=True, viewOptionPriceValues=True):
        temp = []
        tempOption = []
        if viewOptionPriceValues:
            if useCallOptionData:
                for call_option in self.call_option_data:
                    for call in call_option:
                        tempOption.append(call[1])
                    temp.append(tempOption)
                    tempOption = []
            else:
                for put_option in self.put_option_data:
                    for put in put_option:
                        tempOption.append(put[1])
                    temp.append(tempOption)
                    tempOption = []
        return temp

    def getDeltaValues(self, useCallOptionData=True, viewDeltaValues=True, viewDifference=False):
        temp = []
        tempDelta = []
        if viewDeltaValues:
            if useCallOptionData:
                for call_option_file in self.call_option_data:
                    for call_option in call_option_file:
                        stock_index = int(call_option[0])-1
                        greek_value = float(call_option[2])

                        if stock_index < 30:
                            s1 = float(self.stock_price_data[stock_index])
                            s2 = float(self.stock_price_data[stock_index+1])
                            greek_value = greek_value*(s2-s1) # calculate delta effect relative to option price
                            
                            if viewDifference:
                                tempDelta.append(greek_value)
                            else:
                                tempDelta.append(greek_value+float(call_option[1]))
                        else:
                            tempDelta.append(0)
                    temp.append(tempDelta)
                    tempDelta = []
            else:
                for put_option_file in self.put_option_data:
                    for put_option in put_option_file:
                        stock_index = int(put_option[0])-1
                        greek_value = float(put_option[2])

                        if stock_index < 30:
                            s1 = float(self.stock_price_data[stock_index])
                            s2 = float(self.stock_price_data[stock_index+1])
                            greek_value = greek_value*(s2-s1) # calculate delta effect relative to option price
                            if viewDifference:
                                tempDelta.append(greek_value)
                            else:                            
                                tempDelta.append(greek_value+float(put_option[1]))
                        else:
                            tempDelta.append(0)
                    temp.append(tempDelta)
                    tempDelta = []
        return temp

    def getGammaValues(self, useCallOptionData, viewGammaValues=True, viewDifference=False):
        temp = []
        tempGamma = []
        if viewGammaValues:
            if useCallOptionData:
                for call_option_file in self.call_option_data:
                    for call_option in call_option_file:
                        stock_index = int(call_option[0])-1
                        gamma = float(call_option[3])
                        if stock_index < 30:
                            s1 = float(self.stock_price_data[stock_index])
                            s2 = float(self.stock_price_data[stock_index+1])
                            gamma = gamma*(s2-s1) # calculate gamma effect relative to option price
                            if viewDifference:
                                tempGamma.append(gamma)
                            else:
                                tempGamma.append(gamma+float(call_option[1]))
                        else:
                            tempGamma.append(0)
                    temp.append(tempGamma)
                    tempGamma = []
            else:
                for put_option_file in self.put_option_data:
                    for put_option in put_option_file:
                        stock_index = int(put_option[0])-1
                        greek_value = float(put_option[3])
                        if stock_index < 30:
                            s1 = float(self.stock_price_data[stock_index])
                            s2 = float(self.stock_price_data[stock_index+1])
                            greek_value = greek_value*(s2-s1) # calculate gamma effect relative to option price
                            if viewDifference:
                                tempGamma.append(greek_value)
                            else:
                                tempGamma.append(greek_value+float(put_option[1]))
                        else:
                            tempGamma.append(0)
                    temp.append(tempGamma)
                    tempGamma = []
        return temp

    def getVegaValues(self, useCallOptionData, viewVegaValues=True, viewDifference=False):
        temp = []
        tempVega = []
        if viewVegaValues:
            if useCallOptionData:
                for call_option_file in self.call_option_data:
                    for call_option in call_option_file:
                        stock_index = int(call_option[0])-1
                        greek_value = float(call_option[4])

                        if stock_index < 30:
                            greek_value = greek_value*0  # In this option price model the volatility does not change, so the effect is zero
                            if viewDifference:
                                tempVega.append(greek_value)
                            else:
                                tempVega.append(greek_value+float(call_option[1]))
                        else:
                            tempVega.append(0)
                    temp.append(tempVega)
                    tempVega = []
            else:
                for put_option_file in self.put_option_data:
                    for put_option in put_option_file:
                        stock_index = int(put_option[0])-1
                        greek_value = float(put_option[4])

                        if stock_index < 30:
                            greek_value = greek_value*(s2-s1)  # In this option price model the volatility does not change, so the effect is zero
                            if viewDifference:
                                tempVega.append(greek_value)
                            else:
                                tempVega.append(greek_value+float(put_option[1]))
                        else:
                            tempVega.append(0)
                    temp.append(tempVega)
                    tempVega = []
        return temp

    def getThetaValues(self, useCallOptionData, viewThetaValues=True, viewDifference=False):
        temp = []
        tempTheta = []
        if viewThetaValues:
            if useCallOptionData:
                for call_option_file in self.call_option_data:
                    for call_option in call_option_file:
                        greek_value = float(call_option[5])/365
                        if viewDifference:
                            tempTheta.append(greek_value)
                        else:
                            tempTheta.append(greek_value+float(call_option[1]))
                    temp.append(tempTheta)
                    tempTheta = []
            else:
                for put_option_file in self.put_option_data:
                    for put_option in put_option_file:
                        greek_value = float(put_option[5])
                        if viewDifference:
                            tempTheta.append(greek_value)
                        else:
                            tempTheta.append(greek_value+float(put_option[1]))
                    temp.append(tempTheta)
                    tempTheta = []
        return temp

    def getRhoValues(self, useCallOptionData, viewRhoValues=True, viewDifference=False):
        temp = []
        tempRho = []
        if viewRhoValues:
            if useCallOptionData:
                for call_option_file in self.call_option_data:
                    for call_option in call_option_file:
                        r_index = int(call_option[0])-1
                        greek_value = float(call_option[6])
                        if r_index < 30:
                            s1 = float(self.interest_rate_data[r_index])
                            s2 = float(self.interest_rate_data[r_index+1])
                            greek_value = greek_value*(s2-s1) # calculate rho effect relative to option price
                            if viewDifference:
                                tempRho.append(greek_value)
                            else:
                                tempRho.append(greek_value+float(call_option[1]))
                        else:
                            tempRho.append(0)
                    temp.append(tempRho)
                    tempRho = []
            else:
                for put_option_file in self.put_option_data:
                    for put_option in put_option_file:
                        r_index = int(put_option[0])-1
                        greek_value = float(put_option[6])
                        if r_index < 30:
                            s1 = float(self.interest_rate_data[r_index])
                            s2 = float(self.interest_rate_data[r_index+1])
                            greek_value = greek_value*(s2-s1) # calculate rho effect relative to option price
                            if viewDifference:
                                tempRho.append(greek_value)
                            else:
                                tempRho.append(greek_value+float(put_option[1]))
                        else:
                            tempRho.append(0)
                    temp.append(tempRho)
                    tempRho = []
        return temp
