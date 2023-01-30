## Usage Instruction

We provide the implementation of our proposed diversity metric and prioritization method. They can help to prioritize any customized MPs, as well as replicate our evaluation experiments.

## Step-by-step Instruction and Explanation of Our Scripts

The steps to (a) prioritize any customized MPs, or (b) replicate our evaluation experiments are as follows:

1. Clone the whole repository and move to this "ReplicationPackage_Code" directory
```bash
git clone https://github.com/imcsq/ASE22-MPPrioritize/
cd ASE22-MPPrioritize/ReplicationPackage_Code
conda activate MPPrioritize # please first prepare the runtime environment following INSTALL.md
```

2. Prepare the MPs to be prioritized.
For (a), we provide 50 MPs as a brief and representative example in [this directory](../ReplicationPackage_MPExample). You can follow the structure to prepare your own MPs.
For(b), due to the file size, we haven't provided 5000MPs used in our evaluation in this repository directly. Please feel free to contact us( Ryannn@whu.edu.cn) to get the file, if you want to replicate our evaluation experiments.

1. Run `1_calc_all_diversity.py` to calculate the diversity w.r.t. all metrics for each MP on the specified test object and breakpoint.
```bash
python 1_calc_all_diversity.py --output_path /path/to/diversity/output_file --diy DIY --mp_path /path/to/MPs --layer_name BREAK_POINT_NAME --model_type MODEL --function_pickle_path /path/to/function_pickle

# --mp_path specifies the path to the file storing all MPs.
# --diy True means you could execute your MPs on your own referring to the file structure of '../ReplicationPackage_MPExample'. False means you want to execute all MPs used in our evaluation directly. You have to download the 'image.zip' in advance. And we set the default value False.
# --model_type specifies the test object, whose value can be one of 'vgg16','resnet50', and 'inception_v3'.
# --layer_name specifies the layer to be used as the breakpoint.
# --output_path specifies the path to store the diversity information about all the MPs.
# --function_pickle_path specifies the path to the directory storing the function pickle file necessary for SD and BD. such files for VGG16, Inception V3, and ResNet50 have been provided.

# e.g., please run:
# For (a): python 1_calc_all_diversity.py --diy True --mp_path='../ReplicationPackage_MPExample/' --model_type='resnet50' --layer_name='activation_25' --output_path='diversity/' --function_pickle='function_pickles_for_bd&sd/'
# For (b): python 1_calc_all_diversity.py --mp_path='image.zip' --model_type='resnet50' --layer_name='activation_25' --output_path='diversity/' --function_pickle='function_pickles_for_bd&sd/'
# Expect: a npy file `resnet50_activation_25_diversity.npy` will be generated in `diversity/` to store all diversity information about all MPs.
```

4. Run `2_count_violations.py` to identify the violations within all MPs.
```bash
python 2_count_violations.py --diy DIY --mp_path /path/to/MPs --model_type MODEL --violation_record /path/to/violations/output_file

# --diy True represents you could execute your MPs on your own referring to the file structure of '../ReplicationPackage_MPExample'. False represents you want to execute all MPs used in our evaluation directly. You have to download the 'image.zip' in advance.
# --mp_path specifies the path to the file storing all MPs. And we set the default value False.
# --model_type specifies the test object, whose value can be one of 'vgg16','resnet50', and 'inception_v3'.
# --violation_record specifies the file to store the violation situation of all MPs.

# e.g., please run:
# For (a): python 2_count_violations.py --diy True --mp_path='../ReplicationPackage_MPExample/' --model_type='resnet50' --violation_record='violations/'
# For (b): python 2_count_violations.py --mp_path='image.zip' --model_type='resnet50' --violation_record='violations/'
# Expect: a npy file `resnet50.npy` will be generated in `violations/` to store the violation situation of all MPs. 
```

5. Run `3_prioritize.py` to prioritize the MPs with a specified type of diversity.
```bash
python 3_prioritize.py --output_path /path/to/prioritization/output_file --diversity_file /path/to/diversity/output_file --diversity_type DIVERSITY

# --diversity_file specifies the file that includes the diversity information of MPs derived from step 2.
# --diversity_type specifies the diversity criteria used for prioritization, whose value can be one of 'hd', 'js', 'kl', 'wd', 'delta_nc', 'nd', 'sd', 'bd', and 'td.
# --output_path specifies the path to store the priority of the MPs.

# e.g., please run: python 3_prioritize.py --diversity_file='diversity/resnet50_activation_25_diversity.npy' --diversity_type='hd' --output_path='prioritize/'
# Expect: a npy file `output.npy` will be generated in `prioritize/` to store the priority of all MPs. This is the final output of our proposed methodology. We next follow the priority to execute MPs, so as to boost the revealing of detected violations.
```

