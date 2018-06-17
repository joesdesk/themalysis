# Sources:
# Closing frame. http://zetcode.com/wxpython/menustoolbars/

import wx
from .menubar import MenuBar

from ..topicmodelview.topiclist import TopicListCtrl as TopicList
from ..commentview.mainpanel import MainPanel as CommentView


class MainFrame(wx.Frame):
    '''Base for the main application frame.'''
    
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title='ThemeCrafter v0.0', size=(600,400))
        
        # Add the main menubar
        menubar = MenuBar()
        self.SetMenuBar(menubar)
        
        # Add splitter
        splitter = wx.SplitterWindow(self, style=wx.SP_BORDER|wx.SP_LIVE_UPDATE)
        splitter.SetSashGravity(0.35)
        
        # Add controls
        self.ctrl_topiclist = TopicList(splitter)
        self.ctrl_commentview = CommentView(splitter)
        
        # Split the frame
        splitter.SplitVertically(self.ctrl_topiclist, self.ctrl_commentview)
        
        # Add Frame specific bindings
        self.Bind(wx.EVT_MENU, self.Quit, id=wx.ID_EXIT)
        
        
    def Quit(self, e):
        '''Closes the frame.'''
        self.Close()
        
        