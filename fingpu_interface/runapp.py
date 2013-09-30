#! /usr/bin/python

import wx
import interface

if __name__ == '__main__':
    print 'Program started...'
    app = wx.PySimpleApp()
    fig = interface.PlotFrame()
    fig.Show(True)
    size = fig.GetSize()
    fig.SetMinSize((size[0], size[1]))
    app.MainLoop()