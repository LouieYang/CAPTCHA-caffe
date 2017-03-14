import h5py, os
import caffe
import numpy as np
from PIL import Image

def data2h5py(tag, nyclass):
    with open(tag + '_list.txt', 'r' ) as T :
        lines = T.readlines()
    image_folder = "./" + tag + "_image/"
    X = np.zeros((len(lines), 1, 100, 100), dtype='f4' )
    y = np.zeros((len(lines), nyclass), dtype='f4')

    for i,l in enumerate(lines):
        sp = l.split(' ')
        sp.pop()
        img = np.array(Image.open(image_folder + sp[0]), dtype='f4')
        X[i][0] = img / 255.
        labelvec = np.array(sp[1:], dtype='f4')
        y[i] = labelvec
    with h5py.File(tag + '.h5','w') as H:
        H.create_dataset( 'data', data=X )
        H.create_dataset( 'label', data=y )
    with open(tag + '_h5.txt','w') as L:
        L.write( tag + '.h5' ) # list all h5 files you are going to use

if __name__ == "__main__":
    data2h5py("train", 6)
    # data2h5py("val", 6)
