
# Data Class Week 3 Answers

Andrew Lim / 5 Nov 2012

### kNN and Dark Sky

[Reference Dark Sky blog post](http://journal.darkskyapp.com/2012/how-dark-sky-calculates-temperature/)

Suppose we have a training set full of points (X, Y), where X is a vector of feature variables and Y is a variable we would like to be able to predict for any given value of X. The kNN algorithm, given a vector X, finds the points in the training set that are closest to X according to some defined metric and assesses a value Y on the basis of those k nearest neighbors via some kind of aggregating function. If Y is a continuous variable, the aggregation might be a weighted average of the Y-values of the neighbors, with weight proportional to proximity. If Y is a categorical variable, it might be the Y-value most commonly seen amongst the neighbors. Dark Sky's temperature prediction problem is a continuous-variable problem. 

The first-order "nearest station" approach described by Dark Sky is the same as a 1-NN model trained on publicly available National Weather Service data. The approach that Dark Sky uses is a 3-NN model where the aggregation function is temperature of the 3 nearest neighbors weighted by barycentric coordinate. 

Dark Sky first generates what's called a Delauney triangulation based on the National Weather Service station locations. Call that set T. The blog post states that the Delauney triangulation assures that for any point P, the triangle in which it lies are the 3 closest points in T. Call that triangle ABC. The coordinates of P are then converted into what are called barycentric coordinates with respect to ABC; if we express P as (pA, pB, pC), then pA is the area of PBC divided by the area of ABC, pB is PAC divided by ABC, and pC is PAB divided by ABC. (The areas are signed but since we're only considering points inside a triangle this distinction doesn't figure.) The barycentric coordinates are a way of weighting P's proximity to A, B, and C, and the predicted temperature T(P) can be taken as map(T, (A, B, C)) dot (pA, pB, pC). 

Using this aggregation, as the blog post points out, has the advantage of continuously smoothing the predicted temperature. As you approach the line between two nearest-neighbor weather stations on the triangulation, the weight assessed to the third station approaches 0, and on the line is 0 exactly. Likewise, as you approach a neighbor the weights on the other two neighbors approach 0 and are 0 exactly at the station. So as you move from one set of nearest neighbors to another, the predicted temperature fades out the weight from old neighbors and fades in weight to the new neighbors. In contrast, a simple average (the aggregation used in the lecture notes) will still generate discontinuities; all points within the same triangle have the same value and so you'll jump from one triangle to the next. 

The blog post doesn't say how Dark Sky handles points outside the triangulation. One solution might be to just use the negative barycentric coordinate from the nearest triangle. 

A linear regression model could predict temperature based on features of each station. The apples-to-apples comparison is to use latitude and longitude, as this is what Dark Sky uses as well, although you could jazz things up with elevation, distance to nearest major body of water, dummy variables indicating the regional climate type, etc. A very detailed regression might perform well, but I think Dark Sky's 3-NN approach will almost certainly outperform it. Linear regression is linear; it jams an n-dimensional plane through the data, n being the number of features. The 3-NN model has the flexibility to deal with different gradations, curves, and shapes of the predictor variable across the data set. 

The simplest way to think about 3-NN's superiority on latitude/longitude alone is to imagine a 3-d graph with a US map on the xy-plane and the temperatures hovering in z-space above. The temperature could very realistically form a bumpy, curvy surface, affected by fronts pointing in various directions, mountains, bodies of water, and regions of pressure. We see those kind of shapes on weather forecasts (usually color-coded rather than in 3-D). 3-NN can move up or down to match those. Linear regression would have to fit a plane through the data. 