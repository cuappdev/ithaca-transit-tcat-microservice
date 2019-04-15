import csv
from subprocess import PIPE, Popen, STDOUT
import threading
import zipfile

GTFS_URL = 'https://s3.amazonaws.com/tcat-gtfs/tcat-ny-us.zip'
TCAT_NY_US = 'tcat-ny-us'
TEN_SECONDS = 10

gtfs_data = []

def fetch_gtfs(event):
  if gtfs_fetched():
    unzip_gtfs()
    extract_gtfs()
  threading.Timer(TEN_SECONDS, fetch_gtfs, [event]).start()

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

def gtfs_fetched():
  cmd = f'wget -N {GTFS_URL}'
  process = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
  output = process.stdout.read().decode('utf-8')
  return '200 OK' in output

def unzip_gtfs():
  zip_ref = zipfile.ZipFile(f'{TCAT_NY_US}.zip', 'r')
  zip_ref.extractall(TCAT_NY_US)
  zip_ref.close()

def get_gtfs_data():
  return gtfs_data
