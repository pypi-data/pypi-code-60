class BadPatterns():
    
    def Patterns(self):
        '''
        This class contains popluarly used Regular Expressions.
        Patterns Removed are Non alphabets, Links, Repetive Sequence,
        and Symbols.

        Patterns to be removed are in a dict form containing:
        PATTERN and REPLACEMENT. i.e {PATTERN: REPLACEMENT}
        '''
        
        #defining unwanted patterns 
        alpha_pattern = r'[^a-zA-Z]'
        url_pattern = r'((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)'
        user_pattern = r'@[^\s]+'
        sequence_pattern = r'(.)\1\1+'
        mul_pattern = r'\1\1'
        slash_pattern = r'[/(){}\[\]\|@!,;#]'
        
        patterns = {alpha_pattern:' ',url_pattern:'URL',user_pattern:' User',
                   sequence_pattern:mul_pattern,slash_pattern:' '}
        
        return patterns
 