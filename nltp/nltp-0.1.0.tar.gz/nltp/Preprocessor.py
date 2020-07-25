import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import time
from .Patterns import BadPatterns as bp
   
class Preprocessor():
    '''
    Class to a generic way of cleaning text for
    different NLP task. The process employed by
    this class are - remover of unwanted expresions
    like url, usernames (following the @ symbol),
    repetive words and numbers.
    
    This class also perfrom tokenization, and lemmatization. 
    '''
    def __init__(self,text,stop_words=set(stopwords.words('english')),
                 pattern=bp().Patterns()):

        #initilizing variables 
        #defualt patterns from the Patterns class will be used if no patterns are passed, same thing will happen for the stop words
        
        self.patterns = pattern
        self.stop_words = stop_words
        self.text = text


    def token(self,position=0):
        '''Function to tokenize the data set passed to it.
		
		Args: 
			Posotion: the index of the list to be returned. Set to 0 by default
		
		Returns: 
			list:  tokenized version of the data set passed
	
		'''
        
        #Tokenizing passed strings and returning their position. position 0 will be assumed for as default for the strings passed in the list
        
        tokenized_words = nltk.word_tokenize(self.text
        [position])
        return tokenized_words
    
    def text_cleaner(self):
        '''Function to completely preprocess text passed to it.
		
		Args: 
			None
		
		Returns: 
			list:  preprocessed version of the data set passed
	
		'''

        start_time = time.time()
        sentence_list = []
        texts = self.text
        wordLemm = WordNetLemmatizer()
        
        
        #looping through the patterns to remove bad expressions from text
        for pattern, replacement in zip(self.patterns.keys(),self.patterns.values()):
            #Removing bad expressions
            for text in texts:

                cleaned_text = re.sub(pattern,replacement,text)
                sentence_list.append(cleaned_text)

            #perfroming a swap to keep the texts to be cleaned updated
            texts = sentence_list 
            sentence_list = [] 
        #loops for perfroming lemmatization, and remover of stop words
        for text in texts:
            sentence = text.lower()
            sentence = sentence.split()
    
            sentence = [wordLemm.lemmatize(word) for word in sentence if word not in self.stop_words]
            sentence = ' '.join(sentence)
            sentence_list.append(sentence)
            sentence_list
            
        
        stop_time = time.time()
        #getting the total time for completing the exection of the cleaning process 
        execution_time = stop_time - start_time
        print(f'Cleaning Complete')
        print(f'Time Taken: {round(execution_time,3)} seconds')
        return sentence_list
             