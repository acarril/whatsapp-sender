# Simple Twilio Whatsapp sender

A simple program to automate sending Whatsapp messages using Twilio.

## Installation

1. Clone this repository and navigate to its direcotry.
2. Make sure you have Python 3.8.6 (see [.python-version](.python-version.txt))
3. As usual, it is recommended to create a virtual environment for the application. For example, by running
```bash
# create virtual environment (run only once)
python -m venv .venv
# activate environment (run only once per session)
source .venv/bin/activate
```

### Dependencies

Install all required modules in your environmnet by running
```sh
pip install -r requirements.txt
```

## Set up

In order to send messages the program requires
1. [Twilio credentials](http://twil.io/secure) (i.e. Account SID and Auth token),
2. an approved [template message](https://www.twilio.com/docs/whatsapp/tutorial/send-whatsapp-notification-messages-templates), and
3. a database of users to send the messages.

By default, the program will look for these files in `./inputs/`, using the filenames listed below. Note that this directory and these files must be created by the user.
```
inputs
├── recipients.csv
├── secret.json
└── template.txt
```

### 1 Twilio credentials and Sender number

You'll need the Twilio Account SID and Auth token so that the program can securely access your account resources. Both values can be found in your [Twilio Console](https://console.twilio.com/). You'll also need to provide the Whatsapp sender number, which can be found [here](https://www.twilio.com/console/sms/whatsapp/senders).

This information should be written in a JSON file (or any text file). By default, the program will look for this information in `./inputs/secret.json`. The file must have the following structure:
```json
// ./inputs/secret.json
// info below is fake
{
    "account_sid": "fake0bd38058a4ebf3ca22f767273f07",
    "auth_token": "fake74f0eaf990cfdf37e0da70bee8f2",
    "sender_number": "12345678901"
}
```
**Note that the sender number must contain the country code _without_ the `+` sign.** The information above is fake; use your own credentials and sender number.

### 2 Approved template message

You can only send Whatsapp messages via Twilio using pre-approved [templates](https://www.twilio.com/docs/whatsapp/tutorial/send-whatsapp-notification-messages-templates). You can find all your pre-approved messages [here](https://www.twilio.com/console/sms/whatsapp/templates).

Copy the template message text you want to use and paste it in a text file. By default, the program will look for this information in `./inputs/template.txt`. The file must be something like:
```
Hello {{1}}, my name is Han-Tyumi. I am a chatbot.
```
**The message must be copied exactly as it is shown in the message text column. Make sure not to add any new lines above or below the text.**


### 3 Recipients database

Lastly, you'll need a database of users which will receive the message. By default, the program will look for this information in `./inputs/twilio-db.csv`. The file must have the following structure:
```
| index | cellphone   | name  |
|-------|-------------|-------|
| 1     | 11234567890 | Alice |
| 2     | 56987654321 | Bob   |
```
Note that the `cellphone` column has to have numbers that include country code: Alice has a country code of `1` (i.e. USA), and Bob has a country code of `56` (i.e. Chile).


## Usage

```
usage: sender.py [-h] [-r [RECIPIENTS]] [-s [SECRET]] [-t [TEMPLATE]] [-n [NUMBER_COL]] [-f [FILL_COLS [FILL_COLS ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -r [RECIPIENTS], --recipients [RECIPIENTS]
  -s [SECRET], --secret [SECRET]
  -t [TEMPLATE], --template [TEMPLATE]
  -n [NUMBER_COL], --number-col [NUMBER_COL]
  -f [FILL_COLS [FILL_COLS ...]], --fill-cols [FILL_COLS [FILL_COLS ...]]
```