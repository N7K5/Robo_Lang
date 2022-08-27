import numpy as np
import pickle



with open("data/1.np", "rb") as data_file:
    data= pickle.load(data_file)
    print("\n  => loaded data: ", data.shape, "\n")
    data_file.close()



import model_01
