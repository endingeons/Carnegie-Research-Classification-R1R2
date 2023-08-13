import pandas as pd


# noinspection SpellCheckingInspection
def extract():
    # All CSV paths
    all_r1_path = '../Prepared_Data/cc_download_R1.csv'
    all_r2_path = '../Prepared_Data/cc_download_R2.csv'
    ccihe_path = '../Prepared_Data/CCIHE2021-PublicData.csv'
    rankings_path = '../Prepared_Data/rankings.csv'

    # Read all the files into pandas dataframes
    r1_df = pd.read_csv(all_r1_path)
    r2_df = pd.read_csv(all_r2_path)
    ccihe_df = pd.read_csv(ccihe_path)
    rankings_df = pd.read_csv(rankings_path)

    # Remove last column in dataframe
    r1_df = r1_df[r1_df.columns[:-1]]
    r2_df = r2_df[r2_df.columns[:-1]]

    return r1_df, r2_df, ccihe_df, rankings_df
