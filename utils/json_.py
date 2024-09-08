import json

from openpyxl import Workbook


def json_decode_x22(s) -> str:
    out = s.encode('utf8').decode('unicode_escape')
    return out


def json_to_xlsx(json_file, xlsx_file):
    """
    Конвертирует JSON файл в XLSX файл.

    Args:
      json_file (str): Путь к JSON файлу.
      xlsx_file (str): Путь к создаваемому XLSX файлу.
    """

    with open(json_file, 'r') as f:
        d = json_decode_x22(f.read())
        # print(d)
        datas = json.loads(d)
        # print(data)
        headers = datas[0].keys()
        print(headers)
        for data in datas:
            for key, value in data.items():
                if isinstance(value, (float, str)):
                    data[key] = str(value).replace(".", ",")

        data = datas

        workbook = Workbook()
        sheet = workbook.active

        # Записываем заголовки, если это список словарей
        if isinstance(data[0], dict):
            headers = list(data[0].keys())
            sheet.append(headers)

        # Записываем данные
        for row in data:
            if isinstance(row, dict):
                sheet.append(list(row.values()))
            else:
                sheet.append(row)

        workbook.save(xlsx_file)
