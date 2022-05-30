# 合并csv并去重
import csv

if __name__ == '__main__':
    words_exc = []
    with open("./1_words_exc.csv", encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            words_exc.append(row[0])

    words_txt = []
    with open("./1_words_txt.csv", encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            words_txt.append(row[0])

    words_all = []
    words_all += words_exc
    words_all += words_txt
    words_all = list(set(words_all))

    print(words_all)
    print(len(words_all))

    with open('./1_words.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows([i] for i in words_all)
