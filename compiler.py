#!/usr/bin/env python3
import pandas as pd
from sly import Lexer,Parser

class MyLexer(Lexer):
    tokens = { INPUT,OUTPUT,SELECT,PROJECT,AVGGROUP,AVG,SUMGROUP,SORT,JOIN,MOVAVG,MOVSUM,CONCAT,BTREE,HASH,COMP,OR,AND,NAME,NUMBER,DEFINE }
    literals = {'(',')', ','} 
    ignore = ' \t'
   
    # Tokens
    INPUT = r'inputfromfile'
    OUTPUT = r'outputtofile'
    SELECT = r'select'
    PROJECT = r'project'
    AVGGROUP = r'avggroup'
    AVG = r'avg'
    SUMGROUP = r'sumgroup'
    SORT = r'sort'
    JOIN = r'join'
    MOVAVG = r'movavg'
    MOVSUM = r'movsum'
    CONCAT = r'concat'
    BTREE = r'Btree'
    HASH = r'Hash'
:x
    OR = r'or'
    AND = r'and'
    NAME = r'[\']?[a-zA-Z_][a-zA-Z0-9_]*[\']?'
    NUMBER = r'\d+'
    DEFINE = r':='
    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class MyParser(Parser):
    ''' 
    @_('statements statements')
    def statements(self, p):
        return p.statement + [ p.statememts ]
    '''
    tokens = MyLexer.tokens

    def __init__(self):
        self.names = { }
    
    @_('NAME DEFINE expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr
    
    @_('expr')
    def statement(self, p):
        if p.expr in self.names:
            print(self.names[p.expr]) 
        else:
            print(p.expr)

    @_('HASH "(" NAME "," expr ")"')
    @_('BTREE "(" NAME "," expr ")"')
    def statement(self, p):
        self.names[p.NAME] = self.names[p.NAME].set_index(p.expr)
        self.names[p.NAME] = self.names[p.NAME].sort_index() 

    @_('OUTPUT "(" NAME "," NAME ")"')
    def statement(self, p):
        return self.names[p.NAME0].to_csv(p.NAME1,sep='|',index=False)

    @_('INPUT "(" NAME ")"')
    def expr(self, p):
        return pd.read_csv(p.NAME,sep='|')

    @_('SELECT "(" NAME "," expr ")"')
    def expr(self, p):
        return self.names[p.NAME].query(p.expr)

    @_('JOIN "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        df0 = self.names[p.NAME0].add_prefix(p.NAME0+"_")
        df1 = self.names[p.NAME1].add_prefix(p.NAME1+"_")
        return pd.merge(df0.assign(key=0), df1.assign(key=0), on='key').drop('key', axis=1).query(p.expr)

    @_('PROJECT "(" NAME "," expr ")"')
    def expr(self, p):
        return pd.DataFrame(self.names[p.NAME],columns=p.expr)

    @_('AVG "(" NAME "," NAME ")"')
    def expr(self, p):
        return self.names[p.NAME0][p.NAME1].mean()

    @_('SUMGROUP "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        return self.names[p.NAME0].groupby(p.expr)[p.NAME1].sum()
    
    @_('AVGGROUP "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        return self.names[p.NAME0].groupby(p.expr)[p.NAME1].mean()
    
    @_('SORT "(" NAME "," expr ")"')
    def expr(self, p):
        return self.names[p.NAME].sort_values(by=p.expr)

    @_('MOVAVG "(" NAME "," NAME "," NUMBER ")"')
    def expr(self, p):
        return self.names[p.NAME0][p.NAME1].rolling(int(p.NUMBER),min_periods=1).mean()
        # df[col].rolling(num,min_periods=1).mean() 
    
    @_('MOVSUM "(" NAME "," NAME "," NUMBER ")"')
    def expr(self, p):
        return self.names[p.NAME0][p.NAME1].rolling(int(p.NUMBER),min_periods=1).sum()

    @_('CONCAT "(" NAME "," NAME ")"')
    def expr(self, p):
        return pd.concat([self.names[p.NAME0],self.names[p.NAME1]])

    @_('"(" expr ")" OR "(" expr ")"')
    def expr(self, p):
        return p.expr0+" or "+p.expr1;

    @_('"(" expr ")" AND "(" expr ")"')
    def expr(self, p):
        return p.expr0+" and "+p.expr1;

    @_('NAME COMP NAME')
    def expr(self, p):
        if p.COMP == "=":
            return p.NAME0+"=="+p.NAME1
        else:
            return p.NAME0+p.COMP+p.NAME1
    
    @_('NAME COMP NUMBER')
    def expr(self, p):
        if p.COMP == "=":
            return p.NAME+"=="+p.NUMBER
        else:
            return p.NAME+p.COMP+p.NUMBER
     
    @_('NAME "," expr')
    def expr(self, p):
        l = [p.NAME]
        if type(p.expr) == list:
            l.extend(p.expr)  
        else:
            l.append(p.expr)
        return l;

    @_('NAME')
    def expr(self, p):
        return p.NAME

if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    while True:
        try:
            text = input('pd >> ')
        except EOFError:
            break
        if text:
            #for tok in lexer.tokenize(text):
            #    print(tok)
            parser.parse(lexer.tokenize(text)) 

        
