# whereisme

a simple Python server whose only job is to show a location and timestamp on a webpage

## Install

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

none of this has been thoroughly tested for security vulnerabilities, so if you make this public facing at any level it is at yr own risk!

example caddy config:

```Caddyfile
your.website.abc {
        reverse_proxy :13856
}
```

with a userrname and password to view the site:

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
