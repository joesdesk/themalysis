from ..nlp.corpusparser import CorpusParser
from ..nlp.utils import open_tree, show_tree, save_tree, tree2string

from ..preprocessing.labeltransform import LabelTransform
from ..nlp.nltklemmatizer import NOUN_POS, VERB_POS, ADJ_POS

from ..preprocessing import BagOfWords

from ..models.gensimlda import GensimLDA
from ..models.utils import hard_assignments

from pandas import DataFrame
from .html import HTMLInterface


class MainInterface:
    '''Container for all objects of interation for the GUI.'''
    
    def __init__(self):
        '''Creates the variables.'''
        # Parsed XML
        self.docs = None
        self.tree = None
        
        # Sub-interfaces
        self.html = None
        self.labeltransform = LabelTransform()
        self.model = None
        self.topics = None
        
    def load_docs(self, docs):
        '''Loads the documents to be analyzed.'''
        self.docs = docs
        parser = CorpusParser()
        tree = parser.parse(self.docs)
        show_tree(tree)
        xmlstring = tree2string(tree)
        self.html = HTMLInterface(xmlstring)
        
    def loadxml(self):
        '''Load XML into interface'''
        file = "M:/themecrafter/parsed/NLTKPlain2_NEW.xml"
        self.tree = open_tree(file)
        
        xmlstring = tree2string(self.tree)
        self.html = HTMLInterface(xmlstring)
        
    def savexml(self):
        '''Save XML into a file'''
        #filename = ""
        #save_tree(self.tree, filename)
        # Save results to file
        #dir = "M:/themecrafter/labelled/"
        #save_tree(tree, dir+"NLTKPlain2-STANDARD.xml")
        pass
        
    def do_model(self):
        bow = BagOfWords(tokenlabel='label', doc_sel="DOCUMENT")
        bow.fit(self.tree)
        
        # Bag of words representation of each document (sentence)
        bows = bow.bows_
        # Corresponding tree elements for later retagging
        tags = bow.tags_
        print(bows)
        
        # Get model...
        self.model = GensimLDA(bows)
        self.model.fit(k_topics=10)
        
        V = self.model.get_document_topic_matrix()
        y = hard_assignments(V)
        
        for i, t in enumerate(tags):
            t.attrib['topic'] = str(y[i])
        
        # Create data frame with topics
        df = DataFrame(columns=['topic','words'])
        for i, ws in enumerate(self.model.get_topic_bows(7)):
            topic = 'topic {:d}'.format(i+1)
            words = ', '.join(ws)
            df = df.append({'topic':topic,'words':words}, ignore_index=True)
        #self.get_topics(df)
        self.topics = df
        
    def feat_sel(self):
        '''Performs feature selection.'''
        if self.tree is not None:
            self.label(self.tree)
            show_tree(self.tree)
            
    def get_topics(self):
        if self.topics is not None:
            return self.topics
        
    def get_html(self):
        htmlstring = self.html.render(0)
        return htmlstring
        
    def label(self, tree):

        # Flags
        LEMMATIZE = True ## Don't change

        # Remove stopwords and punctuations
        RM_STOPWORDS = True  ## Don't change
        RM_PUNCT = True  ## Don't change

        # Remove short words
        RM_CHAR_LEN = 2  ## Don't change

        # Include only nouns
        KEEP_NOUNS = True  ## Don't change
        KEEP_VERBS = True
        KEEP_ADJ = False  ## Don't change
        KEEP_ALLPOS = True  ## 

        # Extra words to exclude 
        BLACKLIST = []

        # Initialize labeller
        labeltransform = LabelTransform(labelname='label', lemmatize=LEMMATIZE, \
            rm_stopwords=RM_STOPWORDS, rm_punctuation=RM_PUNCT, \
            rm_char_len=RM_CHAR_LEN)
            
        labeltransform.pos_whitelist=[]
        if KEEP_NOUNS:
            labeltransform.pos_whitelist.extend(NOUN_POS)
        if KEEP_VERBS:
            labeltransform.pos_whitelist.extend(VERB_POS)
        if KEEP_ADJ:
            labeltransform.pos_whitelist.extend(ADJ_POS)
        if KEEP_ALLPOS:
            labeltransform.pos_whitelist=None
            
        labeltransform.label_blacklist = BLACKLIST

        # Perform labellling
        labeltransform.fit(tree)
        
        
if __name__=='__main__':
    interface = MainInterface()
    
    interface.loadxml()
    interface.label(interface.tree)
    
    interface.do_model()