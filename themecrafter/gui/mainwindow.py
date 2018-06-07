import wx

from pandas import DataFrame

from .mainwidgets.mainmenu import MainMenuBar

from .mainwidgets.mainsplitter import MainWindowSplitter
from .commentview import CommentView
from .elementlist.tokenlist import TokenListCtrl
from .plotting.mtplot import CanvasPanel
from .topicmodelview.topiclist import MyPanel as TopicListCtrl

from ..nlp.utils import open_tree, tree2string
from ..interface.html2 import HTMLTransform

from . import EVT_DATA_LOAD

# https://wxpython.org/Phoenix/docs/html/events_overview.html#custom-event-summary
# event propagation http://zetcode.com/wxpython/events/

class MainWindow(wx.Frame):
    '''
    This window is the one containing the main controls and panels
    of the program.
    '''

    def __init__(self, parent, title=""):
        '''
        Initializes the main window.
        '''

        # Since we will use a toolbar, we use the wx.Frame
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=title, size=(800,600))

        # Create a new session with the winddow to interact with package routines

        # Add a main menu
        main_menubar = MainMenuBar()
        self.SetMenuBar(main_menubar)

            # See https://wiki.wxpython.org/self.Bind%20vs.%20self.button.Bind
        #self.Bind(wx.EVT_MENU, self.data_loaded, main_menubar)
        self.Bind(EVT_DATA_LOAD, self.data_loaded)
        
        # Add splitters to obtain 4 panels on which to add widgets.
        main_splitter = MainWindowSplitter(self)
        LT_panel = main_splitter.LT_panel
        LB_panel = main_splitter.LB_panel
        RT_panel = main_splitter.RT_panel
        RB_panel = main_splitter.RB_panel

        # Add widget to read comments
        RT_sizer = wx.BoxSizer(wx.VERTICAL)

        self.commentview = CommentView(RT_panel)


        RT_sizer.Add(self.commentview, proportion=1, flag=wx.EXPAND|wx.ALL)
        RT_panel.SetSizer(RT_sizer)


        # Add widget to tabulate cells
        LB_sizer = wx.BoxSizer(wx.VERTICAL)

        # List of vocabulary, tokens and n-grams
        notebook = wx.Notebook(LB_panel)
        
        self.token_list_ctrl = TokenListCtrl(notebook)
        
        notebook.AddPage(self.token_list_ctrl, 'Tokens')
        
        LB_sizer.Add(notebook, proportion=1, flag=wx.EXPAND|wx.ALL)
        LB_panel.SetSizer(LB_sizer)
        
        # Add widget to list topics
        LT_sizer = wx.BoxSizer(wx.VERTICAL)
        self.topic_list_ctrl = TopicListCtrl(LT_panel)
        LT_sizer.Add(self.topic_list_ctrl, proportion=1, flag=wx.EXPAND|wx.ALL)
        LT_panel.SetSizer(LT_sizer)
        
        self.topic_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.sel_topic)
        
        # Add plot to diagram
        RB_sizer = wx.BoxSizer(wx.VERTICAL)
        plot = CanvasPanel(RB_panel)
        RB_sizer.Add(plot, proportion=1, flag=wx.EXPAND|wx.ALL)
        RB_panel.SetSizer(RB_sizer)
        
        # Finally, add the interface
        self.html = None
        

		
    def data_loaded(self, evt):
        data = evt.attr
        print("event reached mainwindow")
        
        #session = PreprocessingSession()
        #session.load_docs(data)
        #session.docs_to_tree()
        tree = open_tree('M:/themecrafter/results/NLTKPlain2_topwords.xml')
        xmlstring = tree2string(tree)
        #print("Session started.")
        
        self.html = HTMLTransform(xmlstring)
        
        self.html.highlight('student', '#CCCCCC')
        
        pages = [self.html.show_page(i) for i in range(self.html.n_pages)]
        #print(pages[1])    
        
        self.commentview.set_data(pages)
        #print("Html Page set")
        
        #tokens = session.tokens_summary()
        #print('Get tokens summary')
        
        #tokens = DataFrame([(4,2),(2,2),(2,22)], columns=['swe','wer'])
        #self.token_list_ctrl.set_data(tokens)
		
        
    def sel_topic(self, event):
        '''Handles the selection of a topic.'''
        
        # Obtain the topic index
        index = event.GetIndex()
        if self.html is not None:
            self.html.highlight('student', "#DDDDDD")
        
        # Select the topic through the interface to obtain pages.