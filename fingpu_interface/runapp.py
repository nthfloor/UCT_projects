#! /usr/bin/python

import wx
import interface


start_msg= """ 
    Use Menus to import a data and test printing.
    Data must be in one folder containing a project settings file.
    Ctrl-C to copy plot image to clipboard.
"""


if __name__ == '__main__':
    print 'Program started...'
    app = wx.PySimpleApp()
    fig = interface.PlotFrame()
    fig.Show(True)

    dlg = wx.MessageDialog(fig, start_msg, "Welcome", wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()

    size = fig.GetSize()
    fig.SetMinSize((size[0], size[1]))
    app.MainLoop()