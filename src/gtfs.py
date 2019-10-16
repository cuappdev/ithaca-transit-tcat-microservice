import csv

TCAT_NY_US = "tcat-ny-us"
TEN_SECONDS = 10

gtfs_data = []
gtfs_feed_info = {}


def fetch_gtfs(event):
    extract_gtfs()


def extract_gtfs():
    global gtfs_data
    with open(f"{TCAT_NY_US}/routes.txt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        column_names = next(csv_reader)
        for row in csv_reader:
            route = {}
            for index, column in enumerate(column_names):
                route[column] = row[index]
                gtfs_data.append(route)


def get_gtfs_feed_info():
    global gtfs_feed_info
    with open(f"{TCAT_NY_US}/feed_info.txt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        column_names = next(csv_reader)
        for row in csv_reader:
            for index, column in enumerate(column_names):
                if column in ["feed_start_date", "feed_end_date", "feed_version"]:
                    gtfs_feed_info[column] = row[index]
    return gtfs_feed_info


def get_gtfs_data():
    return gtfs_data
