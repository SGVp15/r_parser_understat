import os

START_GAME = 21829  # с какого номера скачать матчи
END_GAME = 21850  # по какой включительно

COLUMNS_EXCEL = ['player_id', 'team_id']

DOWNLOAD_SITES = False
DELETE_HTML_FILES = True

url_base = 'https://understat.com/match/'

data = './data'
html_dir = os.path.join(data, 'html')

os.makedirs(html_dir, exist_ok=True)
os.makedirs(data, exist_ok=True)

export_csv_file = os.path.join(data, 'End.csv')
