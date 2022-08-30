import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

parser = argparse.ArgumentParser(description='draw a table to show diversity')
parser.add_argument('--diversity_path', help='the path to store the diversity information', type=str)
parser.add_argument('--diversity_type', help='the type of the diversity', type=str)
parser.add_argument('--violation_record', help='the path to the result of recording the violation information',
                    type=str)
parser.add_argument('--output_path', help='the path to store the box plot image', type=str)
args = parser.parse_args()
diversity = np.load(args.diversity_path)
diversity = diversity.tolist()

mr_list = ['reconstruction', 'monet', 'vangogh', 'cezanne', 'dslr']
box_cezanne = []
box_monet = []
box_vangogh = []
box_reconstruction = []
box_dslr = []

for i in diversity:
    if i.split('.')[0].split('_')[-1] == 'cezanne':
        box_cezanne.append(diversity[i][args.diversity_type])
    if i.split('.')[0].split('_')[-1] == 'monet':
        box_monet.append(diversity[i][args.diversity_type])
    if i.split('.')[0].split('_')[-1] == 'vangogh':
        box_vangogh.append(diversity[i][args.diversity_type])
    if i.split('.')[0].split('_')[-1] == 'reconstruction':
        box_reconstruction.append(diversity[i][args.diversity_type])
    if i.split('.')[0].split('_')[-1] == 'dslr':
        box_dslr.append(diversity[i][args.diversity_type])

results = np.load(args.violation_record)
results = results.tolist()
violations_cezanne = 0
violations_monet = 0
violations_vangogh = 0
violations_reconstruction = 0
violations_dslr =0
for i in results:
    if results[i] == 1:
        if i.split('.')[0].split('_')[-1] == 'cezanne':
            violations_cezanne += 1
        if i.split('.')[0].split('_')[-1] == 'monet':
            violations_monet += 1
        if i.split('.')[0].split('_')[-1] == 'vangogh':
            violations_vangogh += 1
        if i.split('.')[0].split('_')[-1] == 'reconstruction':
            violations_reconstruction += 1
        if i.split('.')[0].split('_')[-1] == 'dslr':
            violations_dslr += 1

plt.figure(figsize=(25, 10))
plt.grid(axis='y', linestyle='dotted', color='gray')
labels = 'MR4\n' + str(format(violations_reconstruction / (len(results) / 5),'.3f' )), 'MR3\n'+ str(format(violations_vangogh / (len(results) / 5),'.3f' )), 'MR1\n'+ str(format(violations_cezanne / (len(results) / 5),'.3f' )), 'MR2\n'+ str(format(violations_monet / (len(results) / 5),'.3f' )), 'MR5\n'+ str(format(violations_dslr / (len(results) / 5),'.3f' ))
l1 = plt.boxplot([box_reconstruction, box_vangogh, box_cezanne, box_monet, box_dslr], labels=labels, showfliers=False,
                 widths=0.3)
plt.xticks(fontsize=35)
plt.yticks(np.arange(0.0, 0.40, 0.05), fontsize=35)
plt.ylabel('HD Diversity', fontsize=40)
folder = os.path.exists(args.output_path)
if not folder:
    os.makedirs(args.output_path)
plt.savefig(args.output_path+args.diversity_type+'_'+'Box_Plot.eps',bbox_inches = 'tight')
print('Box Plot image has been saved to '+ args.output_path+args.diversity_type+'_'+'Box_Plot.eps successfully')




