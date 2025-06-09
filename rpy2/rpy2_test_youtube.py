import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

pandas2ri.activate()

#getting the iris df from R and summarizing it
utils = importr('utils')
dpylr = importr('dplyr')

robjects.r('data(iris)')

robjects.r('''
library(dplyr)
iris_summary <- iris %>%
group_by(Species) %>%
summarise(
    Avg_Sepal_Length = mean(Sepal.Length),
    Avg_Sepal_Width = mean(Sepal.Width)
)
''')

#work with iris pf in python
iris_summary = pandas2ri.rpy2py(robjects.r['iris_summary'])
print(iris_summary)
print(type(iris_summary))