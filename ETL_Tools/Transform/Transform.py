from ETL_Tools.Extract.Extract import extract
import pandas as pd
import re


def drop_fields(r1_df, r2_df, ccihe_df, rankings_df):
    CCIHE_KEYS_SAVE = ['unitid', 'name', 'serd', 'nonserd', 'pdnfrstaff', 'facnum', 'hum_rsd', 'socsc_rsd', 'stem_rsd',
                       'oth_rsd']

    pd.set_option("max_colwidth", 35)
    # print(r1_df.keys())
    # print(r2_df.keys())
    # print(ccihe_df.keys())
    # print(rankings_df.keys())

    ccihe_df.drop(columns=[x for x in ccihe_df.keys() if x not in CCIHE_KEYS_SAVE], inplace=True)
    rankings_df.drop(columns=['Rank_earned_doct', 'Percentile_earned_doct',
                              'Rank_full_time_grad', 'Rank_tot_rd',
                              'Percentile_tot_rd', 'Rank_research_space'], inplace=True)

    return r1_df, r2_df, ccihe_df, rankings_df


def combine_r1_r2_data(r1_df, r2_df):
    return pd.concat([r1_df, r2_df], axis=0, keys=['R1', 'R2']).reset_index(drop=True). \
        rename(columns={'level_0': 'research_level'})


