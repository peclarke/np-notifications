# Neptune's Pride Notifications

NP Notifications is a python notification tool used for sending you text messages when certain conditions are met. Initially, the main condition is if a new,
moving, enemy fleet has entered your scanning range. 

## Installation

Firstly, get your username, password, your user ID, game ID (url), and game API key from your Neptune's Pride game.
Next, you will need to create a Firebase account with Firestore. There must exist a "fleets" table in this database. 
Next, you will need to create a Twilio account in order send text messages.

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip3 install -r requirements.txt
```

Create a .env file with the following fields:
```bash
USERNAME=np_username
PASSWORD=np_password

CURRENT_GAME_ID=game_id
API_VERSION=0.1
API_KEY=api_key

TWILIO_AUTH=twilio_auth
TWILIO_SID=twilio_sid
TWILIO_PH=given_twilio_phone_number
NOTIF_PH=your_phone_number
```

## Usage

You can run this locally by uncommenting the debug statements in main.py. This will allow flask to run and setup the webserver.
The `check.py` file handles all checks. So running the `begin_check()` function there will scan your area and text you if a ship is approaching and your .env is
setup correctly.

In order to get this to run constantly, I highly recommending uploading the project to a Google Cloud Platform App Engine instance.
Make sure that the Google Cloud Scheduling system is enabled for this to constantly update you. To change the custom check time, check `cron.yaml`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
