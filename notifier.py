import json
import random
import sys
import time
import traceback
from datetime import datetime

import telegram

import api

with open("secrets/telegram.json") as f:
    telegram_secrets = json.load(f)


def prepare_html_content(text):
    return text.replace('<p>', '').replace('</p>', '').replace('<br />', '\n')


def format_deliv(deliv):
    msg = []
    msg.append(f'📭 <b>[{deliv["codi_asg"]}]</b>')
    msg.append('')
    msg.append(f'<u>{prepare_html_content(deliv["titol"])}</u>')
    msg.append('')

    if deliv['comentaris']:
        msg.append(prepare_html_content(deliv['comentaris']))
        msg.append('')

    msg.append(f'<i>Due: {datetime.fromisoformat(deliv["data_limit"])}</i>')

    return "\n".join(msg)


def format_ann(ann):
    msg = []
    msg.append(f'📢 <b>[{ann["codi_assig"]}]</b>')
    msg.append('')
    msg.append(f'<u>{prepare_html_content(ann["titol"])}</u>')
    msg.append('')

    if ann['text']:
        msg.append(prepare_html_content(ann['text']))
        msg.append('')

    for att in ann['adjunts']:
        msg.append(f'▶ <a href="{att["url"]}">{att["nom"]}</a>')

    return "\n".join(msg)


def poll():
    bot = telegram.Bot(telegram_secrets['bot_token'])
    token = api.Token.from_file('secrets/token.json')

    known_delivs = set()
    known_anns = set()

    for ann in api.get_announcements(token)['results']:
        ann_id = ann['id']
        known_anns.add(ann_id)

    for deliv in api.get_deliverables(token)['results']:
        deliv_id = deliv['codi_asg'] + '@' + deliv['data_inici'] + '@' + deliv['titol']
        known_delivs.add(deliv_id)

    while True:
        try:
            for ann in api.get_announcements(token)['results']:
                ann_id = ann['id']
                if ann_id not in known_anns:
                    bot.send_message(telegram_secrets['chat_id'], format_ann(
                        ann), disable_web_page_preview=True, parse_mode='html')
                    known_anns.add(ann_id)
            time.sleep(60)

            for deliv in api.get_deliverables(token)['results']:
                deliv_id = deliv['codi_asg'] + '@' + deliv['data_inici'] + '@' + deliv['titol']
                if deliv_id not in known_delivs:
                    bot.send_message(telegram_secrets['chat_id'], format_deliv(
                        deliv), disable_web_page_preview=True, parse_mode='html')
                    known_delivs.add(deliv_id)
            time.sleep(60)
        except:
            print(f'{datetime.now()}: Error', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            time.sleep(60)


if __name__ == '__main__':
    poll()
