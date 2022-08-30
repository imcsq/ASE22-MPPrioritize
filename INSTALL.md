## Environment Preparation Instruction

The scripts depend on Python 3 and some necessary libraries. So, please first install Python 3 interpreter and execute the following commands to install the following libraries. 
*(We recommend you to use environment management tools (e.g., conda and virtualenv) to prepare a standalone python environment.)*

```bash
conda create -n MPPrioritize python=3.5.6 -y
conda activate MPPrioritize
conda install numpy=1.15.2 tensorflow-gpu=1.9 h5py=2.8.0 pillow=5.2.0 matplotlib=3.0.0 -y # If your device has a GPU, please execute this command to exactly replicate our runtime environment.
# conda install numpy=1.15.2 tensorflow=1.9 h5py=2.8.0 pillow=5.2.0 matplotlib=3.0.0 -y # If your device has no GPU, please execute this command to run our codes with CPU. This may bring some minor discrepancy in results due to the characteristic of calculation libraries. 
pip install scipy==1.4.1 keras==2.0.6
```

After preparing the environment, please refer to [this document](ReplicationPackage_Code/README.md) for specific usage and replication instructions. 
