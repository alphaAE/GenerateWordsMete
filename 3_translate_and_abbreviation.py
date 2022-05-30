from pygoogletranslation import Translator
from collections import Counter
import csv


def list_to_csv(csv_path, save_list):
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(save_list)


def translator_words(_words):
    print("翻译采用谷歌网页API，数据量过大，翻译时间较久，请耐心等待...")
    translator = Translator(service_url='translate.google.cn')
    _t = translator.translate(_words, dest='en')
    t_words = [i.text for i in _t]
    return t_words


def abbreviation_words(_words):
    _abb_words = []
    for word in _words:
        _word_list = word.split(' ')
        count = len(_word_list)

        if count == 1:
            _one_count = len(_word_list[0])
            if _one_count <= 7:
                _abb_words.append(_word_list[0].lower())
            else:
                _abb_words.append(_word_list[0].lower()[:4] + _word_list[0].lower()[-1])
        elif count == 2:
            _two_count = len(_word_list[1])
            if _two_count <= 6:
                _abb_words.append(_word_list[0].lower()[0] + _word_list[1].lower())
            else:
                _abb_words.append(_word_list[0].lower()[0] + _word_list[1].lower()[:4])
        else:
            _word = ''
            for w in _word_list:
                _word += w.lower()[0]
            _abb_words.append(_word)

    # 查重
    _abb_words_b = dict(Counter(_abb_words))
    _repeat = [key for key, value in _abb_words_b.items() if value > 1]
    print(_repeat)
    # 标记
    _abb_words = ['###' + i if i in _repeat else i for i in _abb_words]

    return _abb_words


if __name__ == '__main__':
    words = []
    with open("./2_words.csv", encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            words.append(row[0])
    print(words)

    en_words = translator_words(words)
    print(en_words)

    abb_words = abbreviation_words(en_words)
    print(abb_words)

    out_words = []
    for i in range(len(words)):
        out_words.append([words[i], en_words[i], abb_words[i]])

    list_to_csv('./3_out_words.csv', out_words)
