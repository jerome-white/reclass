import sys
from argparse import ArgumentParser

import numpy as np
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA

from distributions import Z

def reclass(df, pr):
    (win, limit) = map(len, (pr, df))
    weights = np.flip(pr.to_numpy())
    keys = lambda x: dict(zip(('day', 'infected'), x))

    for i in df.itertuples():
        j = i.Index + win
        if j > limit:
            break
        adjusted = i.infected * weights
        values = zip(range(i.Index, j), adjusted.ravel())

        yield from map(keys, values)

arguments = ArgumentParser()
arguments.add_argument('--incubation-days', type=float)
arguments.add_argument('--incubation-deviation', type=float)
arguments.add_argument('--diagnosis')
arguments.add_argument('--arima')
arguments.add_argument('--threshold', type=float, default=0.75)
args = arguments.parse_args()

#
#
#
(t_min, t_max) = sorted(map(int, args.diagnosis.split(',')))
z = Z(args.incubation_days, args.incubation_deviation, t_min, t_max)()
k = (z
     .query('F < {}'.format(args.threshold))
     .filter(items=['Pk'])
     .apply(lambda x: x / x.sum()))

#
#
#
df = pd.read_csv(sys.stdin, usecols=['infected'])
start = len(df)

order = tuple(map(int, args.arima.split(',')))
assert len(order) == 3
arima = ARIMA(df, order=order)
est = (arima
       .fit(disp=False)
       .predict(start, start + len(k))
       .to_frame('infected'))

records = reclass(df.append(est), k)
df = (pd
      .DataFrame
      .from_records(records)
      .groupby('day')
      .sum())
df.to_csv(sys.stdout)
