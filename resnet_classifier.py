import os
import time
import argparse
from keras.preprocessing import image as image_utils
from keras.applications.imagenet_utils import decode_predictions, preprocess_input
from keras.applications.resnet50 import ResNet50
import numpy as np
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def classify(path, model):
    image = image_utils.load_img(path, target_size=(224, 224))
    image = image_utils.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)

    preds = model.predict(image)

    id, label, confidence = decode_predictions(preds)[0][0]
    return id, label, confidence

def main():
    model = ResNet50(weights='imagenet')

    print('Illust;ImageNetID;Label;Confidence;Lapsed')

    fpath = os.path.join(os.path.dirname(__file__), 'illusts', '946272')
    for f in sorted(os.listdir(fpath)):
        start = time.time()
        path = os.path.join(fpath, f)
        id, label, confidence = classify(path, model)
        end = time.time()
        lapsed = end - start
        print('{};{};{};{};{}'.format(f, id, label, confidence, lapsed))

if __name__ == '__main__':
    main()
