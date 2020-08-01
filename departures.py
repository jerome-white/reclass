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
arguments.add_argument('--normal-discharge', type=int)
arguments.add_argument('--extended-discharge', type=int)
args = arguments.parse_args()

if args.normal_discharge > args.extended_discharge:
    raise ValueError('Normal discharge should come before extended')

#
#
#
tri = Triangle(args.normal_discharge, args.extended_discharge)()
k = tri.filter(items=['Pk'])

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
