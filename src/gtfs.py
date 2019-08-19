import csv
from subprocess import PIPE, Popen, STDOUT
import datetime
import threading
import zipfile

TCAT_NY_US = 'tcat-ny-us'
TEN_SECONDS = 10

gtfs_data = []
date_updated = None

def fetch_gtfs(event):
  extract_gtfs()

def extract_gtfs():
  global gtfs_data
  with open(f'{TCAT_NY_US}/routes.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    column_names = next(csv_reader)
    for row in csv_reader:
      route = {}
      for index, column in enumerate(column_names):
        route[column] = row[index]
      gtfs_data.append(route)

def get_gtfs_date_updated():
  return date_updated

def get_gtfs_data():
  return gtfs_data
