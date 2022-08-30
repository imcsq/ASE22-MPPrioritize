## Content of Complete Experimental Results

Due to the space limit for the paper, we have not included the experimental results under all configuration setups or for all diversity metrics in our paper. Here we release the other relevant experimental results, i.e., (a) the NAPVD of each candidate metric under all configuration setups; (b) the box plots of the diversity among MPs of different MRs w.r.t. all implementations of our metric.

These results confirm that:
1) Besides under the default configuration (which has been specifically demonstrated in RQ1 in the paper), **our method and metric can also effectively outperform the baselines under the other setups**. This can be supported by the stably higher NAPVD for our method and metric in the complete experimental results (a).
2) Besides HD (whose performance has been specifically discussed in RQ2 in the paper), the other effective implementation of our diversity metric, **JS, also conforms with the conclusions of the configuration sensitivity analysis in our paper**. This can be supported by the corresponding NAPVD comparison over the complete experimental results (a).
3) Besides HD (whose correlation to the violation detection ability of MRs has been discussed in RQ3 in the paper), the other effective implementation of our diversity metric, **JS, also correlates to the violation detection ability of MRs**. This can be supported by the statistical data in the box plots from the complete experimental results (b).

### File Structure

```
CompleteResults
┝━━ "RQ1&2 (Comparison under all configurations)"
│   # (a) The NAPVD of each candidate metric under all configuration setups.
┕━━ "RQ3 (Box plots for all implementations of our metric)"
    # (b) The box plots of the diversity among MPs of different MRs w.r.t. all implementations of our metric.
```
