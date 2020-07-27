# Temporal reclassification

This repository is an implementation of "[Statistically-based
methodology for revealing real contagion trends and correcting
delay-induced errors in the assessment of COVID-19
pandemic](https://doi.org/10.1016/j.chaos.2020.110087)".

## Replication

To replicate the R_t values reported in the original paper, run the
following:

```bash
python arrivals.py --tc 5.1 --sigma 0.41 --t-min 2 --t-max 5 --arima 3,0,0 \
       < chile.csv \
    | python departures.py --t-min 14 --t-max 30 \
    | python rt.py
```

where `chile.csv` is a CSV file in which one column contains the
observed infections and is title "infection".
