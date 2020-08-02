# Temporal reclassification

This repository is an implementation of "[Statistically-based
methodology for revealing real contagion trends and correcting
delay-induced errors in the assessment of COVID-19
pandemic](https://doi.org/10.1016/j.chaos.2020.110087)".

## Replication

To replicate the R_t values reported in the original paper, run the
following:

```bash
$> python arrivals.py \
	  --incubation-days 5.1 \
	  --incubation-deviation 0.41 \
	  --diagnosis 2,5 \
	  --arima 3,0,0 \
	  < data.csv \
       | python departures.py \
		--normal-discharge 14 \
		--extended-discharge 30 \
       | python rt.py
```

where `data.csv` is a CSV file in which one column contains the
observed infections and is titled "infection".
