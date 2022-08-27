 
import keras
import tensorflow as tf
from keras import layers
import numpy as np

from features import IMG_SIZE, FEATURE_COUNT, FEATURE_POINTS
from features import data_to_image, print_image


# print_image(data_to_image([0, 0, 0.6, 0, 0, 0.8, 0.8, 0.3, 0.7, 0.8]))

class Brain:

    def __init__(self):
        self.features_per_symbol= FEATURE_COUNT
        self.symbols_per_line= 17



    def build_model(self, word_count, w_vec_size):

        ip= layers.Input(shape=(word_count, w_vec_size))
        ip_rnn= layers.LSTM(units= 512, activation="tanh")(ip)
        enc_d= layers.Dense(units=self.symbols_per_line * 16, activation="tanh")(ip_rnn)
        enc_d= layers.Reshape((self.symbols_per_line, -1))(enc_d)
        enc_op= layers.LSTM(units=self.features_per_symbol, return_sequences=True, activation="tanh")(enc_d)

        def to_img(d):
            res= list()
            for x1 in d:
                res.append(list())
                for x2 in x1:
                    img= data_to_image(x2)
                res[-1].append(img)
            return tf.convert_to_tensor(res)

        def to_img(d):
            res= np.zeros(len(d)*len(d[0])*IMG_SIZE[0]*IMG_SIZE[1]).reshape(-1, len(d[0]), IMG_SIZE[0], IMG_SIZE[1])
            for x1 in range(len(d)):
                for x2 in range(len(d[x1])):
                    data_to_image(d[x1][x2], res[x1][x2])
            return tf.convert_to_tensor(res)
        
        enc_img= layers.Lambda(to_img, output_shape=(self.symbols_per_line, IMG_SIZE[0], IMG_SIZE[1]), dynamic=True)(enc_op)


        img_tp= keras.backend.permute_dimensions(enc_img, (0,2,3,1))
        conv1= layers.Conv2D(32, (3,3), activation="tanh", padding="same")(img_tp)
        pool1= layers.MaxPooling2D((2,2))(conv1)
        conv2= layers.Conv2D(64, (3,3), activation="tanh", strides=(2,2), padding="same")(pool1)
        flat= layers.Flatten()(conv2)
        dec_d= layers.Dense(units=256, activation="tanh")(flat)
        dec_d= layers.Dense(units=word_count*32, activation="tanh")(dec_d)
        dec_d= layers.Reshape((word_count, -1))(dec_d)
        dec_op= layers.LSTM(units= w_vec_size, activation="softmax", return_sequences=True)(dec_d)



        self.model_enc= keras.models.Model(ip, enc_op)




        self.model= keras.models.Model(ip, dec_op)
        self.model.compile(loss="mse", optimizer="adam")
        self.model.summary()
        







if __name__=="__main__":

    import pickle
    with open("data/1.np", "rb") as data_file:
        data= pickle.load(data_file)
        print("\n  => loaded data: ", data.shape, "\n")
        data_file.close()
    sample_count, word_count, vec_size= data.shape

    b= Brain()
    b.build_model(word_count, vec_size)

    # b.model.predict(data)
    b.model.fit(data, data)

