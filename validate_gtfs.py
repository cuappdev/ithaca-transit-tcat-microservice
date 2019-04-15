import csv

def validate_gtfs():
    # Get all trip_id's from trips.txt
    trip_ids = []
    with open('./tcat-ny-us/trips.txt', 'r') as trips_txt:
      reader = csv.reader(trips_txt)
      # Skip the first row
      next(reader)
      for row in reader:
        trip_id = row[2]
        trip_ids.append(trip_id)

    # Get all trip_id's with a stop time by looking at stop_times.txt
    trip_ids_w_stop_times = set()
    with open('./tcat-ny-us/stop_times.txt', 'r') as stop_times_txt:
      reader = csv.reader(stop_times_txt)
      # Skip the first row
      next(reader)
      for row in reader:
        trip_id = row[0]
        trip_ids_w_stop_times.add(trip_id)

    missing_trip_ids = [trip_id for trip_id in trip_ids if trip_id not in trip_ids_w_stop_times]
    if len(missing_trip_ids) == 0:
        print('SUCCESS: All trip identifiers have stop times')
    else:
        print(f'ERROR: The following trip identifiers are missing stop times.\n{missing_trip_ids}')


if __name__ == '__main__':
    validate_gtfs()
