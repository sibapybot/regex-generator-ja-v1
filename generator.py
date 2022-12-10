from typing import Optional, List
from proces import (disassembly_text, 
                    max_word, 
                    pading, 
                    left_sift, 
                    all_same_element,
                    remove_spaces
                    )
from dataclass import DecomposedString, WordDescription, AllText ,SaveDecomposedString
import statistics
import itertools
import re


def run(texts:List):
    all_pattern:str = "" 
    all_pattern_list:List[SaveDecomposedString] = []
    most_meny_word_pattern_list:list = []
    pattern_firsts:List[SaveDecomposedString] = []
    text_data:List[DecomposedString] = []
    
    for text in texts:
        text_data.append(disassembly_text(text=text))
    
    all_data = AllText()
    all_data.max_len = max(map(len, texts))
    all_data.min_len = min(map(len, texts))
    word_lens = sorted([teda.word_len for teda in text_data])
    all_data.max_len = word_lens[-1]
    all_data.min_len = word_lens[0]
    all_data.str_several = len(texts)

    for two_node in itertools.combinations(text_data,2):

        maxword = max_word(two_node=two_node)
        save_patten_a:list[WordDescription] = []
        save_patten_b:list[WordDescription] = []
        
        for z in range(maxword):
            b:WordDescription = pading(two_node[0].word_quantity,maxword)[z]
            #b:WordDescription = pading(two_node[1].word_quantity,maxword)
            
            for i in range(maxword):
                a = left_sift(arr=pading(two_node[1].word_quantity,maxword),n=i)[z]
                #a = leftwords[z]
                duplicate_check = a not in save_patten_a and b not in save_patten_b        
                if a.word == b.word and a.description == b.description and duplicate_check:
                    save_patten_a.append(a)
                    save_patten_b.append(b)

        def key_out(x:WordDescription):
            return x.string_position
        save_patten_a.sort(key=key_out)
        save_patten_b.sort(key=key_out)
        #for spa,spb in zip(save_patten_a,save_patten_b):
        #print([i.word for i in save_patten_a])
        #print([i.word for i in save_patten_b])

        def division_WordDescription_list(save_patten_a:List[WordDescription],save_patten_b:List[WordDescription]):
            a_po = 0
            b_po = 0
            out_save_patten_a = [[]]
            out_save_patten_b = [[]]
            for i in range(len(save_patten_a)):
                #print(a_po+1 == save_patten_a[i].string_position and b_po+1 == save_patten_b[i].string_position)
                #print(a_po+1 , save_patten_a[i].string_position , b_po+1 , save_patten_b[i].string_position)
                if a_po+1 == save_patten_a[i].string_position and b_po+1 == save_patten_b[i].string_position:
                    out_save_patten_a[-1].append(save_patten_a[i])
                    out_save_patten_b[-1].append(save_patten_b[i])
                    a_po += 1
                    b_po += 1
                else:
                    out_save_patten_a.append([save_patten_a[i]])
                    out_save_patten_b.append([save_patten_b[i]])
                    a_po = save_patten_a[i].string_position
                    b_po = save_patten_b[i].string_position

            return out_save_patten_a,out_save_patten_b
        
        save_patten_a,save_patten_b = division_WordDescription_list(save_patten_a,save_patten_b)
        #print(save_patten_a)
        decstr:List[DecomposedString] = []
        i = 0
        for spa,spb in zip(save_patten_a,save_patten_b):
            spa:List[WordDescription]
            word = [i.word for i in spa]
            word_position = [i.word_position for i in spa]
            string_position = [i.string_position for i in spa]
            word_end =[p+len(w)-1 for w,p in zip(word,word_position)]
            if i > 0:
                print(i)
                decstr.append(DecomposedString(
                string="".join(word),
                str_len=len("".join(word)),
                word_len=len(word),
                str_end=max(word_end) - decstr[i].str_end,
                str_top=min(word_position) - decstr[i].str_top
                ))
                i+=1

            decstr.append(DecomposedString(
                string="".join(word),
                str_len=len("".join(word)),
                word_len=len(word),
                str_end=max(word_end),
                str_top=min(word_position)
            ))
            
        pattern_firsts.append(decstr)

    pattern_firsts_len_max = max([len(pattern_firsts_len) for pattern_firsts_len in pattern_firsts])
    for i in range(pattern_firsts_len_max):
        
        most_meny_word = statistics.mode([pattern_firsts[z][i].string for z in range(len(pattern_firsts))])
        def check(x):
            if pattern_firsts[x][i].string == most_meny_word:
                return pattern_firsts[x][i] 
        most_meny_word_pattern_list.append([check(z) for z in range(len(pattern_firsts))])



    for most_meny_word_pattern in most_meny_word_pattern_list:

        word_pattern_list = SaveDecomposedString()

        word_pattern_list.string = most_meny_word_pattern[0].string

        word_pattern_str_top=[word_pattern.str_top for word_pattern in most_meny_word_pattern]
        if all_same_element(word_pattern_str_top):
            word_pattern_list.str_top = word_pattern_str_top[0]

        word_pattern_str_end=[word_pattern.str_end for word_pattern in most_meny_word_pattern]
        if all_same_element(word_pattern_str_end):
            word_pattern_list.str_end = word_pattern_str_end[0]
        all_pattern_list.append(word_pattern_list)
    
    all_pattern += "^"

    for pattern in all_pattern_list:

        if pattern.str_top == 1:
            all_pattern += pattern.string

        elif pattern.str_top is None:
            all_pattern += f".*"
            all_pattern += pattern.string
        
        elif pattern.str_top > 1:
            
            all_pattern += f".{{{pattern.str_top-1}}}"
            all_pattern += pattern.string

    all_pattern += ".*$"
    
    return all_pattern
        
    
def is_true(text,pattern):

    if re.match(pattern,remove_spaces(text)):
        return True
    else:
        return False
    
        


            


if __name__ == "__main__":
    texts = ["a testだあああああああ！！！asfdaa testだあああああああ！！！ ","a testだあああああああ！！！barbhah ethbe  testだあああああああ！！！","a testだあああああああ！！！agfnl testだあああああああ！！！"]
    pattern = run(texts=texts)
    print(pattern)
    print(is_true("a testだあああああああ！！！asfdaasdaedea testだあああああああ！！！ ",pattern=pattern))
