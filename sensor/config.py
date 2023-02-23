import pymongo
import pandas as pd 
import numpy as np 
import os
from dataclasses import dataclass
TARGET_COLUMN = "class"


class ENVIRONMENT_VARIABLE :
    mongo_db_url = os.getenv("MONGO_DB_URL")

env_var = ENVIRONMENT_VARIABLE()
mongo_clent = pymongo.MongoClient(env_var.mongo_db_url)

