# Loading of training data. (data source: www.footbal-data.co.uk)
#
# Data is stored in csv files in a directory per country. Each file has a fixed
# format like this: country_league_yy_yy.csv (e.g. be_jupiler_league_16_17.csv)
#
# Data encoding:
# Season: yy_yy (e.g 95_96)
# Country: country code (e.g. be)
# League: lower_case (e.g. jupiler_league)

import os
import os.path
import pandas as pd

DATA_ROOT = 'data'
CURRENT_YEAR = 16
COUNTRY_CODES = ['be', 'nl']
LEAGUES = {'be': ['jupiler_league'],
           'nl': ['eredivisie'],
           'fr': ['le_championnat', 'division_2']}


def _data_dir(country_code):
    return os.path.join(DATA_ROOT, country_code)


def _data_file_name(country_code, league, season):
    return "{}_{}_{}.csv".format(country_code, league, season)


def _data_file_path(country, league, season):
    return os.path.join(_data_dir(country),
            _data_file_name(country, league, season))


def _decode_season(season):
    split = season.split(' ')
    return int(split[0]), int(split[1])


def _encode_season(year):
    return '{:02d}_{:02d}'.format(year, year+1)


def load_season_data(country, league, season):
    """ Returns a data frame for country/league/season data. """
    path = _data_file_path(country, league, _encode_season(season))
    with open(path, 'r') as csv_file:
        return pd.read_csv(csv_file)


def load_country_data_for_all_leagues(country, season): 
    """ Returns a map with key the league and as value a data frame with the
        season data. """
    data = {}
    for league in LEAGUES[country]:
        data[league] = load_season_data(country, league, season) 
    return data


def load_country_data_for_league_data_range(country, league, start_year,
        end_year=CURRENT_YEAR):
    """ Returns a list with all data for a league in chronological order from
        start year till end year. """
    data = []
    for year in range(start_year, end_year+1):
        data.append(load_season_data(country, league, year))
    return data
