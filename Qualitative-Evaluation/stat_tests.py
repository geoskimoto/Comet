import numpy as np
import pandas as pd
import scipy.stats as stats

def check_normality(comet_scores, race_scores):
    # Calculate the differences
    differences = comet_scores - race_scores

    # Perform the Shapiro-Wilk test for normality
    shapiro_statistic, shapiro_p_value = stats.shapiro(differences)

    print("Shapiro-Wilk Test for normality:")
    print(f"Statistic: {shapiro_statistic}, p-value: {shapiro_p_value}")

    # Evaluate the normality
    if shapiro_p_value > 0.05:
        print("Differences between paired samples are normally distributed (fail to reject H0).")
    else:
        print("Differences between paired samples are NOT normally distributed (reject H0).")

def check_significance_wilcoxon(comet_scores, race_scores, title):
    zstatistic, p_value = stats.wilcoxon(comet_scores, race_scores, alternative='greater')

    # Correct calculation of the effect size (rank-biserial correlation)
    n = len(comet_scores)
    r = zstatistic / (n * (n + 1) / 2)
    
    print(f"Wilcoxon Signed-Rank Test for {title}, the r value is {r}, zstats is {zstatistic}")

    # Check the p-value
    if p_value < 0.1:
        print(f"The COMET's {title} predictions are significantly better than RACE's {title} predictions (p < 0.1).")
    else:
        print(f"No significant evidence found that COMET's {title} predictions are better than RACE's {title} predictions (p >= 0.1).")

def ttest_significance_ttest(comet_scores, race_scores):
    # Perform the paired t-test if the differences are normally distributed
    t_statistic, t_p_value = stats.ttest_rel(comet_scores, race_scores, alternative='greater')
    
    print("Paired t-test results:")
    print(f"t-Statistic: {t_statistic}, p-value: {t_p_value}")
    
    # Check the significance of the results
    if t_p_value < 0.1:
        print("COMET's predictions are significantly better than RACE's predictions (p < 0.1).")
    else:
        print("No significant evidence found that COMET's predictions are better than RACE's predictions (p >= 0.1).")
    

# Assuming you have the 3 Excel files as 'reviewer1.xlsx', 'reviewer2.xlsx', 'reviewer3.xlsx'
# Load the data from Excel files
df1 = pd.read_csv('Review-1.csv')
df2 = pd.read_csv('Review-2.csv')
df3 = pd.read_csv('Review-3.csv')

# Concatenate the scores from the three reviewers into two arrays
# race_scores = np.concatenate([df1['Pred1_score'].values, df2['Pred1_score'].values, df3['Pred1_score'].values])
# comet_scores  = np.concatenate([df1['Pred2_score'].values, df2['Pred2_score'].values, df3['Pred2_score'].values])
# # Concatenate the scores from the three reviewers into two arrays
race_scores = (df1['Pred1_score'].values + df2['Pred1_score'].values + df3['Pred1_score'].values)/3
comet_scores = (df1['Pred2_score'].values + df2['Pred2_score'].values + df3['Pred2_score'].values)/3

# check_normality(comet_scores, race_scores)
ttest_significance_ttest(comet_scores, race_scores)

# Run the Wilcoxon Signed-Rank Test
# check_significance_wilcoxon(comet_scores, race_scores, "Commit Message Quality Assessment")