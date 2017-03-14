import string
import numpy as np
import caffe
from PIL import Image

def sample(imgdir):
    net_file = "./deploy.prototxt"
    caffe_model = "./captcha_iter_80000.caffemodel"

    net = caffe.Net(net_file,caffe_model,caffe.TEST)
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

    im=np.array(Image.open(imgdir).convert('L').resize((100, 100)), dtype='f4')
    im = im / 255.
    # im = np.reshape(im, (1,) + im.shape)

    net.blobs['data'].data[...] = transformer.preprocess('data',im)
    out = net.forward()

    l_letter = [a for a in string.ascii_letters]
    l_digit = [d for d in string.digits]
    candidate = l_digit + l_letter
    theta_func = dict(zip(range(62), candidate))
    l = []
    l.append(theta_func[np.argmax(net.blobs['prob1'].data[0].flatten())])
    l.append(theta_func[np.argmax(net.blobs['prob2'].data[0].flatten())])
    l.append(theta_func[np.argmax(net.blobs['prob3'].data[0].flatten())])
    l.append(theta_func[np.argmax(net.blobs['prob4'].data[0].flatten())])
    l.append(theta_func[np.argmax(net.blobs['prob5'].data[0].flatten())])
    l.append(theta_func[np.argmax(net.blobs['prob6'].data[0].flatten())])

    return l

if __name__ == "__main__":
    print sample('./2.png')
