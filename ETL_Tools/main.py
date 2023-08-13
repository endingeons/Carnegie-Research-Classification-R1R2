from ETL_Tools.Extract.Extract import *
from ETL_Tools.Transform.Transform import *
from ETL_Tools.Load.Load import *

print('START\n')

# Extract
print('Extracting data from CSV into dataframe')
r1_df, r2_df, ccihe_df, rankings_df = extract()
print('Done')
print('===============\n')

# Transform
print('Reformatting data')
r1_df = clean_keys(r1_df)
r2_df = clean_keys(r2_df)

r1_df, r2_df, ccihe_df, rankings_df = \
    drop_fields(r1_df, r2_df, ccihe_df, rankings_df)

r1_r2_df = combine_r1_r2_data(r1_df, r2_df)
rankings_df = combine_university_names(r1_r2_df, rankings_df)

final_table = join_all_tables(r1_r2_df, ccihe_df, rankings_df)

print('Done')
print('===============\n')

# Load
print('Saving data transformed data to folder')
save_data(r1_r2_df, rankings_df, ccihe_df, final_table)
print('Loading data into MySQL Database')
main_load(final_table)

print('Done....exiting')
print('===============\n')