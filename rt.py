import sys

import pandas as pd

df = pd.read_csv(sys.stdin)
rt = (df['infected'] - df['recovered']) / df['recovered'] + 1
rt.to_csv(sys.stdout, index=False)
