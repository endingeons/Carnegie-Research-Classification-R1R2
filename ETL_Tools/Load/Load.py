from datetime import datetime
from .insertDataSqlDb import *
from .connectToSqlDb import *
import pandas as pd
import json


def main_load(research_uni_data):
    # Connect to SQL Database
    connection = connect_local_sql_db()

    # Create database if it doesn't exist
    execute_scripts_from_file(connection, 'Load\\create_research_db.sql')

    # Insert Data
    insert_data(connection, research_uni_data)

    # Close connection
    close_local_sql_db(connection)


def save_data(r1_r2_df, rankings_df, ccihe_df, final_table):
    SAVE_PATH = '../Uploaded_Data/'
    TODAY_DATE = datetime.today().strftime('%Y%m%d')
    FILENAME1 = SAVE_PATH + TODAY_DATE + '_r1_r2.csv'
    FILENAME2 = SAVE_PATH + TODAY_DATE + '_rankings.csv'
    FILENAME3 = SAVE_PATH + TODAY_DATE + '_ccihe.csv'
    FILENAME4 = SAVE_PATH + TODAY_DATE + '_research_uni_data.csv'

    r1_r2_df.to_csv(FILENAME1, index=False)
    print('\tData saved to {}'.format(FILENAME1))

    rankings_df.to_csv(FILENAME2, index=False)
    print('\tData saved to {}'.format(FILENAME2))

    ccihe_df.to_csv(FILENAME3, index=False)
    print('\tData saved to {}'.format(FILENAME3))

    final_table.to_csv(FILENAME4, index=False)
    print('\tData saved to {}'.format(FILENAME4))





