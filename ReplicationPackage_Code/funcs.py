from keras.models import Model
import random
import collections
def jaccard(a, b):
    A = set(a)
    B = set(b)
    if  float(len(A.union(B)))==0:
        return 0
    return 1 - len(A.intersection(B)) / float(len(A.union(B)))

def get_intermediate_model(model,layer_names):
    intermediate_layer_model = Model(inputs=model.input, outputs=[model.get_layer(layer_name).output for layer_name in layer_names])
    return intermediate_layer_model

def get_outputs(input_data, model):
    layer_outputs = model.predict(input_data)
    return layer_outputs

def scale(layer_output, rmax=1, rmin=0):
    X_std = (layer_output - layer_output.min()) / float(
             layer_output.max() - layer_output.min())
    X_scaled = X_std * (rmax - rmin) + rmin
    return X_scaled

def concatenate(layer_outputs):
    p=[]
    for i in layer_outputs:
        p.append(i)
    return p

def random_dic(dicts):
    random.seed(1)
    dict_key_ls = list(dicts.keys())
    random.shuffle(dict_key_ls)
    new_dic = collections.OrderedDict()
    for key in dict_key_ls:
        new_dic[key] = dicts.get(key)
    return new_dic


