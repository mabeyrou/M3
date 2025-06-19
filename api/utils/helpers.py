
def replace_by_dict(old_value, matching_values):
    for matching_value, values in matching_values.items():
        if old_value in values:
            return matching_value
    return old_value    

def detect_outliers(dataframe, column):
    Q1 = dataframe[column].quantile(0.25)
    Q3 = dataframe[column].quantile(0.75)
    IQR = Q3 - Q1

    return dataframe[(dataframe[column] >= (Q1 - 1.5 * IQR)) & 
                   (dataframe[column] <= (Q3 + 1.5 * IQR))]