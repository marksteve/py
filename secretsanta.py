"""
secretsanta.py

NOTE: Requires EngageSpark account with credits

Usage:
    secretsanta.py < names.csv

    CSV of names should have the following columns:
    - name
    - number
    - wishlist

Environment Variables:
    ENGAGESPARK_API_KEY
    ENGAGESPARK_ORGANIZATION_ID
"""
import os
import sys

import pandas as pd
import requests


def send_sms(number, message):
    return requests.post(
        'https://start.engagespark.com/api/v1/messages/sms',
        headers={
            'Authorization': 'Token {}'.format(os.environ['ENGAGESPARK_API_KEY']),
        },
        json={
            'organization_id': os.environ['ENGAGESPARK_ORGANIZATION_ID'],
            'recipient_type': 'mobile_number',
            'mobile_numbers': [number],
            'message': message,
        },
    )


if __name__ == '__main__':
    df = pd.read_csv(sys.stdin, dtype=str)
    shuffled = df.sample(len(df))
    for i in range(len(shuffled)):
        drawer = shuffled.iloc[i]
        drew = shuffled.iloc[(i + 1) % len(shuffled)]
        message = 'Hi {}. You drew {}!'.format(drawer['name'], drew['name'])
        if type(drew['wishlist']) == str:
            message += "\n{}'s wishlist: {}".format(
                drew['name'], drew['wishlist'])
        resp = send_sms(drawer['number'], message)
        resp.raise_for_status()

