# Simple Twilio Whatsapp sender

A simple program to automate sending Whatsapp messages using Twilio.

- [Simple Twilio Whatsapp sender](#simple-twilio-whatsapp-sender)
  - [Installation](#installation)
    - [Dependencies](#dependencies)
  - [Set up](#set-up)
    - [1. Twilio credentials and Sender number](#1-twilio-credentials-and-sender-number)
    - [2. Approved template message](#2-approved-template-message)
    - [3. Recipients database](#3-recipients-database)
  - [Usage](#usage)
    - [Examples](#examples)
      - [Minimum example with defaults](#minimum-example-with-defaults)
      - [Specifying the cellphone column](#specifying-the-cellphone-column)
      - [Specifying placeholder values](#specifying-placeholder-values)
      - [Specifying different filepaths for inputs](#specifying-different-filepaths-for-inputs)

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

In order to send messages the program requires that you provide
1. [Twilio credentials](http://twil.io/secure) (i.e. Account SID and Auth token) and sender number,
2. an approved [template message](https://www.twilio.com/docs/whatsapp/tutorial/send-whatsapp-notification-messages-templates), and
3. a database of users to send the messages to.

By default, the program will look for these files in the `./inputs` subdirectory, using the filenames listed below.
```
inputs
├── recipients.csv
├── secret.json
└── template.txt
```

You can specify different filename/filepaths from these defaults (see [Usage](#usage)). **Note that this subdirectory and these files must be created by the user; details are provided in the following subsections.**

### 1. Twilio credentials and Sender number

You'll need the [Twilio Account SID and Auth token](http://twil.io/secure) so that the program can securely access your account resources. Both values can be found in your [Twilio Console](https://console.twilio.com/). You'll also need to provide the Whatsapp sender number, which can be found [here](https://www.twilio.com/console/sms/whatsapp/senders).
This information should be written in JSON format. By default, the program will look for this information in `./inputs/secret.json`. The information has to be written in JSON format, using the following structure:
```json
// ./inputs/secret.json
// info below is fake
{
    "account_sid": "fake0bd38058a4ebf3ca22f767273f07",
    "auth_token": "fake74f0eaf990cfdf37e0da70bee8f2",
    "sender_number": "12345678901"
}
```
**Note that the sender number must contain the country code _without_ the `+` sign.**

### 2. Approved template message

You can only send Whatsapp messages via Twilio using pre-approved [templates](https://www.twilio.com/docs/whatsapp/tutorial/send-whatsapp-notification-messages-templates). You can find all your pre-approved messages [here](https://www.twilio.com/console/sms/whatsapp/templates).
Copy the template message text you want to use and paste it in a text file. By default, the program will look for this information in `./inputs/template.txt`. The file must be something like:
```
Hello {{1}}, my name is Han-Tyumi. I am a chatbot.
```
**The message must be copied exactly as it is shown in the message text column. Make sure not to add any new lines above or below the text.**


### 3. Recipients database

Lastly, you'll need a database of users which will receive the message. By default, the program will look for this information in `./inputs/twilio-db.csv`. The database must be a CSV file, with a structure similar to the example below.
```
| index | cellphone   | name  | country |
|-------|-------------|-------|---------|
| 1     | 11234567890 | Alice | USA     |
| 2     | 56987654321 | Bob   | Chile   |
```
The bare minimum that the database must have is a column with cellphone numbers.
By default, the program will look for this information in a column named `cellphone`, but any name can be specified; see [Usage](#usage) below.
Note that this column has to have numbers that include country code _without_ the `+` sign: Alice has a country code of `1` (i.e. USA), and Bob has a country code of `56` (i.e. Chile).

Additional columns are optional, and can be used to fill placeholder values in the [Twilio template](https://www.twilio.com/docs/whatsapp/tutorial/send-whatsapp-notification-messages-templates).  See [Usage](#usage) for information about how to use these additional columns.
## Usage

Make sure you have gone through the [installation](#installation) and [set up](#set-up) processes. General usage is described in the help file, which we print here:

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

### Examples

Examples below assume a simple starting point and then grow in complexity. We assume a recipient database that is
```
| index | cellphone   | name  | country |
|-------|-------------|-------|---------|
| 1     | 11234567890 | Alice | USA     |
| 2     | 56987654321 | Bob   | Chile   |
```
and a template text that reads
```
Hello, my name is Han-Tyumi. I am a chatbot.
```
All filenames and filepaths are the program's defaults,
```
inputs
├── recipients.csv
├── secret.json
└── template.txt
```

#### Minimum example with defaults

Assuming you've [set up](#set-up) everything using the default filepaths, and that your template message doesn't require any inputs (i.e. it doesn't have any placeholder values), then the program can be executed simply with
```bash
python sender.py
```

#### Specifying the cellphone column

Suppose now that the column containing cellphone numbers is named something different from `cellphone`, like `phonez`. We can specify the name of the cellphone numbers explicitely with
```bash
python sender.py -n phonez
```

#### Specifying placeholder values

Suppose now that your template message is the following:
```
Hello {{1}} from {{2}}, my name is Han-Tyumi. I am a chatbot.
```
This template message requires that we specify two columns to fill the information in the placeholders.
Suppose your dataset in `./inputs/recipients.csv` is something like
```
| index | cellphone   | name  | country |
|-------|-------------|-------|---------|
| 1     | 11234567890 | Alice | USA     |
| 2     | 56987654321 | Bob   | Chile   |
```
We need to tell the program that the first placeholder value is to be taken from the column named `name`, and the second one from `country`. We do this by using the `-f` flag (`--fill-cols`), and we give the names of the columns sequentially (i.e. the order matters):
```bash
python sender.py -f name country
```

#### Specifying different filepaths for inputs

Suppose that you want to try a different template text that is located in `./template2.txt`. This template text reads
```
Hello {{1}}, my name is Han-Tyumi. I am a chatbot.
```
The recipients database is the same as in the example above.
We run the program with the `-f` flag to fill the placeholder value with the `name` column, and we specify the location of the template text with the `-t` flag:
```bash
python sender.py -f name -t template2.txt
```