import argparse
from keras.models import load_model
import os
from keras.preprocessing import image
import numpy as np
from funcs import *
from NC import *
from diversity_compute import *
import collections
import keras.backend.tensorflow_backend as KTF
import tensorflow as tf

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
KTF.set_session(sess)

parser = argparse.ArgumentParser(description='count diversity')
parser.add_argument('--output_path', help='the path to store the diversity information', type=str)
parser.add_argument('--diy', help='you can choose your MPs or the MPs we provide', type=bool,default=False)
parser.add_argument('--mp_path', help='the path of MPs', type=str)
parser.add_argument('--layer_name', help='the layer name of the selected break point', type=str)
parser.add_argument('--model_type', help='the type of the selected model', type=str)
parser.add_argument('--function_pickle_path', help='the path of function pickle file', type=str)
args = parser.parse_args()

if args.model_type=='vgg16':
    from keras.applications.vgg16 import VGG16,preprocess_input
    model=VGG16(weights='imagenet')
    size=224
elif args.model_type=='resnet50':
    from keras.applications.resnet50 import ResNet50,preprocess_input
    model=ResNet50(weights='imagenet')
    size=224
elif args.model_type=='inception_v3':
    from keras.applications.inception_v3 import InceptionV3,preprocess_input
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

intermediate_model=get_intermediate_model(model,[args.layer_name])
mr_list = ['reconstruction', 'vangogh', 'cezanne', 'monet', 'dslr']
diversity=collections.OrderedDict()
count=0
print('Calculating Diversity...')
print(str(count)+'/'+str(len(fol_img)))
for name in fol_img:
    count+=1
    if(count%100==0):
        print(str(count)+'/'+str(len(fol_img)))
    source_image=name.rsplit('_',1)[0]+'.png'
    x_s=src_img[source_image]
    layer_outputs_s=get_outputs(x_s,intermediate_model)
    scale_outputs_s=[]
    origin_outputs_s=[]
    layer_output_s=layer_outputs_s[0]
    scale_output_s=scale(layer_output_s)
    for neuron_index in range(scale_output_s.shape[-1]):
        scale_outputs_s.append(np.mean(scale_output_s[..., neuron_index]))
    for neuron_index in range(layer_output_s.shape[-1]):
        origin_outputs_s.append(np.mean(layer_output_s[..., neuron_index]))
    #nd
    total_coverage_s_1, covered_neurons_s_1 = neuron_coverage(scale_outputs_s, 0.75)
    #nc
    total_coverage_s_2, covered_neurons_s_2 = neuron_coverage(scale_outputs_s, 0.5)
    tknc_section_indexes_s = tknc(scale_outputs_s, 1)
    section_indexes_s = kmul(args.function_pickle_path,origin_outputs_s,args.layer_name,args.model_type,2)
    nbc_s = nbc(args.function_pickle_path,origin_outputs_s,args.layer_name,args.model_type)
    temp=collections.OrderedDict()
    follow_image=name
    x_f=fol_img[follow_image]
    layer_outputs_f=get_outputs(x_f,intermediate_model)
    scale_outputs_f = []
    origin_outputs_f = []
    layer_output_f = layer_outputs_f[0]
    scale_output_f = scale(layer_output_f)
    for neuron_index in range(scale_output_f.shape[-1]):
        scale_outputs_f.append(np.mean(scale_output_f[..., neuron_index]))
    for neuron_index in range(layer_output_f.shape[-1]):
        origin_outputs_f.append(np.mean(layer_output_f[..., neuron_index]))
    total_coverage_f_1, covered_neurons_f_1 = neuron_coverage(scale_outputs_f, 0.75)
    nd = jaccard(covered_neurons_s_1, covered_neurons_f_1)
    # delta_nc
    total_coverage_f_2, covered_neurons_f_2 = neuron_coverage( scale_outputs_f, 0.5)
    delta_nc = abs(total_coverage_f_2 - total_coverage_s_2)
    # bd
    nbc_f = nbc(args.function_pickle_path,origin_outputs_f,args.layer_name,args.model_type)
    bd = BD_Compute(nbc_s, nbc_f)
    # sd
    section_indexes_f = kmul(args.function_pickle_path,origin_outputs_f,args.layer_name,args.model_type)
    sd = SD_Compute(section_indexes_s, section_indexes_f)
    # td
    tknc_section_indexes_f = tknc(scale_outputs_f, 1)
    td = TD_Compute(tknc_section_indexes_s, tknc_section_indexes_f)

    kl_d = kl(scale_outputs_s, scale_outputs_f)
    w_d = wd(scale_outputs_s, scale_outputs_f)
    js_d = js(scale_outputs_s, scale_outputs_f)
    h_d = hd(scale_outputs_s, scale_outputs_f)
    temp['nd'] = nd
    temp['delta_nc'] = delta_nc
    temp['kl'] = kl_d
    temp['js'] = js_d
    temp['hd'] = h_d
    temp['wd'] = w_d
    temp['sd'] = sd
    temp['bd'] = bd
    temp['td'] = td
    diversity[name] = temp

folder = os.path.exists(args.output_path)
if not folder:
    os.makedirs(args.output_path)
np.save(args.output_path+args.model_type+'_'+args.layer_name+'_diversity.npy',diversity)
print('Result saved at '+args.output_path+args.model_type+'_'+args.layer_name+'_diversity.npy')