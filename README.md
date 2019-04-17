# ithaca-transit-live-tracking
Microservice for Ithaca Transit that handles:

  * Alerts
  * Bus Stops
  * Fetching GTFS data
  * Live tracking
  * Posting tweets on Twitter

Note that this microservice is only accessed by `ithaca-transit-backend` and is not a public API.

# Setup

If running for the first time, run:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make sure to also create your `.env` file by running:
```
cp env.template .env
```

Environment variable values can be found by asking a member of Cornell AppDev.

# Run

To run the app, just do:

```
python app.py
```

# Endpoints

# **/alerts** • GET

**Description:** Return a list of official TCAT alerts/messages. A list should be included in the app, and periodically updated every so often. All fields are optional.
The date, time, and daysOfWeek fields can specify an alert that takes place for example from 10 pm March 4 (fromDate) to 12 pm April 10 (toDate) on Weekdays (daysOfWeek) from 1 pm (fromTime) to 11 pm (toTime).

## Returns: [Alert]

*class* Alert

| **Name**        | **Type**                                       | **Description**                                                                                                                                                                                 |
| --------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id              | Int                                            | The ID number of the alert.                                                                                                                                                                     |
| message         | String                                         | The message of the alert.                                                                                                                                                                       |
| fromDate        | String                                         | The first date that the alert begins taking effect.  UTC-formatted date string (e.g. “2018-04-10T04:00:00.000Z”)                                                                                |
| toDate          | String                                         | The last date that the alert begins taking effect.  UTC-formatted date string (e.g. “2018-04-10T04:00:00.000Z”)                                                                                 |
| fromTime        | String                                         | The start time during the date range that the alert is in effect.  UTC-formatted date string (e.g. “2018-04-10T04:00:00.000Z”)                                                                  |
| toTime          | String                                         | The start time during the date range that the alert is in effect.  UTC-formatted date string (e.g. “2018-04-10T04:00:00.000Z”)                                                                  |
| priority        | Int                                            | Priority of the alert, from 0 (highest) to 3 (lowest).  Potential Return Values: [0, 1, 2, 3]                                                                                                   |
| daysOfWeek      | String                                         | A String enum representing a day of the week:   Potential Return Values: ["Every day”, “Weekend”, “Weekdays”, “Monday”, “Tuesday”, “Wednesday”, “Thursday”, “Friday”, “Saturday”, “Sunday”, “”] |
| routes          | [Int]                                          | A list of route numbers affected by alert.                                                                                                                                                      |
| signs           | [Int]                                          | A list of ??? affected by the alert.                                                                                                                                                            |
| channelMessages | [{  ChannelId: Int? Message: String?  }]       | A list of ChannelMessage objects. Improve description.                                                                                                                                          |
----------
# **/gtfs** • GET

**Description:** Fetches the GTFS data from TCAT about routes.

## Returns: [RouteInfo]

*class* **RouteInfo**

| **Name**         | **Type** |
| --------         | -------- |
| agency_id        | String   |
| route_id         | String   | 
| route_long_name  | String   |
| route_short_name | String   |
| route_type       | String   |

----------
# **/rtf** • GET

**Description:** Fetches the XML realtime feed data from TCAT and parses it into JSON.

## Returns: JSON object representing the realtime feed data from TCAT

----------
# **/stops** • GET

**Description:** Return a list of TCAT bus stops to show as a possible start / end location. A list should be included in the app, and periodically updated every so often.

**Note:** The type field refers to the type of place. We currently have two different possible types, `busStop` and `googlePlace`. Look at `/search` for further details.

## Returns: [BusStop]

*class* **BusStop**

| **Name** | **Type** | **Description**                           |
| -------- | -------- | ----------------------------------------- |
| name     | String   | The name of the bus stop.                 |
| lat      | Double   | The latitude coordinate of the bus stop.  |
| long     | Double   | The longitude coordinate of the bus stop. |
| type     | String   | This is just the string "busStop".        |

