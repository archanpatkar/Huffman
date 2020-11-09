import math
import pickle
import functools 
from collections import namedtuple

# Taken from
# https://stackoverflow.com/questions/21017698/converting-int-to-bytes-in-python-3
def int_to_bytes(number):
    return number.to_bytes(length=(8 + (number + (number < 0)).bit_length()) // 8, byteorder='big', signed=True)

def int_from_bytes(binary_data):
    return int.from_bytes(binary_data, byteorder='big', signed=True)
# --

Leaf = namedtuple("Leaf",["ch","prob"])
Node = namedtuple("Node",["prob","left","right"])

def letterFreq(data):
    return {ch: data.count(ch) for ch in data} 

def calcProb(data):
    n = sum(data.values())
    return {ch: data[ch]/n for ch in data} 

def calcEntropy(freq):
    return sum([-(freq[k] * math.log2(freq[k])) for k in freq])

def prefixMap(node,prefix='',dict={}):
    if isinstance(node,Node):
        prefixMap(node.left,prefix+'0',dict)
        return prefixMap(node.right,prefix+'1',dict)
    else:
        dict[node.ch] = prefix
        return dict    

def huffTree(weights):
    pq = [Leaf(ch,weights[ch]) for ch in weights]
    pq.sort(key=lambda l: l.prob)
    while len(pq) > 2:
        node = Node(pq[0].prob + pq[1].prob,pq[1],pq[0])
        pq = pq[2:]
        pq.append(node)
        pq.sort(key=lambda l: l.prob)
    return Node(pq[0].prob + pq[1].prob,pq[1],pq[0])

def convert(data,table):
    return functools.reduce(lambda acc,v: acc+table[v],data,'')

def revert(data,table):
    str = ""
    while len(data) != 0:
        for k in table:
            if data.startswith(table[k]):
                str += k
                data = data[len(table[k]):]
                break
    return str

ini = "A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED"
lf = letterFreq("A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED")
entropy = calcEntropy(calcProb(lf))
print(entropy)
tree = huffTree(lf)
print(tree)
table = prefixMap(tree)
print(table)
out = convert("A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED",table)
print(out)

f = open("test.hf","wb")
# print()
f.write(int_to_bytes(int(out,2)))

d = bin(int_from_bytes(int_to_bytes(int(out,2)))).replace("b","")
print(d)
deco = revert(d,table)
print("final")
print(deco)
print(deco == ini)

pickle.dump(table,open("test.map","wb"))