def combine_university_names(r1_r2_df, rankings_df):
    pd.set_option('display.max_colwidth', None)
    names_r1_r2 = r1_r2_df.name
    indices_rankings = []
    indices_remove = []

    stopword_list = ['the', 'of', 'at', 'in']

    # Replace abbreviations for college and university
    rankings_df.Institution = [v.replace('C.', 'College'). \
                                   replace('U.', 'University') for v in rankings_df.Institution]

    # Remove ',' in the name
    rankings_df.Institution = rankings_df.Institution.str.replace(', ', ' ')

    # Handle Rutgers Naming and SUNY school naming
    rankings_df.Institution = rankings_df.Institution.str.replace('-The State University New Jersey',
                                                                  ' University').replace('SUNY, ', '')

    # Remove all designated stop words
    for stopword in stopword_list:
        pattern = re.compile('\A{}[ ]+|[\s]{}[\s]+|[\s]{}$'.format(stopword, stopword, stopword), re.IGNORECASE)
        names_r1_r2 = [pattern.sub(' ', name) for name in names_r1_r2]
        rankings_df.Institution = [pattern.sub(' ', name) for name in rankings_df.Institution]

    # Remove the dashes in the names
    names_r1_r2 = [re.sub('-', ' ', name) for name in names_r1_r2]
    rankings_df.Institution = [re.sub('-', ' ', name) for name in rankings_df.Institution]

    # Handle the A & M / A & T name
    rankings_df.Institution = [re.sub('A&M', 'A & M', name) for name in rankings_df.Institution]
    rankings_df.Institution = [re.sub('Agricultural and Technical', 'A & T', name) for name in rankings_df.Institution]

    # Clean up majority of remaining names that list 'Main Campus' or 'Campus' in the name
    rankings_df.Institution = rankings_df.Institution.str.replace('Main Campus', '').replace('Campus', '')
    names_r1_r2 = [name.replace('Main Campus', '').replace('Campus', '') for name in names_r1_r2]

    # Replace 'St' with 'Saint'
    rankings_df.Institution = rankings_df.Institution.str.replace(' St ', ' Saint ')
    names_r1_r2 = [name.replace(' St ', ' Saint ') for name in names_r1_r2]

    # Remove SUNY from the name
    rankings_df.Institution = rankings_df.Institution.str.replace('SUNY ', '')
    names_r1_r2 = [name.replace('SUNY ', '') for name in names_r1_r2]

    # Delete any trailing or leading spaces
    names_r1_r2 = [re.sub('^[ ]+|[ ]+$', '', name) for name in names_r1_r2]
    rankings_df.Institution = [re.sub('^[ ]+|[ ]+$', '', name) for name in rankings_df.Institution]

    # Delete any duplicate spaces
    names_r1_r2 = [re.sub('[ ]{2,}', ' ', name) for name in names_r1_r2]
    rankings_df.Institution = [re.sub('[ ]{2,}', ' ', name) for name in rankings_df.Institution]

    # [print(name) for name in rankings_df.Institution]

    # Hard coding the remaining names
    hardcoded_map = {'CUNY Graduate School and University Center': 'CUNY Graduate Center',
                     'Louisiana State University and Agricultural & Mechanical College': 'Louisiana State University',
                     'North Carolina State University Raleigh': 'North Carolina State University',
                     'Rutgers University New Brunswick': 'Rutgers State University New Jersey New Brunswick',
                     'SUNY Albany': 'SUNY University Albany',
                     'Tulane University Louisiana': 'Tulane University',
                     'University Colorado Denver/Anschutz Medical': 'University Colorado Anschutz Medical Campus',
                     'Air Force Institute Technology Graduate School Engineering & Management': 'Air Force Institute Technology',
                     'Florida Agricultural and Mechanical University': 'Florida A & M University',
                     'Rutgers University Camden': 'Rutgers State University New Jersey Camden',
                     'Rutgers University Newark': 'Rutgers State University New Jersey Newark',
                     'Albany': 'University Albany',
                     'Pennsylvania State University': 'Pennsylvania State University University Park and Hershey '
                                                      'Medical Center',
                     'University Alabama': 'University Alabama Tuscaloosa',
                     'University Arkansas': 'University Arkansas Fayetteville',
                     'University North Texas': 'University North Texas Denton'
                     }
    # Loop through all r1_r2 names and find matches to the rankings df
    for idx, name in enumerate(names_r1_r2):
        any_match = rankings_df.Institution == name
        idx_match = [i for i, x in enumerate(any_match) if x]
        if len(idx_match) == 1:  # name exists
            indices_rankings = add_to_list(indices_rankings, idx_match[0])
        else:  # name doesn't exist or too many matches, try to map it to hardcoded correction list
            print('Found {} matches for {}'.format(len(idx_match), name))
            print('\tTrying to map to hardcoded correction list...')
            if name in hardcoded_map.keys() and any(rankings_df.Institution.str.contains(hardcoded_map[name])):
                any_match = rankings_df.Institution == hardcoded_map[name]
                idx_match = [i for i, x in enumerate(any_match) if x][0]
                indices_rankings = add_to_list(indices_rankings, idx_match)
                print('\tFound match!')
            else:  # name really doesn't exist, mark index for removal
                indices_remove = add_to_list(indices_remove, idx)
                print('\tNo match found: {}'.format(name))

    print('{} of {} mapped'.format(len(indices_rankings), len(names_r1_r2)))

    rankings_df_filtered = rankings_df.iloc[indices_rankings].reset_index(drop=True)
    print('New length of rankings_df is: {}'.format(len(rankings_df_filtered)))
    print('Length of r1_r2_df is: {}'.format(len(r1_r2_df)))

    # Add the UID to the rankings_df
    rankings_df_filtered['unitid'] = r1_r2_df.unitid

    return rankings_df_filtered


def join_all_tables(r1_r2_df, ccihe_df, rankings_df):
    all_tables = [r1_r2_df, ccihe_df, rankings_df]
    [print(len(x)) for x in all_tables]
    final_df = pd.merge(ccihe_df, rankings_df, on='unitid')
    final_df = pd.merge(final_df, r1_r2_df, on='unitid')

    return final_df


def add_to_list(mylist, value):
    if mylist:
        mylist.append(value)
    else:
        mylist = [value]
    return mylist


def clean_keys(df):
    # Clean up spaces and unexpected characters
    keys_clean = {key: clean_strings(key) for key in df.keys()}
    return df.rename(keys_clean, axis=1)


def clean_data(df):
    print('Placeholder')


def min_max_normalization(df):
    print('Placeholder')


def clean_strings(input_str):
    # Replace hashtags, ampersands, spaces with a single underscore
    input_str = re.sub('[#& ]+', '_', input_str)
    return input_str
