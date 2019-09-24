## Ridley ( A modified Turtle Instagram Photo Downloader)

- It is for downloading your friend's photos and videos with your account.
- Your username and your password won't be stored.
- Whether or not you have two factor authentication in your Instagram account or not, this will still work.
- It uses `Selenium` and three different browsers which are `Chrome`, `Firefox` and `PhantomJS`
    - The driver is being asked at the beginning of the program.
    - If you want to see what happens -> use `Chrome` or `Firefox`
    - If you want to view the process in the background -> use `PhantomJs`

## Requirements

- Python 3.6+
- Selenium
- panda
- Chrome Driver for Selenium


## How to install and run

1. Download the source from Github
    - `git clone https://github.com/trevorbakker-uta/ridley.git`
    - `cd ridley`
2. Install requirements
	- `pip3 install -r requirements.txt`
3. Download the Chrome drivers.
    - Download and install `ChromeDriver`
            - [Download ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) 
            - Moved the ChromeDriver executable to /usr/bin/ (may need sudo)
`
## Usage

Simply call `python3 turtle_console.py -v True`

Choose the Chrome driver.

It will ask for your Instagram username and password for logging in. Then it will ask for a username which user's photo you want to download.

You can download:
- All user's photos
- Just the last stories you do not have
- Number of photos

## Advanced Usage

```
usage: turtle_console.py [-h] [-u] [-p] [-d] [-P] [-l] [-D] [-v]

Fetch all the lectures for a Instagram

optional arguments:
  -h, --help        show this help message and exit
  -u , --username   User username
  -p , --password   User password
  -d , --driver     Choosen Driver. [1]PantomJS [2]Chrome [3]Firefox
  -P , --path       The path for saving photos.
  -l , --list       List of Usernames
  -D , --download   Download choice. [1]Update(Default for list) [2]Full
  -v , --video      Download videos or not. [True]Download [False] Do Not
                    Download
  -s, --start       The start date to start saving posts
  -e, --end         The end date to start saving posts
```

## Config.Json File

This file can be used for saving login data and path for photos. Nothing is saved automatically to here even if you change the file.
- *driver*   : (*int*) Driver you want to use as default (*1* or *2* or *3*)
- *username* : (*string*) User's username
- *password* : (*string*) User's pass
- *path*     : (*string*) The path for saving photos. Default value is `photos`
    - Exp : `path/photos` or `../path/photos`
