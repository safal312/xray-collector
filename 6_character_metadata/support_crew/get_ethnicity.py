# c790922c42f776cb
# http://www.name-prism.com/api_token/eth/json/[API_token]/Barack%20Obama
import os
import re
import requests
import json
import asyncio
import pandas as pd
import pandas.io.common
from unidecode import unidecode
from ratelimit import limits, sleep_and_retry

# import NamePrism from the file in the parent directory
import sys
sys.path.append("..")
from NamePrism import NamePrism

# self.URL = "http://www.name-prism.com/api_token/eth/json/c790922c42f776cb/"
#         self.infile = "unique_names_movies_support_crew.csv"
#         self.outfile = "ethnicity_unique_names_movies_support_crew.csv"

TOKEN="c790922c42f776cb"
infile = "unique_names_movies_support_crew.csv"
outfile = "ethnicity_unique_names_movies_support_crew.csv"
name_id = "person_id"
names = "name"

nprism = NamePrism(TOKEN, infile, outfile, name_id, names)
nprism.get_ethnicities()