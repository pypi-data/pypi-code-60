import re



'''
    c: consonant
    t: tone
    cc_original : https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/tokenize/tcc.py
    cc_cf: n/a
'''

# constants

CONSONANT_SYMBOL = 'c'
PIPE_SYMBOL = '|'
TONE_SYMBOL = 't'
CONSONANTS = '[ก-ฮ]'
TONES = '[่-๋]?'


# Character clusters

cc_original = '''
    เc็c
    เcctาะ
    เccีtยะ
    เccีtย(?=[เ-ไก-ฮ]|$)
    เccอะ
    เcc็c
    เcิc์c
    เcิtc
    เcีtยะ?
    เcืtอะ?
    เc[ิีุู]tย(?=[เ-ไก-ฮ]|$)
    เctา?ะ?
    cัtวะ
    c[ัื]tc[ุิะ]?
    c[ิุู]์
    c[ะ-ู]t
    c็
    ct[ะาำ]?
    แc็c
    แcc์
    แctะ
    แcc็c
    แccc์
    โctะ
    [เ-ไ]ct
    ๆ
    ฯลฯ
    ฯ
'''

cfcc = None


# Character Cluster library

cclib = {
    'original': cc_original,
    'cfcc': cfcc
}



def gen_cc(k):
    if k == 'original':
        ccp = gen_cc_original()

    elif k == 'cf':
        ccp = gen_cc_cfcc()

    return ccp


def gen_cc_original():
    cc_pattern = cclib['original'].replace(CONSONANT_SYMBOL, CONSONANTS).replace(TONE_SYMBOL, TONES).split()
    ccp = re.compile(PIPE_SYMBOL.join(cc_pattern))
    return ccp


def gen_cc_cfcc():
    pass
