#template from David, to test rpy2

# set up rpy2 in python
import rpy2
print(rpy2.__version__)
import rpy2.robjects as robjects
r=robjects.r
from rpy2.robjects import numpy2ri
numpy2ri.activate()
from rpy2.robjects import pandas2ri
pandas2ri.activate()  # Enable conversion

# compile R scripts. I would put calls to R libraries in the R scripts.
r.source("my_r_script.R")
print(r['getwd']())
city_df = r['city_df']
#print(city_df)
#make into pandas
city_df_pd = pandas2ri.rpy2py(city_df)  # Convert to pandas DataFrame
print(city_df_pd)


#r.source('/home/h06/edauster/Documents/python/CoinCalc/R/CoinCalc.R')
# # might be able to parse python variables straight into R but if R complains then wrap the input variables into R type vector objects
# ra = rpy2.robjects.vectors.IntVector(self._seriesA)         # convert np array to vetcor for R
# rb = rpy2.robjects.vectors.IntVector(self._seriesB)
 
# # exampes of how to run r commands. 
# abin = r['CC.binarize'](ra, ev_def, thres)                  #binarise time series for ECA function to work
# bbin = r['CC.binarize'](rb, ev_def, thres)
 
# ECA_output = r['CC.eca.ts'](abin, bbin, delT=self._delT, tau=self._tau, sym=self._sym, sigtest=sigtest)

# # example of how to get a named output variable
# p_nh_prec = self._poisson.rx2('NH precursor')[0]

# For unnamed variables I would try:
# results = routput.rx2() 
