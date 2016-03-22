#Title:         NewsName Matcher
#Orig. Author:  Sasan Bahadaran
#Forked by:     Matt Anderson
#Date:          3/15/16
#Organization:  District Data Labs

##############################################
#   IMPORTS
##############################################
import os,sys
import nltk, re#, pprint
#import codecs
#from fuzzywuzzy import fuzz
import dedupe
import csv
from unidecode import unidecode

#map for name variations
name_map = {}

#list of main candidates
candidates = ["Woodrow Wilson","Charles E. Hughes","Allan L. Benson","Frank Hanly","Arthur E. Reimer"]

class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)
        
def preProcess(column):
    try : # python 2/3 string differences
        column = column.decode('utf8')
    except AttributeError:
        pass
#    column = unidecode(column)
    column = re.sub('  +', ' ', column)
    column = re.sub('\n', ' ', column)
    column = column.strip().strip('"').strip("'").lower().strip()
#If data is missing, indicate that by setting the value to None
    if not column:
        column = None
    return column

def performNameExtraction(text, p_entity_names):
    #Returns a list of what NLTK defines as persons after processing the text passed into it.
    try:
        for sent in nltk.sent_tokenize(text):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label') and chunk.label:
                    if chunk.label() == 'PERSON':
                        name_value = ' '.join(child[0] for child in chunk.leaves())
                        if name_value not in entity_names:
                            p_entity_names.append(name_value)
    except:
        print('Unexpected error:' + sys.exc_info()[0])

    return p_entity_names

def processFiles():


	return entity_names

def normalize_field(value):
	#make text lowercase and strip white space
	
	return value.lower().replace(" ", "")


if __name__ == '__main__':
    	#process every file in data folder
    entity_names = []
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', 'fixtures'))
#	pathjoin = os.path.join
    for fn in os.listdir(data_dir):   		
        if not fn.startswith('otherfiles'):
            f = open(os.path.join(data_dir,fn))
            reader = csv.DictReader(f)
            text = ''
            for row in reader:
                clean_row = [(k, preProcess(v[0])) for (k, v) in row.items()]
                l = len(clean_row)
                for i in range(0,l):
                    temp_row = clean_row[i]
                    l_j = len(temp_row)
                    for j in range(0,l_j):
                        text = text + temp_row[j]
            entity_names = []
            entity_names = performNameExtraction(text, entity_names)
#                entity_names = performNameExtraction(text)

    fields = [
    {'field' : 'First name', 'type': 'String', 'has missing' : True},
    {'field' : 'Last name', 'type': 'String', 'has missing' : False},
    ]
    deduper = dedupe.Dedupe(fields)
