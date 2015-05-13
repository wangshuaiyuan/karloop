# coding=utf-8

__author__ = 'karl'


'''
use DES to encrypt the data
'''


from functools import partial


class DES(object):  
    """ 
    DES encrypt method
    interface: input_key(s, base=10), encode(s), decode(s) 
    """  
    __ip = [  
        58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,   
        62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,   
        57, 49, 41, 33, 25, 17,  9, 1, 59, 51, 43, 35, 27, 19, 11, 3,   
        61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7,   
    ]  
    __ip1 = [  
        40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,   
        38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,   
        36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,   
        34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41,  9, 49, 17, 57, 25,   
    ]  
    __e = [  
        32,  1,  2,  3,  4,  5,   
        4,  5,  6,  7,  8,  9,   
        8,  9, 10, 11, 12, 13,   
        12, 13, 14, 15, 16, 17,   
        16, 17, 18, 19, 20, 21,   
        20, 21, 22, 23, 24, 25,   
        24, 25, 26, 27, 28, 29,   
        28, 29, 30, 31, 32,  1,   
    ]  
    __p = [  
        16,  7, 20, 21, 29, 12, 28, 17,   
        1,  15, 23, 26,  5, 18, 31, 10,   
        2,   8, 24, 14, 32, 27,  3,  9,   
        19, 13, 30,  6, 22, 11,  4, 25,   
    ]  
    __s = [  
        [  
            0xe, 0x4, 0xd, 0x1, 0x2, 0xf, 0xb, 0x8, 0x3, 0xa, 0x6, 0xc, 0x5, 0x9, 0x0, 0x7,   
            0x0, 0xf, 0x7, 0x4, 0xe, 0x2, 0xd, 0x1, 0xa, 0x6, 0xc, 0xb, 0x9, 0x5, 0x3, 0x8,   
            0x4, 0x1, 0xe, 0x8, 0xd, 0x6, 0x2, 0xb, 0xf, 0xc, 0x9, 0x7, 0x3, 0xa, 0x5, 0x0,   
            0xf, 0xc, 0x8, 0x2, 0x4, 0x9, 0x1, 0x7, 0x5, 0xb, 0x3, 0xe, 0xa, 0x0, 0x6, 0xd,   
        ],  
        [  
            0xf, 0x1, 0x8, 0xe, 0x6, 0xb, 0x3, 0x4, 0x9, 0x7, 0x2, 0xd, 0xc, 0x0, 0x5, 0xa,   
            0x3, 0xd, 0x4, 0x7, 0xf, 0x2, 0x8, 0xe, 0xc, 0x0, 0x1, 0xa, 0x6, 0x9, 0xb, 0x5,   
            0x0, 0xe, 0x7, 0xb, 0xa, 0x4, 0xd, 0x1, 0x5, 0x8, 0xc, 0x6, 0x9, 0x3, 0x2, 0xf,   
            0xd, 0x8, 0xa, 0x1, 0x3, 0xf, 0x4, 0x2, 0xb, 0x6, 0x7, 0xc, 0x0, 0x5, 0xe, 0x9,   
        ],  
        [  
            0xa, 0x0, 0x9, 0xe, 0x6, 0x3, 0xf, 0x5, 0x1, 0xd, 0xc, 0x7, 0xb, 0x4, 0x2, 0x8,   
            0xd, 0x7, 0x0, 0x9, 0x3, 0x4, 0x6, 0xa, 0x2, 0x8, 0x5, 0xe, 0xc, 0xb, 0xf, 0x1,   
            0xd, 0x6, 0x4, 0x9, 0x8, 0xf, 0x3, 0x0, 0xb, 0x1, 0x2, 0xc, 0x5, 0xa, 0xe, 0x7,   
            0x1, 0xa, 0xd, 0x0, 0x6, 0x9, 0x8, 0x7, 0x4, 0xf, 0xe, 0x3, 0xb, 0x5, 0x2, 0xc,   
        ],  
        [  
            0x7, 0xd, 0xe, 0x3, 0x0, 0x6, 0x9, 0xa, 0x1, 0x2, 0x8, 0x5, 0xb, 0xc, 0x4, 0xf,   
            0xd, 0x8, 0xb, 0x5, 0x6, 0xf, 0x0, 0x3, 0x4, 0x7, 0x2, 0xc, 0x1, 0xa, 0xe, 0x9,   
            0xa, 0x6, 0x9, 0x0, 0xc, 0xb, 0x7, 0xd, 0xf, 0x1, 0x3, 0xe, 0x5, 0x2, 0x8, 0x4,   
            0x3, 0xf, 0x0, 0x6, 0xa, 0x1, 0xd, 0x8, 0x9, 0x4, 0x5, 0xb, 0xc, 0x7, 0x2, 0xe,   
        ],  
        [  
            0x2, 0xc, 0x4, 0x1, 0x7, 0xa, 0xb, 0x6, 0x8, 0x5, 0x3, 0xf, 0xd, 0x0, 0xe, 0x9,   
            0xe, 0xb, 0x2, 0xc, 0x4, 0x7, 0xd, 0x1, 0x5, 0x0, 0xf, 0xa, 0x3, 0x9, 0x8, 0x6,   
            0x4, 0x2, 0x1, 0xb, 0xa, 0xd, 0x7, 0x8, 0xf, 0x9, 0xc, 0x5, 0x6, 0x3, 0x0, 0xe,   
            0xb, 0x8, 0xc, 0x7, 0x1, 0xe, 0x2, 0xd, 0x6, 0xf, 0x0, 0x9, 0xa, 0x4, 0x5, 0x3,   
        ],  
        [  
            0xc, 0x1, 0xa, 0xf, 0x9, 0x2, 0x6, 0x8, 0x0, 0xd, 0x3, 0x4, 0xe, 0x7, 0x5, 0xb,   
            0xa, 0xf, 0x4, 0x2, 0x7, 0xc, 0x9, 0x5, 0x6, 0x1, 0xd, 0xe, 0x0, 0xb, 0x3, 0x8,   
            0x9, 0xe, 0xf, 0x5, 0x2, 0x8, 0xc, 0x3, 0x7, 0x0, 0x4, 0xa, 0x1, 0xd, 0xb, 0x6,   
            0x4, 0x3, 0x2, 0xc, 0x9, 0x5, 0xf, 0xa, 0xb, 0xe, 0x1, 0x7, 0x6, 0x0, 0x8, 0xd,   
        ],  
        [  
            0x4, 0xb, 0x2, 0xe, 0xf, 0x0, 0x8, 0xd, 0x3, 0xc, 0x9, 0x7, 0x5, 0xa, 0x6, 0x1,   
            0xd, 0x0, 0xb, 0x7, 0x4, 0x9, 0x1, 0xa, 0xe, 0x3, 0x5, 0xc, 0x2, 0xf, 0x8, 0x6,   
            0x1, 0x4, 0xb, 0xd, 0xc, 0x3, 0x7, 0xe, 0xa, 0xf, 0x6, 0x8, 0x0, 0x5, 0x9, 0x2,   
            0x6, 0xb, 0xd, 0x8, 0x1, 0x4, 0xa, 0x7, 0x9, 0x5, 0x0, 0xf, 0xe, 0x2, 0x3, 0xc,   
        ],  
        [  
            0xd, 0x2, 0x8, 0x4, 0x6, 0xf, 0xb, 0x1, 0xa, 0x9, 0x3, 0xe, 0x5, 0x0, 0xc, 0x7,   
            0x1, 0xf, 0xd, 0x8, 0xa, 0x3, 0x7, 0x4, 0xc, 0x5, 0x6, 0xb, 0x0, 0xe, 0x9, 0x2,   
            0x7, 0xb, 0x4, 0x1, 0x9, 0xc, 0xe, 0x2, 0x0, 0x6, 0xa, 0xd, 0xf, 0x3, 0x5, 0x8,   
            0x2, 0x1, 0xe, 0x7, 0x4, 0xa, 0x8, 0xd, 0xf, 0xc, 0x9, 0x0, 0x3, 0x5, 0x6, 0xb,   
        ],  
    ]  
    __k1 = [  
        57, 49, 41, 33, 25, 17,  9,   
        1,  58, 50, 42, 34, 26, 18,   
        10,  2, 59, 51, 43, 35, 27,   
        19, 11,  3, 60, 52, 44, 36,   
        63, 55, 47, 39, 31, 23, 15,   
        7,  62, 54, 46, 38, 30, 22,   
        14,  6, 61, 53, 45, 37, 29,   
        21, 13,  5, 28, 20, 12,  4,   
    ]  
    __k2 = [  
        14, 17, 11, 24,  1,  5,  3, 28,   
        15,  6, 21, 10, 23, 19, 12,  4,   
        26,  8, 16,  7, 27, 20, 13,  2,   
        41, 52, 31, 37, 47, 55, 30, 40,   
        51, 45, 33, 48, 44, 49, 39, 56,   
        34, 53, 46, 42, 50, 36, 29, 32,   
    ]  
    __k0 = [  
        1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1,   
    ]  
    __hex_bin = {  
        '0': '0000', '1': '0001', '2': '0010', '3': '0011',   
        '4': '0100', '5': '0101', '6': '0110', '7': '0111',   
        '8': '1000', '9': '1001', 'a': '1010', 'b': '1011',   
        'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111',   
        ' ': '0000'  
    }  
  
    __re = lambda t, s: ''.join(s[i-1] for i in t)  
  
    __IP = partial(__re, __ip)  
    __IP1 = partial(__re, __ip1)  
    __E = partial(__re, __e)  
    __P = partial(__re, __p)  
    __K1 = partial(__re, __k1)  
    __K2 = partial(__re, __k2)  
  
    __B = partial(lambda hex_bin, s: ''.join(hex_bin[w] for w in ''.join('%2x' % ord(w) for w in s)), __hex_bin)
    __DB = partial(lambda s: ''.join(chr(int(s[i:i+8], 2)) for i in range(0, len(s), 8)))
    __S = partial(lambda hex_bin, __s, s: ''.join(hex_bin['%x' % __s[i][int(s[i*6]+s[i*6+5], 2)*16 + int(s[i*6+1:i*6+5], 2)]] for i in range(8)), __hex_bin, __s)
    __F = partial(lambda s, k: ''.join('0' if s[i]==k[i] else '1' for i in range(len(s))))
    __K0 = partial(lambda k0, K2, k: map(K2, (k[k0[i]:28]+k[0:k0[i]] + k[k0[i]+28:56]+k[28:k0[i]+28] for i in range(16))), __k0, __K2)
    __K = partial(lambda K1, K0, k: K0(K1(k)), __K1, __K0)
  
    def __init__(self):  
        pass  
  
    def input_key(self, key, base=10):  
        if base == 2:  
            pass  
        elif base == 16:  
            key = ''.join(self.__class__.__hex_bin[w] for w in key)  
        else:  
            key = self.__class__.__B(key)  
        self.__k = self.__class__.__K(key)  
  
    def __code(self, s, k):  
        s = self.__IP(s)  
        l, r = s[0:32], s[32:64]  
        for i in range(16):  
            r_t = r  
            r = self.__E(r)  
            r = self.__F(r, k[i])  
            r = self.__S(r)  
            r = self.__P(r)  
            r = self.__F(r, l)  
            l = r_t  
        return self.__class__.__IP1(r+l)  
  
    def encode(self, s):  
        a = ''  
        s += ' ' * ((8-len(s) % 8) % 8)
        for i in range(0, len(s), 8):  
            before = self.__class__.__B(s[i:i+8])  
            after = self.__code(before, self.__k)  
            a += '%16x' % int(after, 2)  
        return ''.join(w if w != ' ' else '0' for w in a)
  
    def decode(self, s):  
        a = ''  
        s.lower()  
        for i in range(0, len(s), 16):  
            before = ''.join(self.__class__.__hex_bin[s[j]] for j in range(i, i+16))  
            after = self.__code(before, self.__k[::-1])  
            a += self.__class__.__DB(after)  
        return a.rstrip().decode('utf-8') 
  
  
if __name__ == '__main__':  
    d = DES()  
    d.input_key('123456789')  
    s = '再来一段中文'
    a = d.encode(s)  
    print a

    b = d.decode(a)
    print b  