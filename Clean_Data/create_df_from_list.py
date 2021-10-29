import pandas as pd

# Takes a dataframe and a column with entries as lists and returns another dataframe
# That dataframe is split into new columns for entires in the list

def create_df_from_list(df, col_name):
    # Takes a column of lists from a dataframe
    # Returns a new dataframe with new columns the length of the lists

    temp_df = df[col_name].apply(pd.Series)
    temp_df = temp_df.rename(columns = lambda x: col_name + '_' + str(x))
    new_df = pd.concat([df, temp_df], axis=1)
    return new_df
