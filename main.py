import asyncio
import csv
import json
import os
import re

import aiofiles
import aiohttp

from config import url_base, export_csv_file, html_dir, START_GAME, END_GAME, DOWNLOAD_SITES, \
    DELETE_HTML_FILES, COLUMNS_EXCEL


def parsing(s: str):
    result = re.findall(r"var rostersData	= JSON\.parse\('(.*)'\)", s)
    if not result:
        return ''
    s = result[0]
    match = str_x_to_dict(s)
    return match


def str_x_to_dict(s: str) -> dict:
    s = bytes(s, 'UTF-8')
    s = s.decode('unicode-escape').encode('latin1').decode('utf-8')
    d = json.loads(s)
    return d


def read_html_file(file_name: str):
    try:
        with open(file_name, encoding='utf-8') as f:
            s = f.read()
            return s
    except FileNotFoundError:
        return ''


async def download_sites(start, end):
    async with aiohttp.ClientSession() as session:
        for i in range(start, end + 1):
            url = url_base + str(i)
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    async with aiofiles.open(os.path.join(html_dir, f'{i}.html'), 'wb') as f:
                        await f.write(content)
                    print(f'Downloaded [ {i} ]')
                else:
                    print(f'Download [ {i} ]\t[Error]')


def del_files(start_game, end_game):
    for file_name in range(start_game, end_game + 1):
        try:
            os.remove(os.path.join(html_dir, f'{file_name}.html'))
        except FileNotFoundError:
            pass


def create_final_csv_file(start_game, end_game):
    with open(export_csv_file, mode='w', encoding='utf-8', newline='') as f:
        is_write_header = False
        for match_id in range(start_game, end_game + 1):
            match: dict = parsing(read_html_file(os.path.join(html_dir, f'{match_id}.html')))
            if type(match) is not dict or not match:
                print(f'[Error]\t{match_id}')
                continue
            for a_h in match.keys():
                for num in match.get(a_h).keys():
                    m = match[a_h][num]
                    m['match_id'] = match_id

                    w = csv.DictWriter(f, COLUMNS_EXCEL, delimiter=";")
                    if not is_write_header:
                        w.writeheader()
                        is_write_header = True
                    s = ''
                    for k in COLUMNS_EXCEL:
                        s += f'{m.get(k)};'
                    s += '\n'
                    s = s.replace('.', ',')
                    f.write(s)
            print(f'[OK]\t{match_id}')


if __name__ == '__main__':
    if DOWNLOAD_SITES:
        asyncio.run(download_sites(START_GAME, END_GAME))
    create_final_csv_file(START_GAME, END_GAME)
    if DELETE_HTML_FILES:
        del_files(START_GAME, END_GAME)
