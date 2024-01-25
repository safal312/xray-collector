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

from NamePrism import NamePrism

TOKEN="c790922c42f776cb"
infile = "all_people.csv"
outfile = "all_people_ethnicity.csv"
name_id = "name_id"
names = "person"

nprism = NamePrism(TOKEN, infile, outfile, name_id, names)
nprism.get_ethnicities()