6. Run `4_calc_napvd.py` to measure the prioritization performance.
```bash
python 4_calc_napvd.py --prioritization_file /path/to/prioritization/output_file --violation_record /path/to/violations/output_file

# --prioritization_file specifies the file to store the priority of all MPs derived from step 3.
# --violation_record specifies the violation situation record file derived from step 4.

# e.g., please run: python 4_calc_napvd.py --prioritization_file='prioritize/output.npy' --violation_record='violations/resnet50.npy'
# Expect: a NAPVD value will be printed on the screen, reflecting the boosting performance of the previously obtained prioritization results.
```

### Instruction to Obtain Results for each RQ

In this section, we introduce the method to leverage the above-mentioned scripts to obtain the results for each RQ in batch. The following example commands are for replicating the experiments (mode (b)). You can also use the mode (a) commands introduced above to obtain results for the customized MPs.

1. Run prioritization for various models with different diversity metrics and the default configuration to get the NAPVD result table for RQ1 (which is the core result of the evaluation of this work).
```bash
# e.g., for replicating the experiments (mode (b)), you can execute:
python 1_calc_all_diversity.py --mp_path='image.zip' --model_type='vgg16' --layer_name='block4_conv1' --output_path='diversity/' --function_pickle='function_pickles_for_bd&sd/'
python 1_calc_all_diversity.py --mp_path='image.zip' --model_type='resnet50' --layer_name='activation_25' --output_path='diversity/' --function_pickle='function_pickles_for_bd&sd/'
python 1_calc_all_diversity.py --mp_path='image.zip' --model_type='inception_v3' --layer_name='activation_55' --output_path='diversity/' --function_pickle='function_pickles_for_bd&sd/'
python 2_count_violations.py --mp_path='image.zip' --model_type='vgg16' --violation_record='violations/'
python 2_count_violations.py --mp_path='image.zip' --model_type='resnet50' --violation_record='violations/'
python 2_count_violations.py --mp_path='image.zip' --model_type='inception_v3' --violation_record='violations/'

# summarize the above results and generate the whole NAPVD result table (including the features of 3_prioritize.py and 4_calc_napvd.py):
python draw_table.py --vgg16_diversity_path='diversity/vgg16_block4_conv1_diversity.npy' --resnet50_diversity_path='diversity/resnet50_activation_25_diversity.npy' --inception_v3_diversity_path='diversity/inception_v3_activation_55_diversity.npy' --vgg16_violation_record='violations/vgg16.npy' --resnet50_violation_record='violations/resnet50.npy' --inception_v3_violation_record='violations/inception_v3.npy' --output_path='results/'
# --vgg16_diversity_path specifies the file to store the diversity information about all the MPs for VGG16.
# --resnet50_diversity_path specifies the file to store the diversity information about all the MPs for ResNet50.
# --inception_v3_diversity_path specifies the file to store the diversity information about all the MPs for Inception_V3.
# --vgg16_violation_record specifies the file to store the violation situation of all MPs for VGG16.
# --resnet50_violation_record specifies the file to store the violation situation of all MPs for ResNet50.
# --inception_v3_violation_record specifies the file to store the violation situation of all MPs for Inception_V3.
# --output_path specifies the path to store the table image.

# Expect: A table will be printed on the screen to organize and show all the NAPVDs. A file `Table.eps` will be generated in `results/` as well (it is the beautified version of the printed table and if needed, please use the default image viewer in Ubuntu or other correct viewers to view it). 
# !!! The above example commands for replicating (mode (b)) will replicate the NAPVDs in **Table-1** in our paper. These NAPVDs are the overall results of our evaluation. !!!
```

2. Run prioritization for a model with a specified diversity metric and a specified configuration (e.g., breakpoint location and output type), to investigate the configuration sensitivity of the proposal and answer RQ2. The data in `CompleteResults/RQ1&2 (Comparison under all configurations)/` are also obtained in this way.

