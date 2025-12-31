# whereisme

![screenshot of the coordinates, timestamp, and link](image.png)

a simple python server whose only job is to show a location and timestamp on a webpage

the page shows:

1. latitude, longitude
1. timestamp of last update in human readable format
1. link to the given coordinates on openstreetmap

the server listens for POST requests with an auth token and updates the page accordingly

only the most recent location is stored in memory; no data persists across runs

## what to use it for

- alternative to find my; use ios shortcuts or tasker or something to periodically update your phone's location
- keep track of where you parked your car or bike
- broadcast the location of your parade float
- play a sophisticated version of hide and seek that involves telling everyone where you're hiding
- tell a child that this website shows you where santa/the easter bunny/jerma985 is, they will believe you
- conduct a treasure hunt with only one treasure at a time
- get directions except without turn-by-turn steps or seeing your current location
- show off your two favorite words or phrases, along with a timestamp, and a link that won't work since it expects coordinates

## install

clone the repo and `cd` into it

make an `.env` file like:

```
GPS_POST_TOKEN="XaEnzCdD9a4CUWKwCRp7eEdwp7NT9tow7xNPm4QxtMeMM2iEhWNJfNp2P7gtaLzD"
LOCAL_TZ="Etc/UTC"
```

`GPS_POST_TOKEN` should probably be a 32+ character mixed-case alphanumeric string generated randomly by a program, not a human (definitely not AI)

[valid TZ identifiers here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

then choose your method:

### locally with Python

```sh
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
```

### docker compose

`docker compose up`

## usage

to set the location on the site:

```
curl -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer XaEnzCdD9a4CUWKwCRp7eEdwp7NT9tow7xNPm4QxtMeMM2iEhWNJfNp2P7gtaLzD" \
    -d '{"latitude":"12.345", "longitude": "98.765"}' \
    http://127.0.0.1:13856/
```

to see the location visit http://127.0.0.1:13856/

### publishing on web

none of this has been thoroughly tested for security vulnerabilities, so if you make this public facing at any level it is at yr own risk! and always use HTTPS and strong authentication methods!

example caddy config:

```Caddyfile
your.website.abc {
        reverse_proxy :13856
}
```

with a username and password to view the site:

```Caddyfile
your.website.abc {
        reverse_proxy :13856
        @get {
                method GET
        }

        basic_auth @get {
            example_username hashed_password
        }
}
```

use `caddy hash-password` for that one

## configuration

aside from the .env file you're gonna have to just edit the repo to make changes my dude sorry... if u want to change something like the port just make sure it's reflected in server.py, compose.yml, Dockerfile, and anywhere else it's relevant

## development

ideally `start-dev.sh` should get the debug server running, but it prob won't at the moment, so adapt it for yr needs
