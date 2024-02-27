from core.rrdbnet import RRDBNet
import numpy as np
from functools import lru_cache
import tensorflow as tf


@lru_cache(maxsize=None)
def load_model(path):
    model = RRDBNet(blockNum=10)
    model.load_weights(path)
    return model

def process(path):
    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    return image

def lp_enhancement(img):
    model = load_model('../models/srgan/rrdb')
    img_array = process(img)
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    prediction = np.squeeze(np.clip(prediction, a_min=0, a_max=1))
    return prediction