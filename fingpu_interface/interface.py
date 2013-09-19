"""
    Main file for FinGPU visualisation interface
    Includes GUI and plotting code

    by Nathan Floor, flrnat001
    flrnat001@cs.uct.ac.za
"""

from __future__ import division, print_function

import wx
import os
import numpy
import matplotlib
import csvReader

matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas, NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm


class PlotFrame(wx.Frame):
    help_msg="""  Menus for
     Save           export figure (png, jpg) to file
     Open           import csv file of option prices
     Copy           copy bitmap of figure to the system clipboard
     Print Setup    setup size of figure for printing
     Print Preview  preview printer page
     Print          send figure to a system printer
     Exit           end application

     where 'figure' means an image of the matplotlib canvas

      In addition, "Ctrl-C" is bound to copy-figure-to-clipboard    
    """

    start_msg= """        Use Menus to test printing
        or Ctrl-C to copy plot image to clipboard  """

    about_msg="""        option_price_visual v0.1  29-Aug-2013
        Nathan Floor, flrnat001@cs.uct.ac.za"""

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Visualise Option Prices and Greeks", size=(300, 500))
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyEvent)

        self.fileReader = csvReader.Reader()
        self.viewLegend = False
        self.viewGrid = True
        self.viewFill = False
        self.showDifference = False
        self.current_view = 0

        # initialise data arrays
        self.option_price = []
        self.time_span = []
        self.delta = []
        self.gamma = []
        self.vega = []
        self.theta = []
        self.rho = []
        
        # initialise bump values
        self.stock_bump = 0
        self.time_bump = 0
        self.rate_bump = 0
        self.volitile_bump = 0
        
        # build interface
        self.Build_Menus()
        self.Build_Panel()
        self.statusbar = self.CreateStatusBar()
        self.Plot_Data()
        self.SetSize(size=(830, 480))

    # on span-selection of graph TODO still
    def onselect(self, xmin, xmax):
        # initialise data sets
        t = numpy.arange(0, 31, 1)
        option_price = []
        delta = []
        gamma = []
        theta = []
        rho = []
        vega = []
        
        # identify the indices of new data set based on selection
        indmin = int(xmin)
        indmax = numpy.searchsorted(t, (xmin, xmax))
        indmax = min(len(t)-1, int(xmax)+1)
        
        thisx = t[indmin:indmax]
        if len(self.option_price) > 0:
            option_price = numpy.array(map(float, self.option_price[self.stock_bump]))
            thisy = option_price[indmin:indmax]
            self.line1.set_data(thisx, thisy)
        if len(self.delta) > 0:
            delta = numpy.array(map(float, self.delta[self.stock_bump]))
            thisy = delta[indmin:indmax]
            self.line2.set_data(thisx, thisy)
        if len(self.gamma) > 0:
            gamma = numpy.array(map(float, self.gamma[self.stock_bump]))
            thisy = gamma[indmin:indmax]
            self.line3.set_data(thisx, thisy)
        if len(self.theta) > 0:
            theta = numpy.array(map(float, self.theta[self.time_bump]))
            thisy = theta[indmin:indmax]
            self.line4.set_data(thisx, thisy)
        if len(self.rho) > 0:
            rho = numpy.array(map(float, self.rho[self.rate_bump]))
            thisy = rho[indmin:indmax]
            self.line5.set_data(thisx, thisy)
        if len(self.vega) > 0:
            vega = numpy.array(map(float, self.vega[self.volitile_bump]))
            thisy = vega[indmin:indmax]
            self.line6.set_data(thisx, thisy)

        self.axes2.set_xlim(thisx[0]-1, thisx[-1]+1)
        # self.axes2.set_ylim(thisy[0]-300, thisy[-1]+300)
        self.canvas.draw()

    def Build_Panel(self):
        self.panel = wx.Panel(self)

        # Create Figure and canvas objects
        self.fig = Figure((6.0, 4.0), 100)
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        self.axes = self.fig.add_subplot(111)

        # setup slider-widgets for controlling GUI
        self.stockSlider_label = wx.StaticText(self.panel, -1, "Stock Price: ")
        self.stockSlider = wx.Slider(self.panel, value=5, minValue=1, maxValue=9, 
            pos=(20, 20), size=(100,-1), style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS)
        self.stockSlider.SetTickFreq(9, 1)
        self.rateSlider_label = wx.StaticText(self.panel, -1, "Interest Rate: ")
        self.rateSlider = wx.Slider(self.panel, value=5, minValue=1, maxValue=9, 
            pos=(20, 20), size=(100,-1), style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS)
        self.rateSlider.SetTickFreq(9, 1)
        self.volatilSlider_label = wx.StaticText(self.panel, -1, "Volatility: ")
        self.volatilSlider = wx.Slider(self.panel, value=5, minValue=1, maxValue=9, 
            pos=(20, 20), size=(100,-1), style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS)
        self.volatilSlider.SetTickFreq(9, 1)
        self.timeStepSlider_label = wx.StaticText(self.panel, -1, "Time Step: ")
        self.timeStepSlider = wx.Slider(self.panel, value=5, minValue=1, maxValue=9, 
            pos=(20, 20), size=(100,-1), style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS)
        self.timeStepSlider.SetTickFreq(9, 1)

        self.Bind(wx.EVT_SLIDER, self.onStockSlider, self.stockSlider)
        self.Bind(wx.EVT_SLIDER, self.onRateSlider, self.rateSlider)
        self.Bind(wx.EVT_SLIDER, self.onVolatilSlider, self.volatilSlider)
        self.Bind(wx.EVT_SLIDER, self.ontimeStepSlider, self.timeStepSlider)        

        # setup options-widgets for controlling graphs
        self.callRadio = wx.RadioButton(self.panel, label="Call options", pos=(10, 10))
        self.putRadio = wx.RadioButton(self.panel, label="Put options", pos=(10, 30))
        self.spaceKeeper = wx.StaticText(self.panel, -1, '')
        self.optionPriceCheck = wx.CheckBox(self.panel, label="Option Price", pos=(20, 20))
        self.deltaCheck = wx.CheckBox(self.panel, label="Delta", pos=(20, 20))
        self.gammaCheck = wx.CheckBox(self.panel, label="Gamma", pos=(20, 20))
        self.rhoCheck = wx.CheckBox(self.panel, label="Rho", pos=(20, 20))
        self.thetaCheck = wx.CheckBox(self.panel, label="Theta", pos=(20, 20))
        self.vegaCheck = wx.CheckBox(self.panel, label="Vega", pos=(20, 20))
        self.differenceCheck = wx.CheckBox(self.panel, label="Show Difference", pos=(20, 20))

        self.Bind(wx.EVT_RADIOBUTTON, self.onCallRadio, self.callRadio)
        self.Bind(wx.EVT_RADIOBUTTON, self.onPutRadio, self.putRadio)
        self.Bind(wx.EVT_CHECKBOX, self.onOptionPrice, self.optionPriceCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onDelta, self.deltaCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onGamma, self.gammaCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onRho, self.rhoCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onTheta, self.thetaCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onVega, self.vegaCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onDifferenceCheck, self.differenceCheck)

        # Create the navigation toolbar, tied to the canvas
        self.toolbar = NavigationToolbar(self.canvas)

        ####################
        # Layout with sizers
        ####################
        flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.hboxMainBlock = wx.BoxSizer(wx.HORIZONTAL)
        self.vboxOptions = wx.BoxSizer(wx.VERTICAL)
        self.hboxSliders = wx.BoxSizer(wx.HORIZONTAL)
        self.flexiGridSizer = wx.FlexGridSizer(4, 2, 3, 10)

        # adds border around sliders to group related widgets
        self.vboxOptions.AddSpacer(10)
        self.sliderBorder = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, 'Sliders'), orient=wx.VERTICAL)
        self.flexiGridSizer.AddMany([(self.stockSlider_label), (self.stockSlider, 1, wx.ALL), 
            (self.rateSlider_label), (self.rateSlider, 1, wx.EXPAND),
            (self.volatilSlider_label), (self.volatilSlider, 1, wx.EXPAND),
            (self.timeStepSlider_label), (self.timeStepSlider, 1, wx.EXPAND)])
        self.sliderBorder.Add(self.flexiGridSizer, 1, wx.ALL, 5)
        self.vboxOptions.Add(self.sliderBorder, 0, flag=wx.ALIGN_LEFT|wx.ALL)
        

        # add border for type of option price
        self.optionsBorder = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, 'Option Price'), orient=wx.VERTICAL)
        self.flexiOptions = wx.FlexGridSizer(2, 1, 3, 10)
        self.flexiOptions.AddMany([(self.callRadio, 1, wx.EXPAND), 
            (self.putRadio, 1, wx.EXPAND)])            
        self.optionsBorder.Add(self.flexiOptions, 1, wx.ALL, 5)
        self.vboxOptions.Add(self.optionsBorder, 1, flag=wx.ALIGN_LEFT|wx.ALL|wx.GROW)
        
        # add border for greeks
        self.greekOptionsBorder = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, 'Options'), orient=wx.VERTICAL)
        self.flexiOptions2 = wx.FlexGridSizer(7, 1, 3, 10)
        self.flexiOptions2.AddMany([(self.optionPriceCheck, 1, wx.EXPAND), (self.deltaCheck, 1, wx.EXPAND), (self.gammaCheck, 1, wx.EXPAND), 
            (self.rhoCheck, 1, wx.EXPAND), (self.thetaCheck, 1, wx.EXPAND), (self.vegaCheck, 1, wx.EXPAND)])
        self.greekOptionsBorder.Add(self.flexiOptions2, 1, wx.ALL, 5)
        self.vboxOptions.Add(self.greekOptionsBorder, 2, flag=wx.ALIGN_LEFT|wx.ALL|wx.GROW)
        #self.vboxOptions.AddSpacer(5)
        
        # add border for other checkable options
        self.otherOptionsBorder = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, 'Options'), orient=wx.VERTICAL)
        self.flexiOptions3 = wx.FlexGridSizer(1, 1, 3, 10)
        self.flexiOptions3.AddMany([(self.differenceCheck, 1, wx.EXPAND)])
        self.otherOptionsBorder.Add(self.flexiOptions3, 1, wx.ALL, 5)
        self.vboxOptions.Add(self.otherOptionsBorder, 0, flag=wx.ALIGN_LEFT|wx.ALL|wx.GROW)
        self.vboxOptions.AddSpacer(5)

        self.hboxMainBlock.Add(self.vboxOptions, 0, flag=flags)
        self.hboxMainBlock.Add(self.canvas, 1, flag=wx.ALIGN_RIGHT|wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        self.sizer.Add(self.hboxMainBlock, 1, wx.ALL|wx.EXPAND)

        self.sizer.Add(self.toolbar, 0, wx.ALL|wx.ALIGN_RIGHT)
        self.sizer.AddSpacer(1)

        self.canvas.Bind(wx.EVT_KEY_DOWN, self.onKeyEvent)
        self.Bind(wx.EVT_CLOSE, self.onExit)

        self.panel.SetSizer(self.sizer)
        self.sizer.Fit(self)
        self.Center()

    def Build_Menus(self):
        """ build menus """
        MENU_EXIT = wx.NewId()
        MENU_OPEN = wx.NewId()
        MENU_SAVE = wx.NewId()
        MENU_PRINT = wx.NewId()
        MENU_PSETUP = wx.NewId()
        MENU_PREVIEW =wx.NewId()
        MENU_CLIPB =wx.NewId()
        MENU_VIEW_GRID = wx.NewId()
        MENU_HELP =wx.NewId()
        MENU_BASIC = wx.NewId()
        MENU_ADVANCE = wx.NewId()
        MENU_LEGEND = wx.NewId()
        MENU_3D = wx.NewId()
        MENU_FILL = wx.NewId()

        menuBar = wx.MenuBar()

        f0 = wx.Menu()
        importItem = wx.MenuItem(f0, MENU_OPEN, "&Import\tCtrl+I")
        f0.AppendItem(importItem)  
        f0.Append(MENU_SAVE,   "&Export",   "Save Image of Plot")
        f0.AppendSeparator()
        printMenu = wx.Menu()
        printMenu.Append(MENU_PSETUP, "Page Setup...",    "Printer Setup")
        printMenu.Append(MENU_PREVIEW,"Print Preview...", "Print Preview")
        printItem = wx.MenuItem(printMenu, MENU_PRINT,  "Print\tCtrl+P")
        printMenu.AppendItem(printItem)
        f0.AppendMenu(-1, '&Print', printMenu)
        f0.AppendSeparator()
        exitItem = wx.MenuItem(f0, MENU_EXIT, 'E&xit\tCtrl+Q')
        f0.AppendItem(exitItem)
        menuBar.Append(f0,     "&File")

        f1 = wx.Menu()
        f1.Append(MENU_BASIC, '&Basic', "Basic View(2D)")
        f1.Append(MENU_ADVANCE, '&Advanced-2D', "Advanced View(2D)")
        f1.Append(MENU_3D, 'A&dvanced-3D', "Advanced View(3D)")
        menuBar.Append(f1, "&View")

        f2 = wx.Menu()
        viewGridItem = wx.MenuItem(f2, MENU_VIEW_GRID, 'View &Grid\tCtrl+G')
        f2.AppendItem(viewGridItem)
        viewLegendItem = wx.MenuItem(f2, MENU_LEGEND, 'View &Legend\tCtrl+L')
        f2.AppendItem(viewLegendItem)
        viewFillItem = wx.MenuItem(f2, MENU_FILL, 'View &Fill\tCtrl+F')
        f2.AppendItem(viewFillItem)
        menuBar.Append(f2, "&Tools")

        f3 = wx.Menu()
        f3.Append(MENU_HELP, "Quick Reference",  "Quick Reference")
        menuBar.Append(f3, "&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.onImport,       id=MENU_OPEN)
        self.Bind(wx.EVT_MENU, self.onPrint,        id=MENU_PRINT)
        self.Bind(wx.EVT_MENU, self.onPrinterSetup, id=MENU_PSETUP)
        self.Bind(wx.EVT_MENU, self.onPrinterPreview, id=MENU_PREVIEW)
        self.Bind(wx.EVT_MENU, self.onClipboard,    id=MENU_CLIPB)
        self.Bind(wx.EVT_MENU, self.onExport,       id=MENU_SAVE)
        self.Bind(wx.EVT_MENU, self.onExit ,        id=MENU_EXIT)
        self.Bind(wx.EVT_MENU, self.onViewGrid,     id=MENU_VIEW_GRID)
        self.Bind(wx.EVT_MENU, self.onViewLegend,     id=MENU_LEGEND)
        self.Bind(wx.EVT_MENU, self.onHelp,         id=MENU_HELP)
        self.Bind(wx.EVT_MENU, self.onBasicView,    id=MENU_BASIC)
        self.Bind(wx.EVT_MENU, self.onAdvancedView, id=MENU_ADVANCE)
        self.Bind(wx.EVT_MENU, self.onAdvanced3DView, id=MENU_3D)
        self.Bind(wx.EVT_MENU, self.onViewFill, id=MENU_FILL)

    """ Menu event methods """
    def onViewFill(self, event=None):
        if self.viewFill:
            self.viewFill = False
        else:
            self.viewFill = True
        self.Plot_Data()

    def onViewLegend(self, event=None):
        if self.viewLegend:
            self.viewLegend = False
        else:
            self.viewLegend = True
        self.Plot_Data()

    def onBasicView(self, event=None):
        self.current_view = 0
        self.Plot_Data()

    def onAdvancedView(self, event=None):
        self.current_view = 1
        self.Plot_Data()

    def onAdvanced3DView(self, event=None):
        self.current_view = 2
        self.Plot_Data()

    def onPrinterSetup(self,event=None):
        self.canvas.Printer_Setup(event=event)

    def onPrinterPreview(self,event=None):
        self.canvas.Printer_Preview(event=event)

    def onPrint(self,event=None):
        self.canvas.Printer_Print(event=event)

    def onClipboard(self,event=None):
        self.canvas.Copy_to_Clipboard(event=event)

    def onKeyEvent(self,event=None):
        """ capture and act upon keystroke events """
        if event == None: return
        key = event.GetKeyCode()
        if (key < wx.WXK_SPACE or  key > 255):  return

        if (event.ControlDown() and chr(key)=='C'): # Ctrl-C
            self.onClipboard(event=event)

    def onHelp(self, event=None):
        dlg = wx.MessageDialog(self, self.help_msg, "Quick Reference", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def onViewGrid(self, event=None):
        if self.viewGrid:
            self.viewGrid = False
        else:
            self.viewGrid = True
        self.Plot_Data()

    def onExport(self,event=None):
        """ save figure image to file"""
        file_choices = "PNG (*.png)|*.png|" \
                       "JPEG (*.jpg)|*.jpg|" \
                       "BMP (*.bmp)|*.bmp"

        thisdir  = os.getcwd()

        dlg = wx.FileDialog(self, message='Save Plot Figure as...',
                            defaultDir = thisdir, defaultFile='plot.png',
                            wildcard=file_choices, style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path,dpi=300)
            if (path.find(thisdir) ==  0):
                path = path[len(thisdir)+1:]
            print('Saved plot to %s' % path)

    def onImport(self, event=None):
        """ Import csv file of option prices and greeks """
        file_choices = "SETTINGS (*.settings)|*.settings"
        thisdir  = ''.join(os.getcwd()+'/data')

        # import output file
        dlg = wx.FileDialog(self, message='Import option prices and greeks (Outputs)',
                            defaultDir = thisdir, defaultFile='data.settings',
                            wildcard=file_choices, style=wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            # this also involves reading in all the data
            self.time_span = self.fileReader.loadSettingsFile(path, thisdir, self.statusbar)
            print('Opened settings file at %s' % path)
        else:
            dlg = wx.MessageDialog(self, "Failed to import the correct settings file.", "Complication", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        # populate data
        self.option_price = self.fileReader.getOptionPrice(self.callRadio.GetValue(), self.optionPriceCheck.IsChecked())
        self.delta = self.fileReader.getDeltaValues(self.callRadio.GetValue(), self.deltaCheck.IsChecked())
        self.gamma = self.fileReader.getGammaValues(self.callRadio.GetValue(), self.gammaCheck.IsChecked())
        self.vega = self.fileReader.getVegaValues(self.callRadio.GetValue(), self.vegaCheck.IsChecked())
        self.theta = self.fileReader.getThetaValues(self.callRadio.GetValue(), self.thetaCheck.IsChecked())
        self.rho = self.fileReader.getRhoValues(self.callRadio.GetValue(), self.rhoCheck.IsChecked())

        self.Plot_Data()

    def onExit(self,event=None):
        dlg = wx.MessageDialog(None, 'Are you sure to exit?', 'Confirm', wx.YES_NO|wx.NO_DEFAULT|wx.ICON_QUESTION)
        ret = dlg.ShowModal()
        if ret == wx.ID_YES:
            self.Destroy()

    """ GUI event methods """
    def onCallRadio(self, event=None):
        self.option_price = self.fileReader.getOptionPrice(self.callRadio.GetValue(), 
            self.optionPriceCheck.IsChecked())
        self.delta = self.fileReader.getDeltaValues(self.callRadio.GetValue(), 
            self.deltaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.gamma = self.fileReader.getGammaValues(self.callRadio.GetValue(), 
            self.gammaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.vega = self.fileReader.getVegaValues(self.callRadio.GetValue(), 
            self.vegaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.theta = self.fileReader.getThetaValues(self.callRadio.GetValue(), 
            self.thetaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.rho = self.fileReader.getRhoValues(self.callRadio.GetValue(), 
            self.rhoCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.Plot_Data()

    def onPutRadio(self, event=None):
        self.option_price = self.fileReader.getOptionPrice(self.callRadio.GetValue(), 
            self.optionPriceCheck.IsChecked())
        self.delta = self.fileReader.getDeltaValues(self.callRadio.GetValue(), 
            self.deltaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.gamma = self.fileReader.getGammaValues(self.callRadio.GetValue(), 
            self.gammaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.vega = self.fileReader.getVegaValues(self.callRadio.GetValue(), 
            self.vegaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.theta = self.fileReader.getThetaValues(self.callRadio.GetValue(), 
            self.thetaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.rho = self.fileReader.getRhoValues(self.callRadio.GetValue(), 
            self.rhoCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.Plot_Data() 

    def onOptionPrice(self, event=None):
        self.option_price = self.fileReader.getOptionPrice(self.callRadio.GetValue(), 
            self.optionPriceCheck.IsChecked())
        self.Plot_Data()

    def onDelta(self, event=None):
        self.delta = self.fileReader.getDeltaValues(self.callRadio.GetValue(), 
            self.deltaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.Plot_Data()

    def onGamma(self, event=None):
        self.gamma = self.fileReader.getGammaValues(self.callRadio.GetValue(), 
            self.gammaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.Plot_Data()

    def onRho(self, event=None):
        self.rho = self.fileReader.getRhoValues(self.callRadio.GetValue(), 
            self.rhoCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.Plot_Data()

    def onTheta(self, event=None):
        self.theta = self.fileReader.getThetaValues(self.callRadio.GetValue(), 
            self.thetaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.Plot_Data()

    def onVega(self, event=None):
        self.vega = self.fileReader.getVegaValues(self.callRadio.GetValue(), 
            self.vegaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.Plot_Data()

    def onDifferenceCheck(self, event=None):
        if self.showDifference:
            self.showDifference = False
        else:
            self.showDifference = True
            
        # reload and replot data
        self.delta = self.fileReader.getDeltaValues(self.callRadio.GetValue(), 
            self.deltaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.gamma = self.fileReader.getGammaValues(self.callRadio.GetValue(), 
            self.gammaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.vega = self.fileReader.getVegaValues(self.callRadio.GetValue(), 
            self.vegaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.theta = self.fileReader.getThetaValues(self.callRadio.GetValue(), 
            self.thetaCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.rho = self.fileReader.getRhoValues(self.callRadio.GetValue(), 
            self.rhoCheck.IsChecked(), self.differenceCheck.IsChecked())
        self.Plot_Data()

    def onStockSlider(self, event=None):
        temp = 0
        if self.stockSlider.GetValue() == 1:
            temp = 7
        elif self.stockSlider.GetValue() == 2:
            temp = 14
        elif self.stockSlider.GetValue() == 3:
            temp = 21
        elif self.stockSlider.GetValue() == 4:
            temp = 28
        elif self.stockSlider.GetValue() == 5:
            temp = 35
        elif self.stockSlider.GetValue() == 6:
            temp = 42
        elif self.stockSlider.GetValue() == 7:
            temp = 49
        elif self.stockSlider.GetValue() == 8:
            temp = 56
        elif self.stockSlider.GetValue() == 9:
            temp = 63

        self.statusbar.SetStatusText("Stock price bump: "+str(temp))
        # print(self.stockSlider.GetValue()-1)
        self.stock_bump = self.stockSlider.GetValue()-1
        self.Plot_Data()

    def onRateSlider(self, event=None):
        temp = 0
        if self.rateSlider.GetValue() == 1:
            temp = 0.001
        elif self.rateSlider.GetValue() == 2:
            temp = 0.002
        elif self.rateSlider.GetValue() == 3:
            temp = 0.003
        elif self.rateSlider.GetValue() == 4:
            temp = 0.004
        elif self.rateSlider.GetValue() == 5:
            temp = 0.005
        elif self.rateSlider.GetValue() == 6:
            temp = 0.006
        elif self.rateSlider.GetValue() == 7:
            temp = 0.007
        elif self.rateSlider.GetValue() == 8:
            temp = 0.008
        elif self.rateSlider.GetValue() == 9:
            temp = 0.009

        self.statusbar.SetStatusText("Interest Rate bump: "+str(temp))
        # print(self.stockSlider.GetValue()-1)
        self.rate_bump = self.rateSlider.GetValue()-1
        self.Plot_Data()

    def onVolatilSlider(self, event=None):
        temp = 0
        if self.volatilSlider.GetValue() == 1:
            temp = 0.004
        elif self.volatilSlider.GetValue() == 2:
            temp = 0.008
        elif self.volatilSlider.GetValue() == 3:
            temp = 0.012
        elif self.volatilSlider.GetValue() == 4:
            temp = 0.016
        elif self.volatilSlider.GetValue() == 5:
            temp = 0.02
        elif self.volatilSlider.GetValue() == 6:
            temp = 0.024
        elif self.volatilSlider.GetValue() == 7:
            temp = 0.028
        elif self.volatilSlider.GetValue() == 8:
            temp = 0.032
        elif self.volatilSlider.GetValue() == 9:
            temp = 0.036

        self.statusbar.SetStatusText("Volatility bump: "+str(temp))
        # print(self.stockSlider.GetValue()-1)
        self.volitile_bump = self.volatilSlider.GetValue()-1
        self.Plot_Data()

    def ontimeStepSlider(self, event=None):
        temp = 0
        if self.timeStepSlider.GetValue() == 1:
            temp = 0.002
        elif self.timeStepSlider.GetValue() == 2:
            temp = 0.004
        elif self.timeStepSlider.GetValue() == 3:
            temp = 0.006
        elif self.timeStepSlider.GetValue() == 4:
            temp = 0.08
        elif self.timeStepSlider.GetValue() == 5:
            temp = 0.01
        elif self.timeStepSlider.GetValue() == 6:
            temp = 0.012
        elif self.timeStepSlider.GetValue() == 7:
            temp = 0.014
        elif self.timeStepSlider.GetValue() == 8:
            temp = 0.016
        elif self.timeStepSlider.GetValue() == 9:
            temp = 0.018

        self.statusbar.SetStatusText("Time step bump: "+str(temp))
        # print(self.stockSlider.GetValue()-1)
        self.time_bump = self.timeStepSlider.GetValue()-1
        self.Plot_Data()
        self.Plot_Data()

    """ Graph plotting methods """
    def Plot_Data(self):
        if self.current_view == 1:
            self.Plot_Data_advanced()
        elif self.current_view == 2:
            self.Plot_Data_3D()
        elif self.current_view == 0:
            """ Basic 2D graph plotter """
            self.fig.delaxes(self.axes)
            self.axes.clear()
            self.axes = self.fig.add_subplot(111) # can use add_axes, but then nav-toolbar would not work
            self.axes.grid(self.viewGrid)

            # plot graphs here
            t = numpy.arange(0, 31, 1)
            p = []
            if self.viewFill:
                p = numpy.array(map(float, self.option_price[self.stock_bump]))
            if len(self.option_price) > 0:
                self.axes.plot(t, self.option_price[self.stock_bump], label="Option Price")
            if len(self.delta) > 0:
                if self.viewFill:
                    s = numpy.array(self.delta[self.stock_bump])
                    self.axes.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.axes.fill_between(t, p, s, where=s<=p, facecolor='green', interpolate=True)
                else:
                    self.axes.plot(self.delta[self.stock_bump], label="Delta")
            if len(self.gamma) > 0:
                if self.viewFill:
                    s = numpy.array(self.gamma[self.stock_bump])
                    self.axes.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.axes.fill_between(t, p, s, where=s<=p, facecolor='cyan', interpolate=True)
                else:
                    self.axes.plot(self.gamma[self.stock_bump], label="Gamma")
            if len(self.vega) > 0:
                if self.viewFill:
                    s = numpy.array(self.vega[self.volitile_bump])
                    self.axes.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.axes.fill_between(t, p, s, where=s<=p, facecolor='yellow', interpolate=True)
                else:
                    self.axes.plot(self.vega[self.volitile_bump], label="Vega")
            if len(self.theta) > 0:
                if self.viewFill:
                    s = numpy.array(self.theta[self.time_bump])
                    self.axes.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.axes.fill_between(t, p, s, where=s<=p, facecolor='blue', interpolate=True)
                else:
                    self.axes.plot(t, self.theta[self.time_bump], label="Theta")
            if len(self.rho) > 0:
                if self.viewFill:
                    s = numpy.array(self.rho[self.rate_bump])
                    self.axes.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.axes.fill_between(t, p, s, where=s<=p, facecolor='white', interpolate=True)
                else:
                    self.axes.plot(t, self.rho[self.rate_bump], label="Rho")

            if self.viewLegend:
                # Shink current axis by 15%
                box = self.axes.get_position()
                self.axes.set_position([box.x0, box.y0, box.width * 0.88, box.height])

                # Put a legend to the right of the current axis
                self.axes.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':8})

            self.canvas.draw()

    def Plot_Data_advanced(self):
        """ Advanced 2D plotter """
        self.fig.delaxes(self.axes)
        self.axes.clear()
        self.axes = self.fig.add_subplot(211)
        self.axes.grid(self.viewGrid)

        t = numpy.arange(0, 31, 1)
        p = []
        if self.viewFill and len(self.option_price) > 0:
            p = numpy.array(map(float, self.option_price[self.stock_bump]))
        if True:
            if len(self.option_price) > 0:
                self.axes.plot(t, self.option_price[self.stock_bump], label="Option Price")
            if len(self.delta) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.delta[self.stock_bump])
                    self.axes.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.axes.fill_between(t, p, s, where=s<=p, facecolor='green', interpolate=True)
                else:
                    self.axes.plot(self.delta[self.stock_bump], label="Delta")
            if len(self.gamma) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.gamma[self.stock_bump])
                    self.axes.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.axes.fill_between(t, p, s, where=s<=p, facecolor='cyan', interpolate=True)
                else:
                    self.axes.plot(self.gamma[self.stock_bump], label="Gamma")
            if len(self.vega) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.vega[self.volitile_bump])
                    self.axes.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.axes.fill_between(t, p, s, where=s<=p, facecolor='yellow', interpolate=True)
                else:
                    self.axes.plot(self.vega[self.volitile_bump], label="Vega")
            if len(self.theta) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.theta[self.time_bump])
                    self.axes.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.axes.fill_between(t, p, s, where=s<=p, facecolor='blue', interpolate=True)
                else:
                    self.axes.plot(t, self.theta[self.time_bump], label="Theta")
            if len(self.rho) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.rho[self.rate_bump])
                    self.axes.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.axes.fill_between(t, p, s, where=s<=p, facecolor='white', interpolate=True)
                else:
                    self.axes.plot(t, self.rho[self.rate_bump], label="Rho")

        self.axes2 = self.fig.add_subplot(212)
        self.axes2.clear()
        self.axes2.grid(self.viewGrid)
        if True:
            if len(self.option_price) > 0:
                self.line1, = self.axes2.plot(t, self.option_price[self.stock_bump], label="Option Price")
            if len(self.delta) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.delta[self.stock_bump])
                    self.line2, = self.axes2.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.line2, = self.axes2.fill_between(t, p, s, where=s<=p, facecolor='green', interpolate=True)
                else:
                    self.line2, = self.axes2.plot(self.delta[self.stock_bump], label="Delta")
            if len(self.gamma) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.gamma[self.stock_bump])
                    self.line3, = self.axes2.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.line3, = self.axes2.fill_between(t, p, s, where=s<=p, facecolor='cyan', interpolate=True)
                else:
                    self.line3, = self.axes2.plot(self.gamma[self.stock_bump], label="Gamma")
            if len(self.vega) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.vega[self.volitile_bump])
                    self.line4, = self.axes2.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.line4, = self.axes2.fill_between(t, p, s, where=s<=p, facecolor='yellow', interpolate=True)
                else:
                    self.line4, = self.axes2.plot(self.vega[self.volitile_bump], label="Vega")
            if len(self.theta) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.theta[self.time_bump])
                    self.line5, = self.axes2.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.line5, = self.axes2.fill_between(t, p, s, where=s<=p, facecolor='blue', interpolate=True)
                else:
                    self.line5, = self.axes2.plot(t, self.theta[self.time_bump], label="Theta")
            if len(self.rho) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.rho[self.rate_bump])
                    self.line6, = self.axes2.fill_between(t, p, s, where=s>=p, facecolor='red', interpolate=True)
                    self.line6, = self.axes2.fill_between(t, p, s, where=s<=p, facecolor='white', interpolate=True)
                else:
                    self.line6, = self.axes2.plot(t, self.rho[self.rate_bump], label="Rho")

        if self.viewLegend:
            # Shink current axis by 15%
            box = self.axes.get_position()
            self.axes.set_position([box.x0, box.y0, box.width * 0.85, box.height])
            # Put a legend to the right of the current axis
            self.axes.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':8})

        # set useblit True on gtkagg for enhanced performance
        self.span = SpanSelector(self.axes, self.onselect, 'horizontal', useblit=True, rectprops=dict(alpha=0.5, facecolor='red'))

        self.canvas.draw()

    def Plot_Data_3D(self):
        """ Advanced 3D plotter """
        # plot graphs
        self.fig.delaxes(self.axes)
        self.axes.clear()
        self.axes = self.fig.add_subplot(111, projection='3d') # can use add_axes, but then nav-toolbar would not work
        self.axes.grid(self.viewGrid)

        t = numpy.arange(0, 31, 1)
        b = numpy.arange(0, 9, 1)
        # p = map(float, self.option_price)
        p = [[float(string) for string in inner] for inner in self.option_price]
        Z2D, Y2D = numpy.meshgrid(b, t)
        # Z2D = numpy.reshape(t,(len(X2D[:,0]),len(X2D[0,:])))
        X2D = p

        self.axes.plot_surface(X2D, Y2D, Z2D) #, cmap=cm.coolwarm, rstride=1, cstride=1, linewidth=0, antialiased=False)
        print(X2D, Y2D, Z2D)
        cset = self.axes.contour(X2D, Y2D, Z2D, zdir='z', offset=-100, cmap=cm.coolwarm)
        # cset = self.axes.contour(X2D, Y2D, Z2D, zdir='x', offset=-40, cmap=cm.coolwarm)
        # cset = self.axes.contour(X2D, Y2D, Z2D, zdir='y', offset=40, cmap=cm.coolwarm)
            
        # ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
        # self.axes.plot(delta, label="Delta")
        # print(self.option_price)
        # self.axes.plot(self.gamma, label="Gamma")
        # self.axes.plot(self.vega, label="Vega")
        # self.axes.plot(self.theta, label="Theta")
        # self.axes.plot(self.rho, label="Rho")
        # X, Y, Z = axes3d.get_test_data(0.05)
        # self.axes.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
        # cset = self.axes.contour(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
        # cset = self.axes.contour(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
        # cset = self.axes.contour(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)

        self.axes.set_xlabel('X')
        # self.axes.set_xlim(-40, 40)
        self.axes.set_ylabel('Y')
        # self.axes.set_ylim(-40, 40)
        self.axes.set_zlabel('Z')
        # self.axes.set_zlim(-100, 100)

        if self.viewLegend:
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            # self.axes.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=1)
        self.canvas.draw()
