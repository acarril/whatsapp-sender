import pandas as pd
from tqdm import tqdm
import argparse
from distutils.util import strtobool
import sys
from twilio.rest import Client
import json
from template_utils import custom_message_from_template
import re

class Zender:
    def __init__(
        self,
        recipients_filepath,
        secret_filepath,
        template_file,
        colnames:list
    ) -> None:
        self.colname_cellphone = colnames[0]
        self.colnames_fields = colnames[1:]
        self.template_text = ' '.join(template_file)
        self.secret_data = json.load(secret_filepath)
        self.client = Client(
            self.secret_data['account_sid'],
            self.secret_data['auth_token']
        )
        self.from_number = 'whatsapp:+' + self.secret_data['sender_number']
        self.recipients_data = self.read_recipients_data(recipients_filepath, self.colnames_fields)

    def send_messages(self, max_errors:int=10, sleep_time=1) -> None:
        df = self.recipients_data
        pbar = tqdm(df.iterrows(), total=df.shape[0])
        for i, row in pbar:
            # Progress bar info
            pbar.set_description(f"texting index {i}, {row[self.colname_cellphone]}")
            # Collect information to construct message
            student_idx = row['index']
            to_number = 'whatsapp:+' + str(row[self.colname_cellphone])
            col_rowvalues = row[self.colnames_fields]
            body_personalized = custom_message_from_template(self.template_text, col_rowvalues)
            # Send message
            try:
                msg = self.client.messages.create(
                    body=body_personalized,
                    from_=self.from_number,
                    to=to_number
                )
            except Exception as error:
                print(f'Error sending message to ID:{student_idx} with number {to_number};', error)
                continue

    def confirm_send(self) -> bool:
        est_time = round(self.recipients_data.shape[0]/240, ndigits=2)
        question = f'Send message to {self.recipients_data.shape[0]} recipients?'\
            f' Estimated time is approximately {est_time} minutes.'
        sys.stdout.write('%s [Y/n]\n' % question)
        while True:
            try:
                usr_input = input()
                usr_input = usr_input if usr_input != '' else 'y' # pressing 'return'
                return strtobool(usr_input)
            except ValueError:
                sys.stdout.write('Please respond with \'y\' or \'n\'.\n')

    @staticmethod
    def read_recipients_data(filepath, colnames_fields) -> pd.DataFrame:
        df = pd.read_csv(filepath)
        check = all(item in df.columns for item in colnames_fields)
        if check is True:
            return df
        else:
            raise KeyError(f'the database must include columns {colnames_fields}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r', '--recipients', 
        nargs='?', type=argparse.FileType('r', encoding='UTF-8'), 
        required=False, default='./inputs/recipients.csv'
    )
    parser.add_argument(
        '-s', '--secret', 
        nargs='?', type=argparse.FileType('r', encoding='UTF-8'), 
        required=False, default='./inputs/secret.json'
    )
    parser.add_argument(
        '-t', '--template', 
        nargs='?', type=argparse.FileType('r', encoding='UTF-8'), 
        required=False, default='./inputs/template.txt'
    )
    parser.add_argument(
        '-n', '--number-col', 
        nargs='?', type=ascii, 
        required=False, default='cellphone'
    )
    parser.add_argument(
        '-f', '--fill-cols', 
        nargs='*', type=ascii, 
        required=False, default=[]
    )
    args = parser.parse_args()
    cols = [args.number_col.strip("'")] + [x.strip("'") for x in args.fill_cols]
    sender = Zender(
        args.recipients.name,
        args.secret,
        args.template,
        cols
    )
    usr_confirm = sender.confirm_send()
    if usr_confirm:
        sender.send_messages()
    else:
        return

if __name__ == "__main__":
    main()
