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

# from mayavi import mlab


class PlotFrame(wx.Frame):
    help_msg="""  Menus for
     Import...import project settings file
     Export...export figure (png, jpg) to file
     Print Setup...setup size of figure for printing
     Print Preview...preview printer page
     Print...send figure to a system printer
     Exit...end application

     Basic-2D...View basic 2D representation of data
     Advanced-2D...View 2D representation (with span selection control)
     Advanced-3D...View 3D representation of data

     View-Grid...Toggle grid
     View-Legend...Toggle legend
     View-Fill...Toggle fill representation of data (only for 2D)

     where 'figure' means an image of the matplotlib canvas

     In addition, "Ctrl-C" is bound to copy-figure-to-clipboard    
    """

    about_msg="""
        Option_price_visualisation v0.1  29-Aug-2013

        Nathan Floor, flrnat001@cs.uct.ac.za
    """

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Visualise Option Prices and Greeks", size=(300, 500))
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyEvent)

        self.fileReader = csvReader.Reader()
        self.viewLegend = False
        self.viewGrid = True
        self.viewFill = False
        self.current_view = 0
        self.time = numpy.arange(0, 31, 1)
        self.indmin = 0
        self.indmax = 31

        # initialise data arrays
        self.option_price = []
        self.delta = []
        self.gamma = []
        self.vega = []
        self.theta = []
        self.rho = []
        self.risidual = []
        
        # initialise secondary data sets
        self.option_price_fill = []
        self.time_span_fill = []
        self.delta_fill = []
        self.gamma_fill = []
        self.vega_fill = []
        self.theta_fill = []
        self.rho_fill = []
        
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
        self.SetSize(size=(850, 550))

    # on span-selection of graph
    def onselect(self, xmin, xmax):
        # initialise data sets
        option_price = []
        delta = []
        gamma = []
        theta = []
        rho = []
        vega = []
        maxYLimlist = []
        minYLimlist = []

        # identify the indices of new data set based on selection
        self.indmin = int(xmin)
        #self.indmax = numpy.searchsorted(t, (xmin, xmax))
        self.indmax = min(len(self.time)-1, int(xmax)+1)

        self.time_span_fill = self.time[self.indmin:self.indmax]
        if len(self.option_price) > 0:
            option_price = numpy.array(map(float, self.option_price[self.stock_bump]))
            self.option_price_fill = option_price[self.indmin:self.indmax]
            #  append to lists for axes limits
            maxYLimlist.append(max(self.option_price_fill))
            minYLimlist.append(min(self.option_price_fill))
            if not self.viewFill:
                self.line1.set_data(self.time_span_fill, self.option_price_fill)
        if len(self.delta) > 0:
            delta = numpy.array(map(float, self.delta[self.stock_bump]))
            self.delta_fill = delta[self.indmin:self.indmax]
            #  append to lists for axes limits
            maxYLimlist.append(max(self.delta_fill))
            minYLimlist.append(min(self.delta_fill))
            if not self.viewFill:
                self.line2.set_data(self.time_span_fill, self.delta_fill)
        if len(self.gamma) > 0:
            gamma = numpy.array(map(float, self.gamma[self.stock_bump]))
            self.gamma_fill = gamma[self.indmin:self.indmax]
            #  append to lists for axes limits
            maxYLimlist.append(max(self.gamma_fill))
            minYLimlist.append(min(self.gamma_fill))
            if not self.viewFill:
                self.line3.set_data(self.time_span_fill, self.gamma_fill)
        if len(self.theta) > 0:
            theta = numpy.array(map(float, self.theta[self.time_bump]))
            self.theta_fill = theta[self.indmin:self.indmax]
            #  append to lists for axes limits
            maxYLimlist.append(max(self.theta_fill))
            minYLimlist.append(min(self.theta_fill))
            if not self.viewFill:
                self.line4.set_data(self.time_span_fill, self.theta_fill)
        if len(self.rho) > 0:
            rho = numpy.array(map(float, self.rho[self.rate_bump]))
            self.rho_fill = rho[self.indmin:self.indmax]
            #  append to lists for axes limits
            maxYLimlist.append(max(self.rho_fill))
            minYLimlist.append(min(self.rho_fill))
            if not self.viewFill:
                self.line5.set_data(self.time_span_fill, self.rho_fill)
        if len(self.vega) > 0:
            vega = numpy.array(map(float, self.vega[self.volitile_bump]))
            self.vega_fill = vega[self.indmin:self.indmax]
            #  append to lists for axes limits
            maxYLimlist.append(max(self.vega_fill))
            minYLimlist.append(min(self.vega_fill))
            if not self.viewFill:
                self.line6.set_data(self.time_span_fill, self.vega_fill)
        if len(self.risidual) > 0:
            risidual = numpy.array(map(float, self.risidual[self.stock_bump]))
            self.risidual_fill = risidual[self.indmin:self.indmax]
            #  append to lists for axes limits
            maxYLimlist.append(max(self.risidual_fill))
            minYLimlist.append(min(self.risidual_fill))
            if not self.viewFill:
                self.line7.set_data(self.time_span_fill, self.risidual_fill)

        if len(maxYLimlist) > 0:
            maxYLim = max(maxYLimlist)
        else:
            maxYLim = 1
        if len(minYLimlist) > 0:
            minYLim = min(minYLimlist)
        else:
            minYLim = 0

        self.axes2.set_xlim(self.time_span_fill[0]-1, self.time_span_fill[-1]+1)
        self.axes2.set_ylim(minYLim, maxYLim)
        if not self.viewFill:
            self.canvas.draw()
        else:
            self.Plot_Data()

    def Build_Panel(self):
        self.panel = wx.Panel(self)

        # Create Figure and canvas objects
        self.fig = Figure((6.0, 4.0), 100)
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        self.axes = self.fig.add_subplot(111)

        # setup slider-widgets for controlling GUI
        self.sliderPanel = wx.Panel(self.panel)
        self.stockSlider_label = wx.StaticText(self.sliderPanel, -1, "Stock Price: ")
        self.stockSlider = wx.Slider(self.sliderPanel, value=5, minValue=1, maxValue=9, 
            pos=(20, 20), size=(100,-1), style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS)
        # self.stockSlider.SetTickFreq(9, 1)
        self.rateSlider_label = wx.StaticText(self.sliderPanel, -1, "Interest Rate: ")
        self.rateSlider = wx.Slider(self.sliderPanel, value=5, minValue=1, maxValue=9, 
            pos=(20, 20), size=(100,-1), style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS)
        self.rateSlider.SetTickFreq(1, 1)
        self.volatilSlider_label = wx.StaticText(self.sliderPanel, -1, "Volatility: ")
        self.volatilSlider = wx.Slider(self.sliderPanel, value=5, minValue=1, maxValue=9, 
            pos=(20, 20), size=(100,-1), style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS)
        self.volatilSlider.SetTickFreq(1, 1)
        self.timeStepSlider_label = wx.StaticText(self.sliderPanel, -1, "Time Step: ")
        self.timeStepSlider = wx.Slider(self.sliderPanel, value=5, minValue=1, maxValue=9, 
            pos=(20, 20), size=(100,-1), style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS)
        self.timeStepSlider.SetTickFreq(1, 1)

        self.Bind(wx.EVT_SLIDER, self.onStockSlider, self.stockSlider)
        self.Bind(wx.EVT_SLIDER, self.onRateSlider, self.rateSlider)
        self.Bind(wx.EVT_SLIDER, self.onVolatilSlider, self.volatilSlider)
        self.Bind(wx.EVT_SLIDER, self.ontimeStepSlider, self.timeStepSlider)        

        # setup options-widgets for controlling graphs
        self.callRadio = wx.RadioButton(self.panel, label="Call options", pos=(10, 10))
        self.putRadio = wx.RadioButton(self.panel, label="Put options", pos=(10, 30))
        self.callRadio.SetValue(True)        
        self.spaceKeeper = wx.StaticText(self.panel, -1, '')
        self.optionPriceCheck = wx.CheckBox(self.panel, label="view Option Price", pos=(20, 20))
        self.deltaCheck = wx.CheckBox(self.panel, label="show Delta effect", pos=(20, 20))
        self.gammaCheck = wx.CheckBox(self.panel, label="show Gamma", pos=(20, 20))
        self.rhoCheck = wx.CheckBox(self.panel, label="show Rho", pos=(20, 20))
        self.thetaCheck = wx.CheckBox(self.panel, label="show Theta", pos=(20, 20))
        self.vegaCheck = wx.CheckBox(self.panel, label="show Vega", pos=(20, 20))
        self.fillCheck = wx.CheckBox(self.panel, label="show fill feature", pos=(20, 20))
        self.risidualCheck = wx.CheckBox(self.panel, label="Show Risidual", pos=(20, 20))
        self.differenceCheck = wx.CheckBox(self.panel, label="Show Difference", pos=(20, 20))
        self.effectCheck = wx.CheckBox(self.panel, label="Show Greek's effect on option price", pos=(20, 20))
        self.effectCheck.SetValue(True)

        self.Bind(wx.EVT_RADIOBUTTON, self.onCallRadio, self.callRadio)
        self.Bind(wx.EVT_RADIOBUTTON, self.onPutRadio, self.putRadio)
        self.Bind(wx.EVT_CHECKBOX, self.onOptionPrice, self.optionPriceCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onDelta, self.deltaCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onGamma, self.gammaCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onRho, self.rhoCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onTheta, self.thetaCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onVega, self.vegaCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onRisidual, self.risidualCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onDifferenceCheck, self.differenceCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onShowEffects, self.effectCheck)
        self.Bind(wx.EVT_CHECKBOX, self.onShowFillEffect, self.fillCheck)

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
        self.sliderStaticBox = wx.StaticBox(self.sliderPanel, -1, 'Bump Sliders')
        self.sliderBorder = wx.StaticBoxSizer(self.sliderStaticBox, orient=wx.VERTICAL)
        self.flexiGridSizer.AddMany([(self.stockSlider_label), (self.stockSlider, 1, wx.ALL), 
            (self.rateSlider_label), (self.rateSlider, 1, wx.EXPAND),
            (self.volatilSlider_label), (self.volatilSlider, 1, wx.EXPAND),
            (self.timeStepSlider_label), (self.timeStepSlider, 1, wx.EXPAND)])
        self.sliderBorder.Add(self.flexiGridSizer, 1, wx.ALL, 5)
        self.sliderPanel.SetSizer(self.sliderBorder)
        self.vboxOptions.Add(self.sliderPanel, 0, flag=wx.ALIGN_LEFT|wx.ALL)

        # add border for type of option price
        self.optionsBorder = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, 'Option Price Type'), orient=wx.VERTICAL)
        self.flexiOptions = wx.FlexGridSizer(3, 1, 3, 10)
        self.flexiOptions.AddMany([(self.callRadio, 1, wx.EXPAND), 
            (self.putRadio, 1, wx.EXPAND), (self.optionPriceCheck, 1, wx.EXPAND)])            
        self.optionsBorder.Add(self.flexiOptions, 1, wx.ALL, 5)
        self.vboxOptions.Add(self.optionsBorder, 0, flag=wx.ALIGN_LEFT|wx.ALL|wx.GROW)
        
        # add border for greeks
        self.greekOptionsBorder = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, 'Greek effect Options'), orient=wx.VERTICAL)
        self.flexiOptions2 = wx.FlexGridSizer(6, 1, 3, 10)
        self.flexiOptions2.AddMany([(self.deltaCheck, 1, wx.EXPAND), (self.gammaCheck, 1, wx.EXPAND), 
            (self.rhoCheck, 1, wx.EXPAND), (self.thetaCheck, 1, wx.EXPAND), (self.vegaCheck, 1, wx.EXPAND)])
        self.greekOptionsBorder.Add(self.flexiOptions2, 1, wx.ALL, 5)
        self.vboxOptions.Add(self.greekOptionsBorder, 1, flag=wx.ALIGN_LEFT|wx.ALL|wx.GROW)
        #self.vboxOptions.AddSpacer(5)
        
        # add border for other checkable options
        self.otherOptionsBorder = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, 'Extra Options'), orient=wx.VERTICAL)
        self.flexiOptions3 = wx.FlexGridSizer(4, 1, 3, 10)
        self.flexiOptions3.AddMany([(self.fillCheck, 1, wx.EXPAND), (self.risidualCheck, 1, wx.EXPAND), (self.differenceCheck, 1, wx.EXPAND), 
            (self.effectCheck, 1, wx.EXPAND)])
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
        MENU_ABOUT = wx.NewId()

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

        optionsMenu = wx.Menu()
        viewGridItem = wx.MenuItem(optionsMenu, MENU_VIEW_GRID, 'View &Grid\tCtrl+G')
        optionsMenu.AppendItem(viewGridItem)
        viewLegendItem = wx.MenuItem(optionsMenu, MENU_LEGEND, 'View &Legend\tCtrl+L')
        optionsMenu.AppendItem(viewLegendItem)
        f1.AppendMenu(-1, "&Options", optionsMenu)

        menuBar.Append(f1, "&View")

        f2 = wx.Menu()
        f2.Append(MENU_HELP, "Quick &Reference",  "Quick Reference")
        f2.Append(MENU_ABOUT, "&About",  "About this interface")
        menuBar.Append(f2, "&Help")

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
        self.Bind(wx.EVT_MENU, self.onAbout,         id=MENU_ABOUT)
        self.Bind(wx.EVT_MENU, self.onBasicView,    id=MENU_BASIC)
        self.Bind(wx.EVT_MENU, self.onAdvancedView, id=MENU_ADVANCE)
        self.Bind(wx.EVT_MENU, self.onAdvanced3DView, id=MENU_3D)

    """ Menu event methods """
    def onViewLegend(self, event=None):
        if self.viewLegend:
            self.viewLegend = False
            self.Plot_Data()
        else:
            self.viewLegend = True
            # Shink current axis by 15%
            box = self.axes.get_position()
            self.axes.set_position([box.x0, box.y0, box.width * 0.88, box.height])
            # Put a legend to the right of the current axis
            self.axes.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':8})
            self.canvas.draw()

    def onBasicView(self, event=None):
        self.current_view = 0
        
        # show sliders panel
        self.sliderPanel.Show()
        self.toolbar.Show()
        self.panel.Layout()
        
        self.Plot_Data()

    def onAdvancedView(self, event=None):
        self.current_view = 1
        
        # show sliders panel
        self.sliderPanel.Show()
        self.toolbar.Hide()
        self.panel.Layout()
        
        self.Plot_Data()

    def onAdvanced3DView(self, event=None):
        self.current_view = 2
        
        # hide slider panel since will not be used
        self.sliderPanel.Hide()
        self.toolbar.Hide()
        self.panel.Layout()
        
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
        if (event.ControlDown() and chr(key)=='P'): # Ctrl-P
            self.onPrinterPreview(event=event)

    def onHelp(self, event=None):
        dlg = wx.MessageDialog(self, self.help_msg, "Quick Reference", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def onAbout(self, event=None):
        dlg = wx.MessageDialog(self, self.about_msg, "About", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def onViewGrid(self, event=None):
        if self.viewGrid:
            self.viewGrid = False
        else:
            self.viewGrid = True
        for a in self.fig.axes:
            a.grid(self.viewGrid)
        self.canvas.draw()

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
            projectDir = path.rsplit('/', 1)[0]
            #projectDir = path.rsplit('\\', 1)[0]
            
            # this also involves reading in all the data
            self.number_bumps = self.fileReader.loadSettingsFile(path, projectDir, self.statusbar)

            # change slider range to mach number of bumps just read in TODO

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
    def onShowFillEffect(self, event=None):
        if self.fillCheck.IsChecked():
            self.viewFill = True
        else:
            self.viewFill = False
        self.Plot_Data()

    def onCallRadio(self, event=None):
        self.option_price = self.fileReader.getOptionPrice(self.callRadio.GetValue(), 
            self.optionPriceCheck.IsChecked())
        self.delta = self.fileReader.getDeltaValues(self.callRadio.GetValue(), 
            self.deltaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.gamma = self.fileReader.getGammaValues(self.callRadio.GetValue(), 
            self.gammaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.vega = self.fileReader.getVegaValues(self.callRadio.GetValue(), 
            self.vegaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.theta = self.fileReader.getThetaValues(self.callRadio.GetValue(), 
            self.thetaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.rho = self.fileReader.getRhoValues(self.callRadio.GetValue(), 
            self.rhoCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.risidual = self.fileReader.getRisidualValues(self.callRadio.GetValue(), self.risidualCheck.IsChecked(),
            self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.Plot_Data()

    def onPutRadio(self, event=None):
        self.option_price = self.fileReader.getOptionPrice(self.callRadio.GetValue(), 
            self.optionPriceCheck.IsChecked())
        self.delta = self.fileReader.getDeltaValues(self.callRadio.GetValue(), 
            self.deltaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.gamma = self.fileReader.getGammaValues(self.callRadio.GetValue(), 
            self.gammaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.vega = self.fileReader.getVegaValues(self.callRadio.GetValue(), 
            self.vegaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.theta = self.fileReader.getThetaValues(self.callRadio.GetValue(), 
            self.thetaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.rho = self.fileReader.getRhoValues(self.callRadio.GetValue(), 
            self.rhoCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.risidual = self.fileReader.getRisidualValues(self.callRadio.GetValue(), self.risidualCheck.IsChecked(),
            self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.Plot_Data() 

    def onOptionPrice(self, event=None):
        self.option_price = self.fileReader.getOptionPrice(self.callRadio.GetValue(), 
                self.optionPriceCheck.IsChecked())
        self.Plot_Data()

    def onDelta(self, event=None):
        self.delta = self.fileReader.getDeltaValues(self.callRadio.GetValue(), 
            self.deltaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.Plot_Data()

    def onGamma(self, event=None):
        self.gamma = self.fileReader.getGammaValues(self.callRadio.GetValue(), 
            self.gammaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())

        self.Plot_Data()

    def onRho(self, event=None):
        self.rho = self.fileReader.getRhoValues(self.callRadio.GetValue(), 
            self.rhoCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.Plot_Data()

    def onTheta(self, event=None):
        self.theta = self.fileReader.getThetaValues(self.callRadio.GetValue(), 
            self.thetaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.Plot_Data()

    def onVega(self, event=None):
        self.vega = self.fileReader.getVegaValues(self.callRadio.GetValue(), 
            self.vegaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.Plot_Data()

    def onRisidual(self, event=None):
        self.risidual = self.fileReader.getRisidualValues(self.callRadio.GetValue(), self.risidualCheck.IsChecked(),
            self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())

        # print(self.risidual)
        self.Plot_Data()

    def onShowEffects(self, event=None):
        if not self.effectCheck.IsChecked():
            warning_msg = """
                This setting will plot the value of the greeks, but not terms of the option price. This means that the greek graphs will no-longer be comparable. You will still be able to plot the greeks against each other though.

                Do you want to continue?
            """
            dlg = wx.MessageDialog(self, warning_msg, "Take Note", wx.YES_NO | wx.ICON_INFORMATION)
            ret = dlg.ShowModal()
            if ret == wx.ID_NO:
                dlg.Destroy()
                self.effectCheck.SetValue(True)
                return
            dlg.Destroy()

        # reload and replot data
        self.delta = self.fileReader.getDeltaValues(self.callRadio.GetValue(), 
            self.deltaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.gamma = self.fileReader.getGammaValues(self.callRadio.GetValue(), 
            self.gammaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.vega = self.fileReader.getVegaValues(self.callRadio.GetValue(), 
            self.vegaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.theta = self.fileReader.getThetaValues(self.callRadio.GetValue(), 
            self.thetaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.rho = self.fileReader.getRhoValues(self.callRadio.GetValue(), 
            self.rhoCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.risidual = self.fileReader.getRisidualValues(self.callRadio.GetValue(), self.risidualCheck.IsChecked(),
            self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())

        self.Plot_Data()

    def onDifferenceCheck(self, event=None):
        # reload and replot data
        self.delta = self.fileReader.getDeltaValues(self.callRadio.GetValue(), 
            self.deltaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.gamma = self.fileReader.getGammaValues(self.callRadio.GetValue(), 
            self.gammaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.vega = self.fileReader.getVegaValues(self.callRadio.GetValue(), 
            self.vegaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.theta = self.fileReader.getThetaValues(self.callRadio.GetValue(), 
            self.thetaCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.rho = self.fileReader.getRhoValues(self.callRadio.GetValue(), 
            self.rhoCheck.IsChecked(), self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.risidual = self.fileReader.getRisidualValues(self.callRadio.GetValue(), self.risidualCheck.IsChecked(),
            self.differenceCheck.IsChecked(), self.effectCheck.IsChecked())
        self.Plot_Data()

    def onStockSlider(self, event=None):
        self.statusbar.SetStatusText("Stock price bump: "+str(self.stockSlider.GetValue()))
        # print(self.stockSlider.GetValue()-1)
        self.stock_bump = self.stockSlider.GetValue()-1
        self.Plot_Data()

    def onRateSlider(self, event=None):
        self.statusbar.SetStatusText("Interest Rate bump: "+str(self.rateSlider.GetValue()))
        # print(self.stockSlider.GetValue()-1)
        self.rate_bump = self.rateSlider.GetValue()-1
        self.Plot_Data()

    def onVolatilSlider(self, event=None):
        self.statusbar.SetStatusText("Volatility bump: "+str(self.volatilSlider.GetValue()))
        # print(self.stockSlider.GetValue()-1)
        self.volitile_bump = self.volatilSlider.GetValue()-1
        self.Plot_Data()

    def ontimeStepSlider(self, event=None):
        self.statusbar.SetStatusText("Time step bump: "+str(self.timeStepSlider.GetValue()))
        # print(self.stockSlider.GetValue()-1)
        self.time_bump = self.timeStepSlider.GetValue()-1
        self.Plot_Data()
        self.Plot_Data()

    """ Graph plotting methods """
    def clearPlots(self):
        """ Clear all graphs and plots for next draw """
        for a in self.fig.axes:
            self.fig.delaxes(a)

    def Plot_Data(self):
        if self.current_view == 1:
            self.Plot_Data_advanced()
        elif self.current_view == 2:
            self.Plot_Data_3D()
        elif self.current_view == 0:
            """ Basic 2D graph plotter """
            self.clearPlots()
            
            self.axes = self.fig.add_subplot(111) # can use add_axes, but then nav-toolbar would not work
            self.axes.set_xlim(0, 30)
            self.axes.grid(self.viewGrid)

            # plot graphs here
            p = []
            if self.viewFill and len(self.option_price) > 0:
                p = numpy.array(map(float, self.option_price[self.stock_bump]))
            if len(self.option_price) > 0:
                self.axes.plot(self.time, self.option_price[self.stock_bump], label="Option Price", color='blue')
            if len(self.delta) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.delta[self.stock_bump])
                    self.axes.fill_between(self.time, p, s, where=s>=p, facecolor='green', interpolate=True)
                    self.axes.fill_between(self.time, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.axes.plot(self.delta[self.stock_bump], label="Delta", color='darkgreen')
            if len(self.gamma) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.gamma[self.stock_bump])
                    self.axes.fill_between(self.time, p, s, where=s>=p, facecolor='cyan', interpolate=True)
                    self.axes.fill_between(self.time, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.axes.plot(self.gamma[self.stock_bump], label="Gamma", color='cyan')
            if len(self.vega) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.vega[self.volitile_bump])
                    self.axes.fill_between(self.time, p, s, where=s>=p, facecolor='aqua', interpolate=True)
                    self.axes.fill_between(self.time, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.axes.plot(self.vega[self.volitile_bump], label="Vega", color='aqua')
            if len(self.theta) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.theta[self.time_bump])
                    self.axes.fill_between(self.time, p, s, where=s>=p, facecolor='yellow', interpolate=True)
                    self.axes.fill_between(self.time, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.axes.plot(self.time, self.theta[self.time_bump], label="Theta", color='red')
            if len(self.rho) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.rho[self.rate_bump])
                    self.axes.fill_between(self.time, p, s, where=s>=p, facecolor='olive', interpolate=True)
                    self.axes.fill_between(self.time, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.axes.plot(self.time, self.rho[self.rate_bump], label="Rho", color='olive')
            if len(self.risidual) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.risidual[self.stock_bump])
                    self.axes.fill_between(self.time, p, s, where=s>=p, facecolor='chartreuse', interpolate=True)
                    self.axes.fill_between(self.time, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.axes.plot(self.time, self.risidual[self.stock_bump], label="Risidual", color='black')

            # set caption and axes labels
            self.axes.set_xlabel('Time (Daily)')
            if self.effectCheck.IsChecked():
                self.axes.set_ylabel('Price (Rands)')
                if hasattr(self, 'title'):
                    self.title.set_text('Option Prices and breakdown of the effects of Greeks')
                else:
                    self.title = self.fig.suptitle('Option Prices and breakdown of the effects of Greeks')
            else:
                self.axes.set_ylabel('Greek Value')
                if hasattr(self, 'title'):
                    self.title.set_text('Raw Greek values not in terms of option price')
                else:
                    self.title = self.fig.suptitle('Greek values not in terms of option price')

            if self.viewLegend:
                # Shink current axis by 15%
                box = self.axes.get_position()
                self.axes.set_position([box.x0, box.y0, box.width * 0.88, box.height])
                # Put a legend to the right of the current axis
                self.axes.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':8})

            self.canvas.draw()

    def Plot_Data_advanced(self):
        """ Advanced 2D plotter """
        self.clearPlots()
        self.axes = self.fig.add_subplot(211)
        self.axes.set_xlim(0, 30)
        self.axes.grid(self.viewGrid)

        p = []
        if self.viewFill and len(self.option_price) > 0:
            p = numpy.array(map(float, self.option_price[self.stock_bump]))
        if True:
            if len(self.option_price) > 0:
                self.axes.plot(self.time, self.option_price[self.stock_bump], label="Option Price", color='blue')
            if len(self.delta) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.delta[self.stock_bump])
                    self.axes.fill_between(self.time, p, s, where=s>=p, facecolor='green', interpolate=True)
                    self.axes.fill_between(self.time, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.axes.plot(self.delta[self.stock_bump], label="Delta", color='green')
            if len(self.gamma) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.gamma[self.stock_bump])
                    self.axes.fill_between(self.time, p, s, where=s>=p, facecolor='cyan', interpolate=True)
                    self.axes.fill_between(self.time, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.axes.plot(self.gamma[self.stock_bump], label="Gamma", color='cyan')
            if len(self.vega) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.vega[self.volitile_bump])
                    self.axes.fill_between(self.time, p, s, where=s>=p, facecolor='aqua', interpolate=True)
                    self.axes.fill_between(self.time, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.axes.plot(self.vega[self.volitile_bump], label="Vega", color='aqua')
            if len(self.theta) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.theta[self.time_bump])
                    self.axes.fill_between(self.time, p, s, where=s>=p, facecolor='yellow', interpolate=True)
                    self.axes.fill_between(self.time, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.axes.plot(self.time, self.theta[self.time_bump], label="Theta", color='red')
            if len(self.rho) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.rho[self.rate_bump])
                    self.axes.fill_between(self.time, p, s, where=s>=p, facecolor='olive', interpolate=True)
                    self.axes.fill_between(self.time, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.axes.plot(self.time, self.rho[self.rate_bump], label="Rho", color='olive')
            if len(self.risidual) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.risidual[self.stock_bump])
                    self.axes.fill_between(self.time, p, s, where=s>=p, facecolor='chartreuse', interpolate=True)
                    self.axes.fill_between(self.time, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.axes.plot(self.time, self.risidual[self.stock_bump], label="Risidual", color='black')

        self.axes2 = self.fig.add_subplot(212)
        self.axes2.grid(self.viewGrid)

        self.time_span_fill = self.time[self.indmin:self.indmax]
        if len(self.option_price) > 0:
            self.option_price_fill = numpy.array(map(float, self.option_price[self.stock_bump][self.indmin:self.indmax]))
        else:
            self.option_price_fill = []
        if self.viewFill:
            p = self.option_price_fill
        if len(self.delta) > 0:
            self.delta_fill = numpy.array(map(float, self.delta[self.stock_bump][self.indmin:self.indmax]))
        else:
            self.delta_fill = []
        if len(self.gamma) > 0:
            self.gamma_fill = numpy.array(map(float, self.gamma[self.stock_bump][self.indmin:self.indmax]))
        else:
            self.gamma_fill = []
        if len(self.rho) > 0:
            self.rho_fill = numpy.array(map(float, self.rho[self.rate_bump][self.indmin:self.indmax]))
        else:
            self.rho_fill = []
        if len(self.theta) > 0:
            self.theta_fill = numpy.array(map(float, self.theta[self.time_bump][self.indmin:self.indmax]))
        else:
            self.theta_fill = []
        if len(self.vega) > 0:
            self.vega_fill = numpy.array(map(float, self.vega[self.volitile_bump][self.indmin:self.indmax]))
        else:
            self.vega_fill = []
        if len(self.risidual) > 0:
            self.risidual_fill = numpy.array(map(float, self.risidual[self.stock_bump][self.indmin:self.indmax]))
        else:
            self.risidual_fill = []

        if True:
            if len(self.option_price) > 0:
                    self.line1, = self.axes2.plot(self.time_span_fill, self.option_price_fill, label="Option Price", color='blue')
            if len(self.delta) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.delta_fill)
                    self.axes2.fill_between(self.time_span_fill, p, s, where=s>=p, facecolor='green', interpolate=True)
                    self.axes2.fill_between(self.time_span_fill, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.line2, = self.axes2.plot(self.time_span_fill, self.delta_fill, label="Delta", color='green')
            if len(self.gamma) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.gamma_fill)
                    self.axes2.fill_between(self.time_span_fill, p, s, where=s>=p, facecolor='cyan', interpolate=True)
                    self.axes2.fill_between(self.time_span_fill, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.line3, = self.axes2.plot(self.time_span_fill, self.gamma_fill, label="Gamma", color='cyan')
            if len(self.theta) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.theta_fill)
                    self.axes2.fill_between(self.time_span_fill, p, s, where=s>=p, facecolor='yellow', interpolate=True)
                    self.axes2.fill_between(self.time_span_fill, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.line4, = self.axes2.plot(self.time_span_fill, self.theta_fill, label="Theta", color='red')
            if len(self.rho) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.rho_fill)
                    self.axes2.fill_between(self.time_span_fill, p, s, where=s>=p, facecolor='olive', interpolate=True)
                    self.axes2.fill_between(self.time_span_fill, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.line5, = self.axes2.plot(self.time_span_fill, self.rho_fill, label="Rho", color='olive')
            if len(self.vega) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.vega_fill)
                    self.axes2.fill_between(self.time_span_fill, p, s, where=s>=p, facecolor='aqua', interpolate=True)
                    self.axes2.fill_between(self.time_span_fill, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.line6, = self.axes2.plot(self.time_span_fill, self.vega_fill, label="Vega", color='aqua')
            if len(self.risidual) > 0:
                if self.viewFill and len(self.option_price) > 0:
                    s = numpy.array(self.risidual_fill)
                    self.axes2.fill_between(self.time_span_fill, p, s, where=s>=p, facecolor='chartreuse', interpolate=True)
                    self.axes2.fill_between(self.time_span_fill, p, s, where=s<=p, facecolor='red', interpolate=True)
                self.line7, = self.axes2.plot(self.time_span_fill, self.risidual_fill, label="Risidual", color='black')

        # set limits for x and y axes
        self.axes2.set_xlim(self.time_span_fill[0], self.time_span_fill[-1])
        # self.axes2.set_ylim(min(p, key=float), max(p, key=float))

        # set caption and axes labels
        self.axes2.set_xlabel('Time (Daily)')
        self.axes2.set_ylabel('Price (Rands)')
        self.axes.set_ylabel('Price (Rands)')

        # set useblit True on gtkagg for enhanced performance
        self.span = SpanSelector(self.axes, self.onselect, 'horizontal', useblit=True, rectprops=dict(alpha=0.5, facecolor='red'))

        if self.viewLegend:
                # Shink current axis by 15%
                box = self.axes.get_position()
                self.axes.set_position([box.x0, box.y0, box.width * 0.88, box.height])
                # Put a legend to the right of the current axis
                self.axes.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':8})

        self.canvas.draw()

    def Plot_Data_3D(self):
        """ Advanced 3D plotter """
        # plot graphs
        self.clearPlots()
            
        self.axes = self.fig.add_subplot(111, projection='3d') # can use add_axes, but then nav-toolbar would not work
        self.axes.grid(self.viewGrid)

        b = numpy.arange(0, 9, 1)
        X2D, Y2D = numpy.meshgrid(self.time, b)
        Z2D = None
        
        # plot option price surface
        if len(self.option_price) > 0:
            Z2D = [[float(string) for string in inner] for inner in self.option_price]            
            surf = self.axes.plot_surface(X2D, Y2D, Z2D, rstride=1, cstride=1,
                antialiased=False, alpha=0.75, cmap=cm.afmhot, zorder=0.5)  #cm.coolwarm, cm.winter, cm.autumn
            cbar = self.fig.colorbar(surf, shrink=0.5, aspect=5)
            cbar.set_label('Option Price', rotation=90)

            # X2D, Y2D = numpy.mgrid[self.time, b]
            # print(X2D)
            # s = mlab.surf(Z2D)
            # mlab.show()

        # plot greek surfaces
        if len(self.delta) > 0:
            Z2D = [[float(string) for string in inner] for inner in self.delta]
            self.axes.plot_surface(X2D, Y2D, Z2D, rstride=1, cstride=1,
                antialiased=False, alpha=0.75, color='green')

        if len(self.gamma) > 0:
            Z2D = [[float(string) for string in inner] for inner in self.gamma]
            self.axes.plot_surface(X2D, Y2D, Z2D, rstride=1, cstride=1,
                antialiased=False, alpha=0.75, color='cyan')
                
        if len(self.theta) > 0:
            Z2D = [[float(string) for string in inner] for inner in self.theta]
            self.axes.plot_surface(X2D, Y2D, Z2D, rstride=1, cstride=1,
                antialiased=False, alpha=0.75, color='red')
                
        if len(self.rho) > 0:
            Z2D = [[float(string) for string in inner] for inner in self.rho]
            self.axes.plot_surface(X2D, Y2D, Z2D, rstride=1, cstride=1,
                antialiased=False, alpha=0.75, color='olive')
                
        if len(self.vega) > 0:
            Z2D = [[float(string) for string in inner] for inner in self.vega]
            self.axes.plot_surface(X2D, Y2D, Z2D, rstride=1, cstride=1,
                antialiased=False, alpha=0.75, color='aqua')

        if len(self.risidual) > 0:
            Z2D = [[float(string) for string in inner] for inner in self.risidual]
            self.axes.plot_surface(X2D, Y2D, Z2D, rstride=1, cstride=1,
                antialiased=False, alpha=0.75, color='black')
        
        if Z2D != None:
            # cset1 = self.axes.contourf(X2D, Y2D, Z2D, zdir='z', offset=300, cmap=cm.afmhot)
            cset2 = self.axes.contourf(X2D, Y2D, Z2D, zdir='x', offset=0, cmap=cm.coolwarm)
            cset3 = self.axes.contour(X2D, Y2D, Z2D, zdir='y', offset=-0.3, cmap=cm.winter)
            # cset = self.axes.contour(X2D, Y2D, Z2D, zdir='y', offset=10, cmap=cm.afmhot)
            # cbar = self.fig.colorbar(cset1, shrink=0.7, aspect=3)
            # cbar = self.fig.colorbar(cset2, shrink=0.7, aspect=3)
            # cbar = self.fig.colorbar(cset3, shrink=0.5, aspect=5)
            # cbar.set_label('Option Proce', rotation=90)

        self.axes.set_xlabel('Time (Days)')
        self.axes.set_xlim(0, 35)
        self.axes.set_ylabel('Bump Size')
        #~ self.axes.set_ylim(-3, 8)
        self.axes.set_zlabel('Price (Rands)')
        # ~ self.axes.set_zlim(-100, 100)

        self.canvas.draw()
