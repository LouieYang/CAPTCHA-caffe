
# coding: utf-8

# In[77]:

import string
import random
import numpy as np
import scipy.io as sio
import json
from io import BytesIO
from captcha.image import ImageCaptcha
from operator import itemgetter
image = ImageCaptcha(width=100, height=100, fonts=['./YH.ttf', './YH.ttf'])



# In[30]:

l_letter = [a for a in string.ascii_letters]
l_digit = [d for d in string.digits]
candidate = l_digit + l_letter
theta_func = dict(zip(candidate, range(62)))

# In[21]:

def generate_text(length, number):
    res = []
    while len(res) < number:
        captcha = ''
        for index in range(length):
            captcha += random.choice(candidate)
        if captcha in res:
            continue
        else:
            res.append(captcha)
    print(res)
    return res


# In[54]:

def get_label(captcha):
    ''' Returen shape(64,)'''
    label = []
    for i in range(len(captcha)):
        ch = captcha[i]
        theta = theta_func[ch]
        cell = np.zeros(62)
        cell[theta] = 1
        label.extend(cell.tolist())
    return label


# In[65]:

def get_label_int(captcha):
    ''' Returen shape(6,)'''
    label = []
    for i in range(len(captcha)):
        ch = captcha[i]
        theta = theta_func[ch]
        label.append(theta)
    return label


# In[84]:

text = generate_text(6, 200000)
label_dict = {}
for i in range(len(text)):
    captcha_text = text[i]
    data = image.generate(captcha_text)
    # assert isinstance(data, BytesIO)
    filename = './image/' + str(i) + '.png'
    label_dict[filename] = get_label_int(captcha_text)
    image.write(captcha_text, filename)

# json form
with open("labels.json", "w") as f:
    json.dump(label_dict, f)
