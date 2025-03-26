import sys
import math
import time
import logging
import pandas as pd
import datetime

class Timer:

   performanceTemplate = {"calls": 0.0
                          , "elapsedMin": float('Inf')
                          , "elapsedMean": None
                          , "elapsedMax": float('-Inf')
                          , "elapsedTotal": 0.0
                          , "elapsedLast": None
                          , "startTime": None
                          }
   
   def __init__(self, logger = None):
      self.logger = logger
      if not self.logger:
         logging.basicConfig(level = logging.INFO)
         self.logger = logging.getLogger()
      self.performance = {}
      
   def start(self, methodName = None):
      # Get the name of the calling method
      methodName = methodName or sys._getframe(1).f_code.co_name
      # Get current performance stats
      performance = self.performance.get(methodName, Timer.performanceTemplate.copy())
      # Get the startTime
      performance["startTime"] = time.perf_counter()
      # Save it back in the dictionary
      self.performance[methodName] = performance
      
      
   def stop(self, methodName = None):
      # Get the name of the calling method
      methodName = methodName or sys._getframe(1).f_code.co_name
      # Get current performance stats
      performance = self.performance.get(methodName)
      # Compute the elapsed
      elapsed = time.perf_counter() - performance["startTime"]
      # Update the stats
      performance["calls"] += 1
      performance["elapsedLast"] = elapsed
      performance["elapsedMin"] = min(performance["elapsedMin"], elapsed)
      performance["elapsedMax"] = max(performance["elapsedMax"], elapsed)
      performance["elapsedTotal"] += elapsed
      performance["elapsedMean"] = performance["elapsedTotal"]/performance["calls"]
   

   def getStats(self):
      return pd.DataFrame.from_dict(self.performance, orient = "index")
   
   def showStats(self, methodName = None):
      methods = methodName or self.performance.keys()
      for method in methods:
         performance = self.performance.get(method)
         if performance:
            self.logger.info(f"Execution Stats ({method}):")
            for key in performance:
               if key != "startTime":
                  if key == "calls" or performance[key] == None:
                     value = performance[key]
                  elif math.isinf(performance[key]):
                     value = None
                  else:
                     value = datetime.timedelta(seconds = performance[key])
                  self.logger.info(f"  --> {key}:{value}")
         else:
            self.logger.warning(f"There are no execution stats available for method {method}!")