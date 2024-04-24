import os

url_base = 'https://understat.com/match/'

data = './data'
html_dir = os.path.join(data, 'html')

os.makedirs(html_dir, exist_ok=True)
os.makedirs(data, exist_ok=True)

export_csv_file = os.path.join(data, 'End.csv')
