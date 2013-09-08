#! /usr/bin/python

import wx
import interface

if __name__ == '__main__':
    app = wx.PySimpleApp()
    fig = interface.PlotFrame()
    fig.Show(True)
    app.MainLoop()