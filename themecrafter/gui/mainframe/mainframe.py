# Sources:
# Closing frame. http://zetcode.com/wxpython/menustoolbars/

import wx
from .menubar import MenuBar

from ..topicmodelview.topiclist import TopicListCtrl as TopicList
from ..commentview.main import CommentView


class MainFrame(wx.Frame):
    '''Base for the main application frame.'''
    
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, \
            title='ThemeCrafter v0.0', size=(800,500))
        
        # Add the main menubar
        menubar = MenuBar()
        self.SetMenuBar(menubar)
        
        # Add splitter
        splitter = wx.SplitterWindow(self, style=wx.SP_BORDER|wx.SP_LIVE_UPDATE)
        splitter.SetSashGravity(0.3)
        
        # Add controls
        self.ctrl_topiclist = TopicList(splitter)
        self.ctrl_commentview = CommentView(splitter)
        
        # Split the frame
        splitter.SplitVertically(self.ctrl_topiclist, self.ctrl_commentview)
        
        # Add Status bar
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('This goes in your statusbar')
        
        # Add Frame specific bindings
        self.Bind(wx.EVT_MENU, self.quit, id=wx.ID_EXIT)
        
    
    def set_topics(self, df):
        self.ctrl_topiclist.set_data(df)
        
    def quit(self, e):
        '''Closes the frame.'''
        self.Close()
        
        