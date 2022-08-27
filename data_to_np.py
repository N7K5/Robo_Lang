from tqdm import tqdm
import numpy as np
import pickle


data_file= "data/1.replaced.final.csv"


def process_and_get_data_components(data_file):
    extracted_lines= list()
    extracted_words= set()
    with open(data_file) as file:
        for line_idx, line in tqdm(enumerate(file)):
            line= line.rstrip("\n")
            if line_idx>= 1200 : break
            extracted_lines.append(line)
            words= line.split(" ")
            if len(words)<2: continue
            for w in words:
                if len(w)>0:
                    extracted_words.add(w)
        file.close()
    return extracted_lines, extracted_words


def make_data_onehot(data_text, uniques, data_max_len):
    uniques= list(set(uniques))
    onehot_map= dict()

    for idx, u in enumerate(uniques):
        hot= np.zeros(len(uniques))
        hot[idx]=1
        onehot_map.update({
            u: hot,
        })
    
    res= list()

    for d in tqdm(data_text):
        words= d.split(" ")
        arr= list()
        for w in words:
            arr.append(onehot_map.get(w))
        while len(arr)<data_max_len:
            arr.append(np.zeros(len(uniques)))
        res.append(arr)

    res= np.array(res)
    return res





lines, words= process_and_get_data_components(data_file)
max_d_len= 0
for l in lines:
    max_d_len= max(max_d_len, len(l.split(" ")))
np_data= make_data_onehot(lines, words, max_d_len)
print("\n => got data(lines, w/line, w_size):", np_data.shape, "\n")

pkl= open("data/1.np", "wb")
pickle.dump(np_data, pkl)
pkl.close()
