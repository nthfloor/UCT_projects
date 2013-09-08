"""
    Main file for FinGPU visualisation interface
    Includes GUI and plotting code

    by Nathan Floor, flrnat001
    flrnat001@cs.uct.ac.za
"""

from __future__ import division, print_function

import wx
import os
# import numpy
import matplotlib
import csvReader

matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas, NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure


class PlotFrame(wx.Frame):
    global fileReader
    global viewGrid
    global viewLegend

    fileReader = csvReader.Reader()
    viewGrid = True
    viewLegend = True

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
        wx.Frame.__init__(self, None, -1, "Visualise Option Prices and Greeks", size=(250, 200))
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyEvent)
        
        self.Build_Menus()
        self.Build_Panel()
        self.Plot_Data()

    def Build_Panel(self):
        self.panel = wx.Panel(self)

        # Create Figure and canvas objects
        self.fig = Figure((5.0, 4.0), 100)
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        # can use add_axes, but then nav-toolbar would not work
        self.axes = self.fig.add_subplot(111)

        # setup slider-widgets for controlling GUI
        self.stockSlider_label = wx.StaticText(self.panel, -1, "Stock Price: ")
        self.stockSlider = wx.Slider(self.panel, value=0, minValue=-5, maxValue=5, 
            pos=(20, 20), size=(100,-1), style=wx.SL_HORIZONTAL)
        self.rateSlider_label = wx.StaticText(self.panel, -1, "Interest Rate: ")
        self.rateSlider = wx.Slider(self.panel, value=0, minValue=-5, maxValue=5, 
            pos=(20, 20), size=(100,-1), style=wx.SL_HORIZONTAL)
        self.volatilSlider_label = wx.StaticText(self.panel, -1, "Volatility: ")
        self.volatilSlider = wx.Slider(self.panel, value=0, minValue=-5, maxValue=5, 
            pos=(20, 20), size=(100,-1), style=wx.SL_HORIZONTAL)
        self.timeStepSlider_label = wx.StaticText(self.panel, -1, "Time Step: ")
        self.timeStepSlider = wx.Slider(self.panel, value=0, minValue=-5, maxValue=5, 
            pos=(20, 20), size=(100,-1), style=wx.SL_HORIZONTAL)

        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.onStockSlider, self.stockSlider)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.onRateSlider, self.rateSlider)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.onVolatilSlider, self.volatilSlider)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.ontimeStepSlider, self.timeStepSlider)        

        # setup options-widgets for controlling graphs
        self.callRadio = wx.RadioButton(self.panel, label="Call options", pos=(10, 10))
        self.putRadio = wx.RadioButton(self.panel, label="Put options", pos=(10, 30))
        self.spaceKeeper = wx.StaticText(self.panel, -1, '')
        self.deltaCheck = wx.CheckBox(self.panel, label="Delta", pos=(20, 20))
        self.gammaCheck = wx.CheckBox(self.panel, label="Gamma", pos=(20, 20))
        self.rhoCheck = wx.CheckBox(self.panel, label="Rho", pos=(20, 20))
        self.thetaCheck = wx.CheckBox(self.panel, label="Theta", pos=(20, 20))
        self.epsilonCheck = wx.CheckBox(self.panel, label="Epsilon", pos=(20, 20))

        self.Bind(wx.EVT_RADIOBUTTON, self.onCallRadio, self.callRadio)
        self.Bind(wx.EVT_RADIOBUTTON, self.onPutRadio, self.putRadio)
        self.Bind(wx.EVT_CHECKBOX, self.onDelta, self.deltaCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onGamma, self.gammaCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onRho, self.rhoCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onTheta, self.thetaCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onEpsilon, self.epsilonCheck)

        # Create the navigation toolbar, tied to the canvas
        self.toolbar = NavigationToolbar(self.canvas)

        #
        # Layout with sizers
        #
        flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.hboxMainBlock = wx.BoxSizer(wx.HORIZONTAL)
        self.vboxOptions = wx.BoxSizer(wx.VERTICAL)
        self.hboxSliders = wx.BoxSizer(wx.HORIZONTAL)
        self.flexiGridSizer = wx.FlexGridSizer(4, 2, 3, 10)

        # adds border around sliders to group related widgets
        self.sliderBorder = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, 'Sliders'), orient=wx.VERTICAL)
        self.flexiGridSizer.AddMany([(self.stockSlider_label), (self.stockSlider, 1, wx.ALL), 
            (self.rateSlider_label), (self.rateSlider, 1, wx.EXPAND),
            (self.volatilSlider_label), (self.volatilSlider, 1, wx.EXPAND),
            (self.timeStepSlider_label), (self.timeStepSlider, 1, wx.EXPAND)])
        self.sliderBorder.Add(self.flexiGridSizer, 1, wx.ALL, 5)
        self.vboxOptions.Add(self.sliderBorder, 1, flag=wx.ALIGN_LEFT|wx.ALL)
        self.vboxOptions.AddSpacer(10)

        self.optionsBorder = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, 'Options'), orient=wx.VERTICAL)
        self.flexiOptions = wx.FlexGridSizer(8, 1, 3, 10)
        self.flexiOptions.AddMany([(self.callRadio, 1, wx.EXPAND), (self.putRadio, 1, wx.EXPAND), (self.spaceKeeper), 
            (self.deltaCheck, 1, wx.EXPAND), (self.gammaCheck, 1, wx.EXPAND), (self.rhoCheck, 1, wx.EXPAND), 
            (self.thetaCheck, 1, wx.EXPAND), (self.epsilonCheck, 1, wx.EXPAND)])
        self.optionsBorder.Add(self.flexiOptions, 1, wx.ALL, 5)
        self.vboxOptions.Add(self.optionsBorder, 1, flag=wx.ALIGN_LEFT|wx.ALL)               

        self.hboxMainBlock.Add(self.vboxOptions, 0, flag=flags)
        self.hboxMainBlock.Add(self.canvas, 1, flag=wx.ALIGN_RIGHT|wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add(self.hboxMainBlock, 0, wx.ALL)

        self.sizer.Add(self.toolbar, 0, wx.ALIGN_RIGHT)

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
        f1.Append(MENU_ADVANCE, '&Advanced', "Advanced View(3D)")
        menuBar.Append(f1, "&View")

        f2 = wx.Menu()
        viewGridItem = wx.MenuItem(f2, MENU_VIEW_GRID, 'View &Grid\tCtrl+G')
        f2.AppendItem(viewGridItem)
        viewLegendItem = wx.MenuItem(f2, MENU_LEGEND, 'View &Legend\tCtrl+L')
        f2.AppendItem(viewLegendItem)
        menuBar.Append(f2, "&Options")

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

    """ Menu event methods """
    def onViewLegend(self, event=None):
        global viewLegend
        if viewLegend:
            viewLegend = False
        else:
            viewLegend = True
        self.Plot_Data()

    def onBasicView(self, event=None):
        self.Plot_Data()

    def onAdvancedView(self, event=None):
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
        key = event.KeyCode()
        if (key < wx.WXK_SPACE or  key > 255):  return

        if (event.ControlDown() and chr(key)=='C'): # Ctrl-C
            self.onClipboard(event=event)

    def onHelp(self, event=None):
        dlg = wx.MessageDialog(self, self.help_msg, "Quick Reference", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def onViewGrid(self, event=None):
        global viewGrid
        if viewGrid:
            viewGrid = False
        else:
            viewGrid = True
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
        file_choices = "CSV (*.csv)|*.csv"

        thisdir  = os.getcwd()

        # import output file
        dlg = wx.FileDialog(self, message='Import option prices and greeks (Outputs)',
                            defaultDir = thisdir, defaultFile='outputs.csv',
                            wildcard=file_choices, style=wx.OPEN)

        global fileReader
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            fileReader.loadOutputFile(path)
            self.Plot_Data()
            print('Opened csv file at %s' % path)

        # import input file
        dlg = wx.FileDialog(self, message='Import stock prices and other inputs (Inputs)',
                            defaultDir = thisdir, defaultFile='inputs.csv',
                            wildcard=file_choices, style=wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            fileReader.loadInputFile(path)
            self.Plot_Data()
            print('Opened csv file at %s' % path)

    def onExit(self,event=None):
        dlg = wx.MessageDialog(None, 'Are you sure to exit?', 'Confirm', wx.YES_NO|wx.NO_DEFAULT|wx.ICON_QUESTION)
        ret = dlg.ShowModal()
        if ret == wx.ID_YES:
            self.Destroy()

    """ GUI event methods """
    def onCallRadio(self, event=None):
        self.Plot_Data()

    def onPutRadio(self, event=None):
        self.Plot_Data() 

    def onDelta(self, event=None):
        self.Plot_Data()

    def onGamma(self, event=None):
        self.Plot_Data()

    def onRho(self, event=None):
        self.Plot_Data()

    def onTheta(self, event=None):
        self.Plot_Data()

    def onEpsilon(self, event=None):
        self.Plot_Data()

    def onStockSlider(self, event=None):
        self.Plot_Data()

    def onRateSlider(self, event=None):
        self.Plot_Data()

    def onVolatilSlider(self, event=None):
        self.Plot_Data()

    def ontimeStepSlider(self, event=None):
        self.Plot_Data()

    def Plot_Data(self):
        """ 2D graph plotter """
        global fileReader, viewGrid, viewLegend

        # t = numpy.arange(0.0,5.0,0.01)
        # s = numpy.sin(2.0*numpy.pi*t)
        # c = numpy.cos(0.4*numpy.pi*t)

        option_price = fileReader.getOptionPrice(self.callRadio.GetValue())
        delta = fileReader.getDeltaValues(self.callRadio.GetValue(), self.deltaCheck.IsChecked())
        gamma = fileReader.getGammaValues(self.callRadio.GetValue(), self.gammaCheck.IsChecked())
        vega = fileReader.getVegaValues(self.callRadio.GetValue(), self.epsilonCheck.IsChecked())
        theta = fileReader.getThetaValues(self.callRadio.GetValue(), self.thetaCheck.IsChecked())
        rho = fileReader.getRhoValues(self.callRadio.GetValue(), self.rhoCheck.IsChecked())

        self.axes.clear()
        self.axes.grid(viewGrid)
        p1, = self.axes.plot(option_price, label="Option Price")
        self.axes.plot(delta, label="Delta")
        self.axes.plot(gamma, label="Gamma")
        self.axes.plot(vega, label="Vega")
        self.axes.plot(theta, label="Theta")
        self.axes.plot(rho, label="Rho")

        if viewLegend:
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            # self.axes.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=1)
        self.canvas.draw()
