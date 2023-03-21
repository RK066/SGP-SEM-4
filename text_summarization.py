import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation  
from heapq import nlargest

text= """Generating random paragraphs can be an excellent way for writers to get their creative flow going at the beginning of the day. The writer has no idea what topic the random paragraph will be about when it appears. This forces the writer to use creativity to complete one of three common writing challenges. The writer can use the paragraph as the first one of a short story and build upon it. A second option is to use the random paragraph somewhere in a short story they create. The third option is to have the random paragraph be the ending paragraph in a short story. No matter which of these challenges is undertaken, the writer is forced to use creativity to incorporate the paragraph into their writing."""

def summarizer(rawdocs):
    
    stopwords=list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    #print(doc)
    tokens = [token.text for token in doc]
    #print(tokens)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text] +=1
                
    #print(word_freq)
    max_freq = max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
        
    # print(word_freq)
    
    sent_tokens = [sent for sent in doc.sents]
    #print(sent_tokens)
    
    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if  word.text in word_freq.keys():
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = word_freq[word.text]
                    else:
                        sent_scores[sent] += word_freq[word.text]
    #print(sent_scores)

    select_len = int(len(sent_tokens)*0.3)
    #print(select_len)

    summary = nlargest(select_len, sent_scores, key = sent_scores.get)
    #print(summary)                                        

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    #print(summary)   
    #print("length of original text ",len(text.split(' ')))
    #print("length of summary ",len(summary.split(' ')))
    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))
 