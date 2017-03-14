import string
import os
import random
import numpy as np
import scipy.io as sio
import argparse
import json
from captcha.image import ImageCaptcha
from operator import itemgetter
image = ImageCaptcha(width=100, height=100, fonts=['./generator/YH.ttf', './generator/YH.ttf'])

def generate_text(length, number):
    res = []
    while len(res) < number:
        captcha = ''
        for index in range(length):
            captcha += random.choice(candidate)
        if captcha not in res:
            res.append(captcha)
    return res

def get_label(captcha):
    ''' Returen shape(6,)'''
    label = []
    for ch in captcha:
        theta = theta_func[ch]
        label.append(theta)
    return label

def gen(tag, CAPTCHA_LEN, nsamples):

    text = generate_text(CAPTCHA_LEN, nsamples)
    label_dict = {}
    folder_prefix = './' + tag + '_image/'

    if not os.path.exists(folder_prefix):
        os.mkdir(folder_prefix)

    for i in range(len(text)):
        captcha_text = text[i]
        data = image.generate(captcha_text)

        filename = str(i) + '.png'
        label_dict[filename] = get_label(captcha_text)
        image.write(captcha_text, './' + tag + '_image/' + filename)

    with open(tag + "_label.json", "w") as f:
        json.dump(label_dict, f)

    print "Done generating " + str(nsamples) + " " + tag + " dataset ..."

def data2h5py(tag, nyclass):
    with open(tag + '_list.txt', 'r' ) as T :
        lines = T.readlines()
    image_folder = "./" + tag + "_image/"
    X = np.zeros((len(lines), 1, 100, 100), dtype='f4' )
    y = np.zeros((len(lines), nyclass), dtype='f4')

    for i,l in enumerate(lines):
        sp = l.split(' ')
        sp.pop()
        im = Image.open(image_folder + sp[0]).convert("L")
        img = np.array(im.resize(100, 100), dtype='f4')
        X[i][0] = img / 255.
        labelvec = np.array(sp[1:], dtype='f4')
        y[i] = labelvec
    with h5py.File(tag + '.h5','w') as H:
        H.create_dataset( 'data', data=X )
        H.create_dataset( 'label', data=y )
    with open(tag + '_h5.txt','w') as L:
        L.write( tag + '.h5' ) # list all h5 files you are going to use

    print "Done generating " + tag + ".h5 ..."

def json2txt(s, out):
    f = open(s)
    json_content = json.load(f)
    l = list(json_content.iteritems())
    f.close()
    with open(out,'w+') as L:
        for t in l:
            L.write(t[0] + ' ')
            for i in t[1]:
                L.write(str(i) + ' ')
            L.write('\n')
    print "Done generating " + out + " ..."

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--captcha_len', default =6, type=int, help='the size of captcha numbers')
    parser.add_argument('--ntrain', default=200000, type=int, help='the size of training dataset')
    parser.add_argument('--nval', default=1000, type=int, help='the size of evaluation dataset')
    parser.add_argument('--charnum', default=True, type=bool, help='1=character plus number, 0=only number')

    args = parser.parse_args()
    params = vars(args)
    print 'parsed input parameters:'
    print json.dumps(params, indent = 2)

    l_letter = [a for a in string.ascii_letters]
    l_digit = [d for d in string.digits]
    if params['charnum']:
        candidate = l_digit + l_letter
    else:
        candidate = l_digit

    theta_func = dict(zip(candidate, range(len(candidate))))
    gen('train', params['captcha_len'], params['ntrain'])
    gen('val', params['captcha_len'], params['nval'])

    json2txt("./train_label.json", 'train_list.txt')
    json2txt("./val_label.json", 'val_list.txt')
    data2h5py("train", params['captcha_len'])
    data2h5py("val", params['captcha_len'])
