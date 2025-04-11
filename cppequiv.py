import sys
import numpy as np
sys.path.append('.')
import importlib
dynamicDistModule = importlib.import_module('DynamicDist')
dynamicDistClass  = getattr(dynamicDistModule, 'DynamicDist')
dynamicDistInstance = dynamicDistClass()
dynamicDistInstance.add(3.1415)
h,b = dynamicDistInstance.histogram()
print(h)
print(b)
h,b = np.histogram([3.14])
print(h)
print(b)