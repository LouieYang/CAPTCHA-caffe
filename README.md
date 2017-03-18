# CAPTCHA-caffe

Captcha-caffe is an extremely simple deep learning project to recognize simple fixed length captcha. Once trained your own model, it could be easily embedded in any app.

![app-sample](https://github.com/LouieYang/CAPTCHA-caffe/blob/master/train-sample/sample.png)

# Requirements
- h5py
- pycaffe
- numpy, scipy

# Pre-training
```
python generator/generator-v1.py --ntrain 200 --nval 100
```
where ntrain denotes the size of training dataset, nval denotes the size of validation dataset. The default length of captcha is 6, you can change it by adding "--captcha_len 6". If you want to train only on the digit captcha, you can set by adding "--charnum False".

# Training
```
/pathtocaffe/build/tools/caffe train --solver=model/solver.prototxt
```

# Sample Training-Loss Graph
![train-sample](https://github.com/LouieYang/CAPTCHA-caffe/blob/master/train-sample/train-test-image.png)

# Sample Trained Model
Sample Trained Model for 6 length captcha with 200K training set and 1k validation set could be download at [BaiduYun](http://pan.baidu.com/s/1o7NAxp4) or [GoogleDrive](https://drive.google.com/file/d/0BxvKyd83BJjYMUtQaktQcUs4VUk/view?usp=sharing).
