import pandas as pd
import numpy as np
import matplotlib as plt

###
# 1. Methods Cleaning Dataframe and getting dataframe to desired shape
###


# Remove the letter so that value H1 -> 1 and A4 -> 4
def remove_letter(df_codes):
    for column_i in df_codes.columns:
        for row_j in df_codes.index:
            # if the value is not NA, get everything but the from index 1 onward (A10 -> 10)
            if not pd.isna(df_codes[column_i][row_j]):
                df_codes[column_i][row_j] = df_codes[column_i][row_j][1:]
    # return matrix and fill every NA with 0
    return df_codes.fillna(0).astype('int')


# Remove the NaN-values of each columns and compress so that every NaN in between is removed
def compress_matrix(df_codes):
    columns = []
    # Get every column individually so each column can get compressed individually
    for i in df_codes.columns:
        # Drop the 0 from the column and reset the index
        columns.append(pd.DataFrame(df_codes[i].dropna()).
                       set_index(np.arange(0, len(df_codes[i].dropna()), 1)))
    # combine every column again and return
    return pd.concat(columns, axis=1)


# Count the occurance of each value and store in dataframe
def category_count(df_codes):
    # Create empty df to add the value counts to
    df_category_count = pd.DataFrame()
    for column_i in df_codes.columns:
        # add to df total count of categories
        df_category_count[column_i] = df_codes[column_i].value_counts().sort_index()[1:]
    # return df with category count and series with category count, series so it is easier to compare to other serie
    return df_category_count.fillna(0), df_category_count.transpose().stack(dropna=False)


#Combine every possible combination of series so that column 1 is for example serie_Remco en column 2 serie_Saskia
def combine_series(cc_series, names):
    combined_series = []
    serie_classifier = []
    # Take every possible combination of series without taking any combination double
    for serie_i in range(len(cc_series)):
        for serie_j in range(len(cc_series)):
            if serie_j > serie_i:
                temp = pd.concat([cc_series[serie_i], cc_series[serie_j]], axis=1).\
                    fillna(0).rename({0: 'A', 1: 'B'}, axis=1)
                for index_i in temp.index:
                    # Make sure that each category that both have not chosen is deleted (probably was no category)
                    if temp['A'][index_i]+temp['B'][index_i] == 0:
                        temp.drop(index_i, axis=0, inplace=True)
                # add two combined series to list and make sure each list has a classifier by index
                combined_series.append(temp)
                serie_classifier.append(str(f'{names[serie_i]} vs {names[serie_j]}'))
    return combined_series, serie_classifier


# Make sure series has same length as the rest (some have last row empty so df is smaller)
def uniformize_length(category_serie, length):
    # check if the df has the correct amount of rows, if not add an empty row
    if len(category_serie) < length:
        category_serie.loc[length] = [0, 0, 0, 0, 0, 0, 0, 0]
    return category_serie


# Combine different series of categories
def stack_series(category_series, names):
    data = {}
    # add each series to a dictionary with the corresponding name as row title/ key
    for index_i in range(len(category_series)):
        data[names[index_i]] = category_series[index_i].transpose().stack(dropna=False).to_numpy()
    df_perc = pd.DataFrame(data=data)
    # return for perc agreement the df where at least someone has coded a category
    return df_perc.loc[(df_perc != 0).any(axis=1)]

###
# 2. Calculate Percentage Agreement
###


# Function to add column for perc. agreement and the average perc. agreement
def perc_agreement(df_perc):
    perc_list = []
    # Calculate for each row the percentage agreement
    for row_i in range(len(df_perc)):
        temp = pd.DataFrame(df_perc.iloc[row_i]).value_counts().max()/len(df_perc.iloc[row_i])
        perc_list.append(temp)
    # add the column with percentage agreement to the df
    df_perc['perc_agreement'] = perc_list
    # calculate average percentage agreement
    perc_coefficient = round(np.mean(df_perc['perc_agreement']), 2)
    return df_perc, perc_coefficient


###
# 3. Bland-Altman plot and Pearson Correlation
###


# calculate the difference and mean of each row
def add_bland_altman_stat(combined_series, df_key_stat):
    temp_md = []
    temp_CI_low = []
    temp_CI_high = []

    for df_i in combined_series:
        # calculate difference and mean per row
        df_i['difference'] = abs(df_i['A']-df_i['B'])
        df_i['mean'] = ((df_i['A'] + df_i['B'])/2)

        # calculate total mean and CI of the hole combination_df and ad to temp column
        md = np.mean(df_i['difference'])
        sd = np.std(df_i['difference'])
        temp_md.append(round(md, 2))
        temp_CI_low.append(round((md - 1.96 * sd), 2))
        temp_CI_high.append(round((md + 1.96 * sd), 2))

    df_key_stat['md'] = temp_md
    df_key_stat['CI low'] = temp_CI_low
    df_key_stat['CI high'] = temp_CI_high

    return combined_series, df_key_stat



#Make a bland altman plot
def plot_bland_altman(name, mean, diff, md, CI_low, CI_high):
    #Set style


    # Plot mean to difference and add the 3 lines (Mean and 95% CI)
    plt.scatter(mean, diff)
    plt.axhline(md, color='gray', linestyle='--')
    plt.axhline(CI_low, color='gray', linestyle='--')
    plt.axhline(CI_high, color='gray', linestyle='--')

    # Make the plot presentable
    plt.title(f"Bland Altman Plot {name}", fontweight="bold")
    plt.xlabel("Means")
    plt.ylabel("Difference")
    plt.ylim(CI_low-2, CI_high+2)

    xOutPlot = np.min(mean) + (np.max(mean) - np.min(mean)) * 1.14

    # Add needed information as text
    plt.text(xOutPlot, CI_low,
             r'-1.96SD:' + "\n" + "%.2f" % CI_low,
            ha="center",
            va="center",
            )
    plt.text(xOutPlot, CI_high,
            r'+1.96SD:' + "\n" + "%.2f" % CI_high,
            ha="center",
            va="center",
            )
    plt.text(xOutPlot, md,
    r'Mean:' + "\n" + "%.2f" % md,
            ha="center",
            va="center",
            )
    plt.subplots_adjust(right=0.85)

    plt.show()


# Calculate the pearson correlation
def pearson_corr(combined_series, df_key_stat):
    temp_pearson = []
    for matrix_i in combined_series:
        # calculate pearson correlation and add to temp column
        pearson_corr = np.corrcoef(matrix_i['A'].to_numpy(), matrix_i['B'].to_numpy())
        temp_pearson.append(round(pearson_corr[0][1], 2))
    df_key_stat['pearson corr'] = temp_pearson
    return df_key_stat
