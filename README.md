#Pi Code

## Setup

* ### Dependencies
* [Python 2.7](https://www.python.org/download/releases/2.7/)
* *virtualenv* - `pip install virtualenv`

* ### First Time Setup
* `git clone https://github.com/dabba-fyp/dabba-pi-server`
* `cd dabba-pi-server`
* `virtualenv venv`
* `source venv/bin/activate`
* `sudo pip install -r requirements.txt`


* ### Running The App
* `python application.py` 

* #### GCP API
* Enable the vision API
* Create a bucket
* Download the config json from GCP
* Run the following command
* `export GOOGLE_APPLICATION_CREDENTIALS=[path-to-config]`

# Telegram Code

* You need a Telegram App to use this module

### Running The App
* `python telegram_main.py`

### Sending Asynch Messages

You can send asynchronous messages to any user in the Telegram App.

<b>Note:</b> The method will fail if the user data is not present in `telegram_db` document.<br>
<b>Note:</b> Make sure the telegram_api file is in the same directory.

```
from send_asynch_messages import send_message
send_message([USER_NAME], [MESSAGE])
```

  