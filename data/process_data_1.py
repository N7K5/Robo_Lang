import csv
from time import sleep
from tqdm import tqdm
import pickle
import re

op_file= open("1.processed.csv", "w")
unique_words_file= open("1.uniques.obj", "wb")


def process_line(line:str):
    line= line.lower()
    to_be_replaced= [
        ["'ll", " will"],
        ["n't", "n not"],
        ["'s", " is"],
        ["'re", " are"],
        ["'d", " would"],
        ["'m", " am"],
    ]

    for oldval, newval in to_be_replaced:
        line= line.replace(oldval, newval)
    

    to_be_removed= ["\"", "\'", "?", ".", "!", "@", "(", ")", "$", ",", ";", "/", ":"]

    for val in to_be_removed:
        line= line.replace(val, "")

    for space_count in range(2, 5):
        line= line.replace(" "*space_count, " ")

    return line


words_to_remove= list()
def print_stats(d):
    global words_to_remove
    print("  ---------------------")
    print("  Total unique words:", len(d))
    freq_d= dict()
    for word in d:
        freq= d[word]
        if freq not in freq_d: freq_d[freq]=[]
        freq_d[freq].append(word)
    
    freqs= list(freq_d.keys())
    freqs.sort()

    for x in freqs[:20]+freqs[:-6:-1]:
        print("  Words with frequency",x, " : ", len(freq_d[x]), "eg:", freq_d[x][:3])

    words_with_less_freq= list()
    for x in freqs[:20]:
        words_with_less_freq.extend(freq_d[x])
    f= open("1.less_freq.obj", "wb")
    pickle.dump(words_with_less_freq, f)
    f.close()
    print("   less frequent words count:", len(words_with_less_freq))
    print("   remaining:", len(d)-len(words_with_less_freq))
    words_to_remove= words_with_less_freq



unique_words= {}


with open("1.csv") as file:
    d= csv.reader(file, delimiter=",")
    for line_idx, line in tqdm(enumerate(d)):
        if line_idx==0: continue
        line= line[0]
        line= process_line(line)
        op_file.write("\n")

        words= line.split(" ")
        for w in words:
            if w not in unique_words:
                unique_words[w]=0
            unique_words[w]+=1
        op_file.write(line)

    print_stats(unique_words)

    pickle.dump(unique_words, unique_words_file, protocol=pickle.HIGHEST_PROTOCOL)
    unique_words_file.close()
    op_file.close()
    file.close()







#################################################################################




print(" Unique_words_len:", len(unique_words))
print(" removable_words_len:", len(words_to_remove))
words_to_keep= set(unique_words)-set(words_to_remove)
print(" Words_to_keep:", len(words_to_keep))

op_with_less_freq_word_removed= open("1.replaced.final.csv", "w")
LINE_MIN_LEN, LINE_MAX_LEN= 7, 15

new_uniques= set()
with open("1.processed.csv") as file:
    for line_no, line in tqdm(enumerate(file)):
        line= line.rstrip("\n")
        words= line.split(" ")
        if len(words)<LINE_MIN_LEN or len(words)>LINE_MAX_LEN:
            continue
        words= [w if w in words_to_keep else "INFQ_W" for w in words]
        for w in words:
            new_uniques.add(w)
        line= " ".join(words)
        for x in range(2,6):
            line= line.replace(" "*x, " ")
        op_with_less_freq_word_removed.write(line)
        op_with_less_freq_word_removed.write("\n")
    op_with_less_freq_word_removed.close()

print(" ->Remaining uniques:", len(new_uniques))
# print(new_uniques)