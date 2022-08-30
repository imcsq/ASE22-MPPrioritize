import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
import collections

parser = argparse.ArgumentParser(description='draw a table to show diversity')
parser.add_argument('--vgg16_diversity_path', help='the path to store the diversity information for VGG16', type=str)
parser.add_argument('--resnet50_diversity_path', help='the path to store the diversity information for ResNet50', type=str)
parser.add_argument('--inception_v3_diversity_path', help='the path to store the diversity information for Inception_V3', type=str)
parser.add_argument('--vgg16_violation_record', help='the path to the result of recording the violation information for VGG16', type=str)
parser.add_argument('--resnet50_violation_record', help='the path to the result of recording the violation information for ResNet50', type=str)
parser.add_argument('--inception_v3_violation_record', help='the path to the result of recording the violation information for Inception_V3', type=str)
parser.add_argument('--output_path', help='the path to store the table image', type=str)
args = parser.parse_args()


vgg16_diversity=np.load(args.vgg16_diversity_path)
vgg16_diversity=vgg16_diversity.tolist()
resnet50_diversity=np.load(args.resnet50_diversity_path)
resnet50_diversity=resnet50_diversity.tolist()
inception_v3_diversity=np.load(args.inception_v3_diversity_path)
inception_v3_diversity=inception_v3_diversity.tolist()
vgg16_results=np.load(args.vgg16_violation_record)
vgg16_results=vgg16_results.tolist()
resnet50_results=np.load(args.resnet50_violation_record)
resnet50_results=resnet50_results.tolist()
inception_v3_results=np.load(args.inception_v3_violation_record)
inception_v3_results=inception_v3_results.tolist()
model_diversity=dict()
model_diversity['vgg16']=vgg16_diversity
model_diversity['resnet50']=resnet50_diversity
model_diversity['inception_v3']=inception_v3_diversity
model_results=dict()
model_results['vgg16']=vgg16_results
model_results['resnet50']=resnet50_results
model_results['inception_v3']=inception_v3_results
col=['vgg16','inception_v3','resnet50']
row=['delta_nc','nd','bd','td','sd','wd','kl','js','hd']
vals=[]
for model_type in col:
    diversity = model_diversity[model_type]
    results = model_results[model_type]
    temp=[]
    for type in row:
        d=collections.OrderedDict()
        for name in diversity:
            d[name] = diversity[name][type]
        d = sorted(d.items(), key=lambda x: x[1], reverse=True)
        violations=[]
        count=0
        for i in d:
            count += 1
            name = i[0]
            if results[name] == 1:
                violations.append(count)
        apvd = 1 - (np.sum(violations) / (len(d) * len(violations))) + 1 / (2 * len(d))
        apvd_min = len(violations) / (2 * len(d))
        apvd_max = 1 - apvd_min
        napvd = (apvd - apvd_min) / (apvd_max - apvd_min)
        temp.append(format(napvd,'.4f'))
    vals.append(temp)
vals=np.asarray(vals).T
plt.figure(figsize=(20,8))
tab = plt.table(cellText=vals,
              colLabels=col,
             rowLabels=row,
              loc='center',
              cellLoc='center',
              rowLoc='center')
tab.scale(1,2)
plt.axis('off')
folder = os.path.exists(args.output_path)
if not folder:
    os.makedirs(args.output_path)
plt.savefig(args.output_path+'Table.eps',bbox_inches = 'tight')
print('Table image has been saved to', args.output_path+'Table.eps successfully')

print('The row represents different test objects. The column represents different diversity.')
print('\tVGG16\tResNet50\tInception_V3')
for i in range(0,len(row)):
    print(row[i]+' ',end='')
    for j in range(0,len(col)):
        print(str(vals[i][j])+'\t',end='')
    print('\n')
