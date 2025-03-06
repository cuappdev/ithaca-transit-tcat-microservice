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
                if column in {"feed_start_date", "feed_end_date", "feed_version"}:
                    gtfs_feed_info[column] = row[index]
    return gtfs_feed_info


def get_gtfs_data():
    return gtfs_data


def validate_gtfs():
    # Get all trip_id's from trips.txt
    trip_ids = []
    with open("./tcat-ny-us/trips.txt", "r") as trips_txt:
        reader = csv.reader(trips_txt)
        # Skip the first row
        next(reader)
        for row in reader:
            trip_id = row[2]
            trip_ids.append(trip_id)

    # Get all trip_id's with a stop time by looking at stop_times.txt
    trip_ids_w_stop_times = set()
    with open("./tcat-ny-us/stop_times.txt", "r") as stop_times_txt:
        reader = csv.reader(stop_times_txt)
        # Skip the first row
        next(reader)
        for row in reader:
            trip_id = row[0]
            trip_ids_w_stop_times.add(trip_id)

    missing_trip_ids = [
        trip_id for trip_id in trip_ids if trip_id not in trip_ids_w_stop_times
    ]
    if len(missing_trip_ids) == 0:
        print("SUCCESS: All trip identifiers have stop times")
    else:
        print(
            f"ERROR: The following trip identifiers are missing stop times.\n{missing_trip_ids}"
        )
