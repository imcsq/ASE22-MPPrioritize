from keras.models import load_model
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing import image
import numpy as np
import os
import argparse
import keras.backend.tensorflow_backend as KTF
import tensorflow as tf

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
KTF.set_session(sess)

parser = argparse.ArgumentParser(description='prioritize the test case')
parser.add_argument('--model_type', help='the type of the selected model', type=str)
parser.add_argument('--diy', help='you can choose your MPs or the MPs we provide', type=bool,default=False)
parser.add_argument('--mp_path', help='the path of MPs', type=str)
parser.add_argument('--violation_record', help='the path to the result of recording the violation information', type=str)
args = parser.parse_args()

if args.model_type=='vgg16':
    from keras.applications.vgg16 import preprocess_input,VGG16
    model=VGG16(weights='imagenet')
    size=224
elif args.model_type=='resnet50':
    from keras.applications.resnet50 import preprocess_input,ResNet50
    model=ResNet50(weights='imagenet')
    size=224
elif args.model_type=='inception_v3':
    from keras.applications.inception_v3 import preprocess_input,InceptionV3
    model=InceptionV3(weights='imagenet')
    size=299
else:
    print('wrong model type')

print('Loading image... Please wait for a while...')
if args.diy:
    src_img = dict()
    fol_img = dict()
    for name in os.listdir(args.mp_path + 'source'):
        img_s = image.load_img(args.mp_path + 'source/' + name, target_size=(size, size))
        x_s = image.img_to_array(img_s)
        x_s = np.expand_dims(x_s, axis=0)
        x_s = preprocess_input(x_s)
        src_img[name] = x_s
    for name in os.listdir(args.mp_path + 'follow-up'):
        img_f = image.load_img(args.mp_path + 'follow-up/' + name, target_size=(size, size))
        x_f = image.img_to_array(img_f)
        x_f = np.expand_dims(x_f, axis=0)
        x_f = preprocess_input(x_f)
        fol_img[name] = x_f
else:
    mp = np.load(args.mp_path)
    mp = mp['image.npy']
    mp = mp.tolist()
    if args.model_type == 'vgg16' or args.model_type == 'resnet50':
        src_img = mp['src_224']
        fol_img = mp['fol_224']
    elif args.model_type == 'inception_v3':
        src_img = mp['src_299']
        fol_img = mp['fol_299']
    else:
        print('wrong model type')

results={}
mr_list = ['dslr', 'vangogh', 'monet', 'cezanne', 'reconstruction']
print('Counting Violations... Please wait for a while...')
count=0
print(str(count)+'/'+str(len(fol_img)))
for i in src_img:
    count+=1
    if (count % 100 == 0):
        print(str(count*5) + '/' + str(len(fol_img)))
    x=src_img[i]
    preds = model.predict(x)
    result_src=decode_predictions(preds)[0][0][0]

    for mr in mr_list:
        name=i[:-4] + '_' + mr + '.png'
        x=fol_img[name]
        preds = model.predict(x)
        result_fol=decode_predictions(preds)[0][0][0]
        if result_src==result_fol:
            results[name]=0
        else:
            results[name]=1
folder = os.path.exists(args.violation_record)
if not folder:
    os.makedirs(args.violation_record)
np.save(args.violation_record+args.model_type+'.npy',results)
print('Result saved at '+args.violation_record+args.model_type+'.npy')



