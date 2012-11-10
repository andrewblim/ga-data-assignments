
# Data Class Answers - kNN vs. linear regression

Andrew Lim / 8 Nov 2012

### Execution

To run model fitting, run `python run_knn.py`. The output is the `predictions.csv` file, a `summary.txt` file that outputs `summary()` on the statsmodels linear regression model object, and several `.pkl` files representing the pickled model result objects. 

To generate histograms of the data (not directly part of the assignment, but I used it to determine what kind of transformations to apply), run `python run_knn.py histograms`. The output is to the `histograms` directory. 

### Answers

I ran two analyses on the white wine subset of the [Wine Quality Data Set](http://archive.ics.uci.edu/ml/datasets/Wine+Quality). Some of the variables were positively skewed; I tried to fix these to be more normal with log1p transforms. The variables which the transform helped with were "residual sugar", "free sulfur dioxide", and "volatile acidity". I also transformed "total sulfur dioxide" and "free acidity" to keep them on the same scale as the latter two previously transformed variables. 

In the first analysis I used quality as the outcome variable. I used linear regression with a constant and also kNN with 1, 3, and 10 neighbors, and each of those with both a regressor (treats the output value as continuous) and a classifier (discrete categories). The quality rating was an integer between 0 and 10, and actually no rating was below 3 or above 9, so classification was a very reasonable approach. The 1-NN classifier and regressor are both included but they are the same since on the basis of only one neighbor they're going to predict the same value. 

In the second analysis I used pH as the outcome variable and used citric acid, fixed acidity, and total acidity as the predictor variables (the "acid" predictors). I used 1-NN, 3-NN, and 10-NN again but did not use classifiers here as pH is continuous. 

It is not reasonable to measure the efficacy of a model against the data with which it was trained. Doing this will give you a false impression of the model's strengths. For example, the 1-NN model would look perfect if you measured it against its own training data, since every point in the training data would return its exact value. To get around this problem, I randomly partitioned the data into 2 equal-sized "folds" and predicted values for each fold based on a model fit on the rest of the data. For what it's worth, increasing the folds to 5 or 10 did not have a substantial impact on the root mean squared errors.

The exact RMSEs will vary a little from run to run, but here is a representative result: 

#### 'quality' on all other variables

- 1-NN classifier: 1.2655
- 1-NN regressor: 1.2655
- 3-NN classifier: 1.2350
- 3-NN regressor: 1.1206
- 10-NN classifier: 1.1534
- 10-NN regressor: 1.0538
- Linear regression (w/constant): 1.0105

#### 'pH' on 'citric acid', 'fixed acidity', 'volatile acidity'

- 1-NN regressor: 0.2129
- 3-NN regressor: 0.1864
- 10-NN regressor: 0.1707
- Linear regression (w/constant): 0.1657

The regression model performs the bets in both cases, and the kNN models improve with higher k. The regressors beat the classifiers; even though 'quality' had a small set of possible values, the fact that those values were distinctly ordered seems to allow our regressors to win out. 

In both analyses I think a regression model is fine and probably preferable to the kNN models, certainly in the latter case. The kNN models are better for fitting a model where we expect the response variable to be potentially very unsmooth in its predictor variables. kNN's mechanism is to provide anchoring points on the unsmooth surface to allow your prediction to vary accordingly. I would not certainly not expect this to come up when trying to predict pH from acidity measures, and even in human-perceived quality, which certainly may be erratic in inputs, I would not expect the unsmoothness to be too severe for linear regression to handle. 

## pip freeze

In case there is some issue about getting the code to work, I'll always include this.

	Jinja2==2.6
	PyYAML==3.10
	Pygments==1.5
	Sphinx==1.1.3
	boto==2.6.0
	distribute==0.6.28
	docutils==0.9.1
	ipython==0.13.1
	matplotlib==1.1.1
	mrjob==0.3.5
	nose==1.2.1
	numpy==1.6.2
	pandas==0.9.0
	patsy==0.1.0
	python-dateutil==2.1
	pytz==2012h
	pyzmq==2.2.0.1
	rpy2==2.3.0beta1
	scikit-learn==0.12.1
	scipy==0.11.0
	simplejson==2.6.2
	six==1.2.0
	statsmodels==0.5.0
	tornado==2.4
	wsgiref==0.1.2
