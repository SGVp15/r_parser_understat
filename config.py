start_game = 21829  # с какого номера скачать матчи
end_game = 21850  # по какой включительно









import os

url_base = 'https://understat.com/match/'

data = './data'
html_dir = os.path.join(data, 'html')

os.makedirs(html_dir, exist_ok=True)
os.makedirs(data, exist_ok=True)

export_csv_file = os.path.join(data, 'End.csv')
