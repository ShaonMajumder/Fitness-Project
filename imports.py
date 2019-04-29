from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout,ReadTimeout,ConnectionError
from tkinter import messagebox
from datetime import datetime,timedelta,date
from utilities.utility import *
from utilities.mysql_database import *
from tkinter import font

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
import tkinter.scrolledtext as tkscrolled
import tkinter as tk