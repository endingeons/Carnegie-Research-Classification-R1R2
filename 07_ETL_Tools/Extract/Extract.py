import pandas as pd


# noinspection SpellCheckingInspection
def extract():
    # All CSV paths
    all_r1_path = '../../2. Prepared Data/cc_download_R1.csv'
    all_r2_path = '../../2. Prepared Data/cc_download_R2.csv'
    ccihe_path = '../../2. Prepared Data/CCIHE2021-PublicData.csv'
    rankings_path = '../../2. Prepared Data/rankings.csv'

    # Read all the files into pandas dataframes
    r1_df = pd.read_csv(all_r1_path)
    r2_df = pd.read_csv(all_r2_path)
    ccihe_df = pd.read_csv(ccihe_path)
    rankings_df = pd.read_csv(rankings_path)

    return r1_df, r2_df, ccihe_df, rankings_df
