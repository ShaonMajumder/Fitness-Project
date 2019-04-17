from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout,ReadTimeout,ConnectionError
from tkinter import messagebox
from utilities import utility as util
from utilities import mysql_database as mysql
from datetime import datetime,timedelta
import os
import re
import requests
import time
import random
import codecs
import json
import chardet
import winsound
import shutil
import string
import configparser
import tkinter