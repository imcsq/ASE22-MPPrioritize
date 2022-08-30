import numpy as np
import argparse
import collections
import os

parser = argparse.ArgumentParser(description='prioritize the test case')
parser.add_argument('--output_path', help='the path to store the prioritization information', type=str)
parser.add_argument('--diversity_file', help='the file including the diversity information of MPs', type=str)
parser.add_argument('--diversity_type', help='the type of the diversity', type=str)

args = parser.parse_args()


diversity=np.load(args.diversity_file)
diversity=diversity.tolist()
d=collections.OrderedDict()
for name in diversity:
    d[name] = diversity[name][args.diversity_type]
d = sorted(d.items(), key=lambda x: x[1], reverse=True)
for i in d:
    print(i)
folder = os.path.exists(args.output_path)
if not folder:
    os.makedirs(args.output_path)
np.save(args.output_path+'output.npy',d)
print('Result saved at '+args.output_path+'output.npy')
