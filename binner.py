import pandas as pd
import numpy as np

# Sample data
data = [1, 2, 3]
df = pd.DataFrame({'value': data})

# Create bins
df['bins'] = pd.cut(df['value'], bins=2, labels=False)

print(df)

h = np.histogram(data, bins=2)
print(h)