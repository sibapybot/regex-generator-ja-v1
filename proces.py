
import MeCab
from typing import Optional, List
from dataclass import WordDescription, DecomposedString


tagger = MeCab.Tagger("-Ochasen")

def disassembly_text(text:str) -> DecomposedString:
    """
    textをDecomposedStringに変換する関数。
    """
    global tagger
    node = tagger.parseToNode(text)

    nodet,s=[],0
    while node:
        nodes = WordDescription()
        nodes.word = node.surface
        nodes.description = node.feature.split(",")
        nodes.string_position = s
        nodes.word_position = sum([len(word.word) for word in nodet],len(nodes.word))
        nodet.append(nodes)

        node = node.next
        s+=1
    nodet = list(nodet)[1:-1]

    disassembly_text = DecomposedString()
    disassembly_text.str_len = len(text)
    disassembly_text.word_quantity = nodet
    disassembly_text.word_len = len(nodet)
    disassembly_text.string = text
    return disassembly_text

def max_word(two_node):
    return max([two_node[0].word_len,two_node[1].word_len])

def pading(node,max):
    #リストを同じ長さに揃える
    return node + [WordDescription()]*(max-len(node))

def left_sift(arr:List[WordDescription],n:int):
    #右ずらしをしていく
    return arr[n:] + arr[:n]

def all_same_element(x):
    return x[1:] == x[:-1]

def remove_spaces(s):
  return s.replace(" ", "")