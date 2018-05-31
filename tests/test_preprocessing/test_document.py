import pytest

from themecrafter.preprocessing.docelements import TokenElement, \
    SentenceElement, DocumentElement, CorpusElement


def test_token_element():
    txt = 'The'
    token = TokenElement(txt)
    assert token.as_plain_text()==txt
    

def test_sentence_element():
    txt = 'The quick brown fox jumped over the lazy dog.'
    sentence = SentenceElement(txt)
    assert sentence.as_plain_text()==txt
    
    
def test_document_element():
    txt = 'An independent clause has the ability to stand alone as a sentence. It always makes a complete thought. A dependent clause cannot stand alone, even though it has a subject and a verb.'
    document = DocumentElement(txt)
    assert document.as_plain_text()==txt

    
if __name__=='__main__':
    test_token_element()
    test_sentence_element()
    test_document_element()