
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

### Problem 4

### Problem 5

### Problem 6