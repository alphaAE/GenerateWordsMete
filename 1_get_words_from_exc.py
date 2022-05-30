# 该工具用于从多张Excel中提取去重的中文关键字词字，并保存为csv
import csv

import pandas as pd
import jieba


def is_contains_chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def get_words_excel(excel_file):
    words_all = ''
    for sheet_name in excel_file.sheet_names:
        data = pd.read_excel(excel_file, sheet_name, header=None)
        # 展开二维表
        data = sum(data.values.tolist(), [])
        data = map(str, data)
        words_all += ','
        words_all += ','.join(data)

    words_out = list(set(jieba.cut_for_search(words_all)))
    words_out = [x for x in words_out if is_contains_chinese(x)]
    return words_out


def get_words_excel_list(excel_list):
    words_all = []
    for file in excel_list:
        words_all += get_words_excel(file)
    # 再次去重
    return list(set(words_all))


def list_to_csv(csv_path, save_list):
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows([i] for i in save_list)


if __name__ == '__main__':
    files = [
        pd.ExcelFile(r'../../DataSource/qi1.xlsx'),
        pd.ExcelFile(r'../../DataSource/qi2.xlsx')
    ]
    words = get_words_excel_list(files)
    print(words)
    print(len(words))
    list_to_csv('./1_words_exc.csv', words)
