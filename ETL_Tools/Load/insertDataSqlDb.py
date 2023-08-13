import mysql.connector
from mysql.connector import Error
import pandas as pd


def insert_data(connection, data):
    print('\tStarting to insert data into SQL db')
    # Start adding data
    
    """
    university_key, name, city, state, level, control, undergrad_program,\
    graduate_program, enrollment_profile, size_setting, basic, community_engagement
    """
    research_uni_vals = [(x['unitid'], x['name_x'], x['city'],
                          x['state'], x['level'], x['control'],
                          x['Undergraduate_Program'], x['Graduate_Program'],
                          x['Enrollment_Profile'], x['Undergraduate_Profile'],
                          x['Size_Setting'], x['Basic'],
                          x['Community_Engagement'])
                         for index, x in data.iterrows()]

    """
    university_key, serd, nonserd, pdnfrstaff, facnum, socsc_rsd,\
    hum_rsd, stem_rsd, oth_rsd, pct_full_time_grad, pct_research_space
    """
    uni_stats_vals = [(x['unitid'], x['serd'], x['nonserd'],
                       x['pdnfrstaff'], x['facnum'], x['socsc_rsd'],
                       x['hum_rsd'], x['stem_rsd'], x['oth_rsd'],
                       x['Percentile_full_time_grad'], x['Percentile_research_space'],)
                      for index, x in data.iterrows()]


    # Excute query
    execute_list_query(connection, pop_research_uni(), research_uni_vals)
    execute_list_query(connection, pop_uni_stats(), uni_stats_vals)

    print('\tDone!')


def pop_research_uni():
    sql = """
        INSERT INTO research_uni (university_key, name, city, state, level, control, undergrad_program,\
        graduate_program, enrollment_profile, undergrad_profile, size_setting, basic, community_engagement)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return sql


def pop_uni_stats():
    sql = """
            INSERT INTO uni_stats (university_key, serd, nonserd, pdnfrstaff, facnum, socsc_rsd,\
            hum_rsd, stem_rsd, oth_rsd, pct_full_time_grad, pct_research_space)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
    return sql


def execute_query(connection, query):
    # https://www.freecodecamp.org/news/connect-python-with-sql/
    cursor = connection.cursor()
    try:
        cursor.execute('USE research')
        cursor.execute(query)
        connection.commit()
        # print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def execute_list_query(connection, sql, val):
    # https://www.freecodecamp.org/news/connect-python-with-sql/
    cursor = connection.cursor()
    try:
        cursor.execute('USE research')
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def execute_scripts_from_file(connection, filename):
    cursor = connection.cursor()

    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:

        command = command.replace("\n", '')
        command = command.replace("\t", ' ')

        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cursor.execute(command)
        except Error as err:
            print(f"Error: '{err}'")
