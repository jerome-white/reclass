import sys
from argparse import ArgumentParser

import pandas as pd
from statsmodels.tsa.arima_model import ARIMA

from distributions import Z

arguments = ArgumentParser()
arguments.add_argument('--tc', type=float)
arguments.add_argument('--t-min', type=int)
arguments.add_argument('--t-max', type=int)
arguments.add_argument('--sigma', type=float)
arguments.add_argument('--threshold', type=float, default=0.75)
args = arguments.parse_args()

#
#
#
z = Z(args.tc, args.sigma, args.t_min, args.t_max)()
k = (z
     .query('F < {}'.format(args.threshold))
     .filter(items=['Pk'])
     .apply(lambda x: x / x.sum()))

#
#
#
df = pd.read_csv(sys.stdin, usecols=['infected'])
start = len(df)

arima = ARIMA(df, order=(3, 0, 0))
est = (arima
       .fit(disp=False)
       .predict(start, start + len(k))
       .to_frame('infected'))

df = df.append(est)
df.to_csv(sys.stdout, index=False)
