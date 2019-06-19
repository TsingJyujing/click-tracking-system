# Click Tracking System (Developing)

Actually, this is a click tracking system, actually, it looks like a short url system, it will log every visit,
and you can attach information (in JSON format) while generate link.
So there're maybe 2 different short point to same url but have different meta data.

This project is developed for ApacheCN to tracking the user behaviors on viewing and clicking.

## Quick Start

### Start with Docker (Strongly Recommend!)

#### Prepare Your Configure

There're 2 files you should prepare for start your system, the most important is `config.py`, please follow the comment to write your own config file.
Second is `token.txt`, of course, if you'd changed the `token_valid` function in `config.py`, 
maybe this file is not necessary anymore and you may prepare another file.

#### Create a Superuser Account

```bash
docker run -it -p 8000:80 -v {Your Data Dir}:/data \
    tsingjyujing/click-tracking-system \
    /usr/bin/python3 docker_start.py --mode createsuperuser
```

#### Start Your Service

```bash
docker run -d -p 8000:80 -v {Your Data Dir}:/data tsingjyujing/click-tracking-system
```

### Setup by Python (For Debugging or Developing Usage)

```bash
pip3 install -r requirements.txt
python3 manager.py runserver 8000
```

## Configuration File

There're 2 parts to modify settings, first of all is:

### click_ts/settings.py

This Django native setting file, you can modify the Django related settings, like DEBUG or ALLOW_HOSTS options.
For more details, please ref this doc: [Django Settings](https://docs.djangoproject.com/en/2.2/ref/settings/)

### config.py

This Click Tracking System related settings like how to connect the MongoDB or Queue cleaning behaviors.
Please open this file and read the comments.

## APIs

Reading about [doc/interfaces.md](doc/interfaces.md) for more details.