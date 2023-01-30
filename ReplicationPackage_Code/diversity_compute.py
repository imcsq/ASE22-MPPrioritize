import scipy.stats
import numpy as np
import pickle
from collections import OrderedDict
import sys

def neuron_coverage(layer_outputs, threshold):
    covered_list = []
    count = 0
    sum=0
    for j in layer_outputs:
        sum+=1
        if j > threshold:
            count+=1
            covered_list.append(sum)
    return count/sum, covered_list

def hd(layer_outputs_s,layer_outputs_f):
    p=layer_outputs_s
    q=layer_outputs_f
    p = p / np.sum(p)
    q = q / np.sum(q)
    hd = 1 / np.sqrt(2) * np.linalg.norm(np.sqrt(p) - np.sqrt(q))
    return hd

def kl(layer_outputs_s,layer_outputs_f):
    p = layer_outputs_s
    q = layer_outputs_f
    kl = scipy.stats.entropy(p, q)
    if kl == np.inf:
       kl=1
    return kl

def js(layer_outputs_s,layer_outputs_f):
    p = layer_outputs_s
    q = layer_outputs_f
    p=np.asarray(p)
    q=np.asarray(q)
    M = (p + q) / 2
    js=0.5 * scipy.stats.entropy(p, M) + 0.5 * scipy.stats.entropy(q, M)
    return js

def wd(layer_outputs_s,layer_outputs_f):
    p=layer_outputs_s
    q=layer_outputs_f
    p = p / np.sum(p)
    q = q / np.sum(q)
    wd = scipy.stats.wasserstein_distance(p, q)
    return wd

def kmul(function_pickle_path,layer_outputs,layer_name,model_type,k=2):
    section_indexes = []
    with open(function_pickle_path+'min_'+model_type+'.pickle','rb') as f:
        min = pickle.load(f)
    with open(function_pickle_path+'max_'+model_type+'.pickle','rb') as f:
        max = pickle.load(f)

        for neuron_idx in range(len(layer_outputs)):
            lower_bound = min[(layer_name, neuron_idx)]
            upper_bound = max[(layer_name, neuron_idx)]
            unit_range = (upper_bound - lower_bound) / k
            output = layer_outputs[neuron_idx]
            if unit_range == 0:
                section_indexes.append(-sys.maxsize - 1)
                continue
            if output > upper_bound or output < lower_bound:
                section_indexes.append(-sys.maxsize - 1)
                continue
            subrange_index = int((output - lower_bound) / unit_range)
            if subrange_index == k:
                subrange_index -= 1
            section_indexes.append(subrange_index)
    return section_indexes

def nbc(function_pickle_path,layer_outputs,layer_name,model_type):
    cov_dict = OrderedDict()
    with open(function_pickle_path + '/min_'+model_type+'.pickle', 'rb') as f:
        min = pickle.load(f)
    with open(function_pickle_path + '/max_'+model_type+'.pickle', 'rb') as f:
        max = pickle.load(f)
    for neuron_idx in range(len(layer_outputs)):
        output = layer_outputs[neuron_idx]
        lower_bound = min[(layer_name, neuron_idx)]
        upper_bound = max[(layer_name, neuron_idx)]
        if output < lower_bound:
            cov_dict[(layer_name, neuron_idx)] = 0
        elif output > upper_bound:
            cov_dict[(layer_name, neuron_idx)] = 2
        else:
            cov_dict[(layer_name, neuron_idx)] = 1
    return cov_dict

def tknc(layer_outputs, k=1):
    section_indexes = []
    count=0
    min_num=-sys.maxsize-1
    topk={}
    for i in range(k):
        topk[i]=min_num
    for neuron_idx in range(len(layer_outputs)):
        output = layer_outputs[neuron_idx]
        min = sorted(zip(topk.values(), topk.keys()))[0]
        min_key = min[1]
        min_value = min[0]
        if output > min_value:
            del topk[min_key]
            topk[neuron_idx] = output
    for key in topk:
        section_indexes.append(key+count)
    count += len(layer_outputs)
    return section_indexes



