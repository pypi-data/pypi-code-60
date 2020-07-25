from tccseg import cc



class Core(object):
    def __init__(self, cclib='original'):
        self.ccp = cc.gen_cc(cclib)


    def generate(self, s):
        p = 0
        while p < len(s):
            m = self.ccp.match(s[p:])
            if m:
                n = m.span()[1]
            else:
                n = 1
            yield s[p:p + n]
            p += n


    def segment(self, s):
        res = self.generate(s)
        return list(res)
