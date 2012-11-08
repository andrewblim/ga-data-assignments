
# Data Class Answers - kNN vs. linear regression

Andrew Lim / 8 Nov 2012

To run everything, run `python run_knn.py`. The output is the `predictions.csv` file, a `summary.txt` file that outputs `summary()` on the statsmodels linear regression model object, and several `.pkl` files representing the pickled model result objects. 

`pip freeze` on my virtualenv: 

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

### Answers

I ran analysis on the white wine subset of the [Wine Quality Data Set](http://archive.ics.uci.edu/ml/datasets/Wine+Quality), using quality as the outcome variable. I used linear regression with a constant and also kNN with 1, 3, 5, and 10 neighbors, and each of those with both a regressor (treats the output value as continuous) and a classifier () The 1-NN model is just done