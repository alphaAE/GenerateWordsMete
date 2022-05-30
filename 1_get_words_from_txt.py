# 该工具用于从多个txt提取去重的中文关键字词字，并保存为csv
import csv

import pandas as pd
import jieba


def is_contains_chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def get_words_txt(txt_file):
    words_out = ''
    with open(txt_file, 'r', encoding='utf-8') as file:
        words_out = list(set(jieba.cut_for_search(file.read())))
    words_out = [x for x in words_out if is_contains_chinese(x)]
    return words_out


def get_words_txt_list(txt_list):
    words_all = []
    for file in txt_list:
        words_all += get_words_txt(file)
    # 再次去重
    return list(set(words_all))


def list_to_csv(csv_path, save_list):
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows([i] for i in save_list)


if __name__ == '__main__':
    files = [r'./qx.txt']
    words = get_words_txt_list(files)
    print(words)
    print(len(words))
    list_to_csv('./1_words_txt.csv', words)
