
# Practicum Week 2 Answers

Andrew Lim
22 Oct 2012

All problems can be run with `python run_fda.py --all-problems`. Individual problems can be run with flags as specified below. 

### Problem 1

I did the initial cleanup work using Google Refine. The JSON files that describe the transformations I did are in `data/google-refine`. I actually think the entirety of problem 1, transforming the data in this fashion, could theoretically be done in Refine, but I found Refine to be crashy for NUT_DATA-sized projects. The cleaned-up csvs are in `data`: 

- `data/FD_GROUP.csv`
- `data/FOOD_DES.csv`
- `data/NUT_DATA.csv`
- `data/NUTR_DEF.csv`

To generate the reformatted food data to `nutr_by_food.csv`, run `python run_fda.py --food-detail`. This generates a column for every single nutrient. The food label filtration is done later, see problem 3. 

### Problem 2

I found it useful to apply a log1p transformation to the nutrient data to get less skewed distributions. 

To figure out what columns to plot, I calculated the correlations of magnesium against other nutrients. You can generate the table of such correlations with `python run_fda.py --magnesium_corrs` (this is not run as part of the `--all-problems` command, as I just used it as a sort of diagnostic). I disregarded correlations with too few observations (for example, "Adjusted Protein" had only 2 observations and so naturally the correlation was 1). 

Some of the highest relevant positive correlations were with potassium, phosphorus, and manganese, which had (log1p-transformed) correlations of 0.7638, 0.7361, and 0.6006, respectively. The negative correlations were generally not as strong. 

There were some graphs that seemed to show a relationship between magnesium and _variance_ of nutrient level. An example is the total trans fatty acids, which had a log1p-transformed correlation of -0.4189. From the scatterplot, you can see that low-magnesium foods have a wide variety of trans fatty acid levels, some very high but some very low, and high-magnesium foods have both lower fatty acid levels overall and less variation in levels. Manganese shows this to a lesser degree in the opposite direction; low-magnesium foods have consistently low levels of manganese, and high-magnesium foods have both higher levels of manganese and higher variation in those levels. 

To generate scatterplots for magnesium versus potassium, phosphorus, manganese, and trans fatty acids, run `python run_fda.py --magnesium-scatter`. They will be produced into the `scatter` directory. 

### Problem 3

The features I found on nutrition data labels for which there were columns in SR22 were: 

- Fatty acids, total saturated
- Fatty acids, total polyunsaturated
- Fatty acids, total monounsaturated
- Fatty acids, total trans
- Cholesterol
- Sodium, Na
- Potassium, K
- Fiber, total dietary
- Sugars, total
- Calcium, Ca
- Iron, Fe
- Zinc, Zn
- Phosphorus, P
- Copper, Cu
- Manganese, Mn
- Thiamin
- Riboflavin
- Niacin
- Vitamin A
- Vitamin B6
- Vitamin B12
- Folate

Vitamin A and folate are reported in a few different ways - I used the "equivalents" columns, which are the "RAE" column (retinol activity equivalents) for Vitamin A and the "DFE" column (dietary folate equivalents) for folate. These are intended to measure overall nutritional content of a few different ways the body can acquire these nutrients. 

The full data set is 7538 foods, but since I can only use rows for which all of these values are present, the regression ended up being on only 711 of those 7538 foods. Run `python run_fda.py --full-reg` to generate the regression summary to `regressions/full_reg.txt` and the pickled statsmodels results object to `regressions/full_reg.pkl`. As before, these are on the log1p-transformed data. 

The R^2 of the full regression is 0.819. The coefficients significant at the 5% threshold or better are: 

- Sodium, Na
- Potassium, K
- Fiber, total dietary
- Sugars, total
- Phosphorus, P
- Copper, Cu
- Manganese, Mn
- Thiamin
- Niacin
- Vitamin B12

The constant term was in fact not statistically significant. There was no predictive significance added by aggregating the fatty acid columns into a single feature. These findings suggest that we can actually drop several of these coefficients (and incorporate more data points, since we'll have to drop fewer rows), although it looks like we'll be doing that in later problems. 

The average absolute error of the full model (including statistically insignificant coefficients) in log1p-space is 0.250. When translated back to regular mg of magnesium, the average absolute error is 11.759 mg. 

For a model I could keep in my head, the first order of business would be to consider just the above features. To reduce it further, we can drop the features with smallest coefficients. Before doing that you have to check whether the range of values for the different features varies substantially - a small coefficient could be more important than a large coefficient if the small coefficient's feature had much larger values. I checked the standard deviations of the features and they're all between 1.74 and 2.16. The features we would drop in this case would be sodium, sugar, and niacin. If I really wanted to make it simple to remember, thiamin and vitamin B12's coefficients are around -0.2 and the others are all around +0.25, so I'd just round that way. 

### Problems 4 and 5

Run `python run_fda.py --bootstrap` to generate bootstrap data to `bootstrap_data/coefs.csv` based on a resampling size of 25% (so each regression is based on floor(0.25 * 711) = 177 of the 711 available entries) and to print out the 95% confidence interval of parameters. The exact values will of course differ from run to run, but what I found was that the coefficients whose 95% bands did not include 0 generally included:

- Sodium, Na
- Potassium, K
- Fiber, total dietary
- Phosphorus, P
- Manganese, Mn
- Vitamin B12

This is a subset of the features mentioned in Problem 3. These features are the ones where the hypothesis of a 0 coefficient was rejected at 95% by this procedure. The width of the confidence intervals correspond to uncertainty about the predicted values. Of the above six features, manganese has the widest interval, indicating greatest uncertainty; while the hypothesis of a zero coefficient is rejected with good certainty, the actual coefficient to use to predict magnesium is unclear. 

Based on these results, a one-sentence heuristic for finding high-magnesium foods is to look for high potassium, fiber, and phosphorus, and to avoid high sodium and vitamin B12. 

### Problem 6

With only the six features above, we actually have much more data at our disposal since we don't need to drop nearly as many rows. The number of foods that have entries for all six features is 5189, up from 711. 

Running the regression on the expanded data set, the R^2 is still 0.813. The average error on the expanded data set is up a little bit - on the log1p data it's 0.2858, and transformed back out to mg of magnesium it's 12.783553. For a stricter apples-to-apples comparison, I ran it on only the 711 data lines that we'd been previously using and produced an average error of 0.2727 and 13.1287, respectively.