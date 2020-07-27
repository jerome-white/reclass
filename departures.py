import sys
from argparse import ArgumentParser

import numpy as np
import pandas as pd

from distributions import Triangle

def reclass(df, pr):
    (win, limit) = map(len, (pr, df))
    weights = pr.to_numpy()
    keys = lambda x: dict(zip(('day', 'recovered'), x))

    for i in df.itertuples():
        j = min(i.Index + win, limit)
        adjusted = i.infected * weights
        values = zip(range(i.Index, j), adjusted.ravel())

        yield from map(keys, values)

arguments = ArgumentParser()
arguments.add_argument('--t-min', type=int)
arguments.add_argument('--t-max', type=int)
args = arguments.parse_args()

#
#
#
tri = Triangle(args.t_min, args.t_max)()
k = tri.iloc[:args.t_max-1].filter(items=['Pk'])

#
#
#
df = pd.read_csv(sys.stdin, usecols=['infected'])
start = len(df)

records = reclass(df, k)
recovered = (pd
             .DataFrame
             .from_records(records)
             .groupby('day')
             .sum())

df = (pd
      .concat((df, recovered), axis='columns')
      .rename_axis('day', axis='index'))
df.to_csv(sys.stdout)