```bash
# e.g., for replicating the experiments (mode (b)) to investigate the sensitivity of metric `HD` about breakpoint location on VGG16 model, you can execute:
python 1_calc_all_diversity.py --mp_path='image.zip' --model_type='vgg16' --layer_name='block1_conv1' --output_path='diversity/' --function_pickle='function_pickles_for_bd&sd/'
python 1_calc_all_diversity.py --mp_path='image.zip' --model_type='vgg16' --layer_name='block2_conv1' --output_path='diversity/' --function_pickle='function_pickles_for_bd&sd/'
python 1_calc_all_diversity.py --mp_path='image.zip' --model_type='vgg16' --layer_name='block3_conv1' --output_path='diversity/' --function_pickle='function_pickles_for_bd&sd/'
python 1_calc_all_diversity.py --mp_path='image.zip' --model_type='vgg16' --layer_name='block4_conv1' --output_path='diversity/' --function_pickle='function_pickles_for_bd&sd/' # if you have executed this command before for the other purposes (e.g., generating Table-1), just skip it to save time
python 1_calc_all_diversity.py --mp_path='image.zip' --model_type='vgg16' --layer_name='block5_conv1' --output_path='diversity/' --function_pickle='function_pickles_for_bd&sd/'
python 2_count_violations.py --mp_path='image.zip' --model_type='vgg16' --violation_record='violations/' # if you have executed this command before for the other purposes (e.g., generating Table-1), just skip it to save time
python 3_prioritize.py --diversity_file='diversity/vgg16_block1_conv1_diversity.npy' --diversity_type='hd' --output_path='prioritize/'
python 4_calc_napvd.py --prioritization_file='prioritize/output.npy' --violation_record='violations/vgg16.npy'
python 3_prioritize.py --diversity_file='diversity/vgg16_block2_conv1_diversity.npy' --diversity_type='hd' --output_path='prioritize/'
python 4_calc_napvd.py --prioritization_file='prioritize/output.npy' --violation_record='violations/vgg16.npy'
python 3_prioritize.py --diversity_file='diversity/vgg16_block3_conv1_diversity.npy' --diversity_type='hd' --output_path='prioritize/'
python 4_calc_napvd.py --prioritization_file='prioritize/output.npy' --violation_record='violations/vgg16.npy'
python 3_prioritize.py --diversity_file='diversity/vgg16_block4_conv1_diversity.npy' --diversity_type='hd' --output_path='prioritize/'
python 4_calc_napvd.py --prioritization_file='prioritize/output.npy' --violation_record='violations/vgg16.npy'
python 3_prioritize.py --diversity_file='diversity/vgg16_block5_conv1_diversity.npy' --diversity_type='hd' --output_path='prioritize/'
python 4_calc_napvd.py --prioritization_file='prioritize/output.npy' --violation_record='violations/vgg16.npy'

# Expect: Every time executing `4_calc_napvd.py`, the NAPVD corresponding to the specified configuration will be printed. The users can collect all the outputted NAPVDs and use the other tools to formulate intuitive tables and figures. 
# !!! The above example commands for replicating (mode (b)) will give five NAPVDs, corresponding to using the beginning layers of the five blocks in VGG16 as the breakpoint. These data are used to formulate the blue solid line in **Figure-5(a)** in our paper. !!!
# For the other data points of the other configurations (which cannot be completely enumerated here), users can adjust parameters and run our scripts in this way to obtain the corresponding NAPVDs. 
```

3. Calculate diversity and draw box plots that reflect the correlation between the violation revealing abilities of different MRs and their MPs' diversity (for RQ3). The figures in `CompleteResults/RQ3(Box plots for all implementations of our metric))/` are also obtained in this way.
```bash
# e.g., for replicating the experiments (mode (b)) to investigate the correlation between the HD-based diversity and the violation rates on ResNet50 model, you can execute:
python 1_calc_all_diversity.py --mp_path='image.zip' --model_type='resnet50' --layer_name='activation_25' --output_path='diversity/' --function_pickle='function_pickles_for_bd&sd/' # if you have executed this command before for the other purposes (e.g., generating Table-1), just skip it to save time
python 2_count_violations.py --mp_path='image.zip' --model_type='resnet50' --violation_record='violations/' # if you have executed this command before for the other purposes (e.g., generating Table-1), just skip it to save time
python box_plot.py --diversity_path='diversity/resnet50_activation_25_diversity.npy' --output_path='results/' --diversity_type='hd' --violation_record='violations/resnet50.npy'
# --diversity_path specifies the file to store the diversity information about all MPs.
# --output_path specifies the path to store the Box Plot image.
# --diversity_type specifies the diversity criteria used for prioritization, whose value can be one of 'hd', 'js', 'kl', 'wd', 'delta_nc', 'nd', 'sd', 'bd', and 'td.
# --violation_record specifies the file to store the violation situation of all MPs for specified model.

# Expect: A box-plot image file `hd_Box_Plot.eps` will be generated in `results/` (please use the default image viewer in Ubuntu or other correct viewers to view it). 
# !!! The above example commands for replicating (mode (b)) will replicate the box plot image **Figure-9(c)** in our paper. !!!
# For the other diversity metric and models, users can adjust parameters and run our scripts in this way to obtain the corresponding box plots. 
```
