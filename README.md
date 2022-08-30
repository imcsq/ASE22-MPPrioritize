# **Artifact for the Paper "Boosting the Revealing of Detected Violations in Deep Learning Testing: A Diversity-Guide Method"**

This is the artifact for the *ASE 2022 Research Track* paper "*Boosting the Revealing of Detected Violations in Deep Learning Testing: A Diversity-Guide Method*".

It contains:

1. **The replication package for this paper:** 1) the implementation of our prioritization method and diversity metric; 2) the scripts to replicate our extensive evaluation experiments.
2. **The complete experimental results for this paper:** 1) the prioritization performance with all diversity metrics under all configurations; 2) the box plots of the diversity among the MPs of different MRs w.r.t. all implementations of our diversity metric.


------


## Content of Replication Package

We release the relevant code and data to replicate our experiments. Specifically, we provide: (a) the scripts to calculate our diversity metric (four implementations), as well as the five baseline diversity metrics for the given MPs; (b) the instruction, scripts, and MP set to replicate our evaluation experiments. 

Please first refer to [INSTALL.md](INSTALL.md) for the detailed instructions to prepare the runtime environment, and next refer to [this document](ReplicationPackage_Code/README.md) for the detailed instructions to use our scripts and replicate our experiments.

### File Structure

```
ReplicationPackage_Code
    # All necessary python scripts for running our prioritization method and diversity metric and replicating our evaluation experiments.
ReplicationPackage_MPExample
    # The source and follow-up cases (specific images) of example MPs used in our evaluation.
```


## Content of Complete Experimental Results

Due to the space limit for the paper, we have not included the experimental results under all configuration setups or for all diversity metrics in our paper. Here we release the other relevant experimental results, i.e., (a) the NAPVD of each candidate metric under all configuration setups; (b) the box plots of the diversity among MPs of different MRs w.r.t. all implementations of our metric.

These results give further evidence to confirm the conclusions in our paper. For more details, please refer to [this document](CompleteResults/README.md).


### File Structure

```
CompleteResults
┝━━ "RQ1&2 (Comparison under all configurations)"
│   # (a) The NAPVD of each candidate metric under all configuration setups.
┕━━ "RQ3 (Box plots for all implementations of our metric)"
    # (b) The box plots of the diversity among MPs of different MRs w.r.t. all implementations of our metric.
```

------

If you find our paper useful, please kindly cite it as:
```
@inproceedings{ASE22MPPrioritize,
  author    = {Xiaoyuan Xie and
               Pengbo Yin and
               Songqiang Chen},
  title     = {Testing Your Question Answering Software via Asking Recursively},
  booktitle = {Proceedings of the 37th {IEEE/ACM} International Conference on Automated Software Engineering, {ASE} 2022},
  year      = {2022},
}
```