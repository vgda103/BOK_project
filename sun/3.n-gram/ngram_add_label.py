import os
import json
import csv
import re

def txt_to_json():
    textpath = './tokens/'
    file_lists = os.listdir(textpath)
    dir = './reportjson/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    result_dict = {}
    for filename in file_lists:
        with open(os.path.join(textpath, filename), 'r', encoding='utf-8') as f:
            data = f.read()
            data = eval(data)
            result_dict[filename[:-4]] = data

    for key, value in result_dict.items():
        json_data = json.dumps({key: value}, ensure_ascii=False, indent=4)
        with open(dir + f'{key}.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)

    return print("JSON 파일로 변환 및 저장 완료")

def ngram():
    json_folder = './reportjson/'
    file_lists = os.listdir(json_folder)

    n_gram_json = './ngram/'
    if not os.path.exists(n_gram_json):
        os.makedirs(n_gram_json)

    # Load CSV file for labeling
    label_dict = {}
    with open('call_rate_label.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            label_dict[row['month']] = row['polar']

    for filename in file_lists:
        with open(os.path.join(json_folder, filename), encoding='utf-8') as f:
            data = json.load(f)
            value_lists = data[filename[:-5]]
            for i in range(1, 6):
                gram_list = []
                for lists in value_lists:
                    grams = []
                    for x in range(0, len(lists)-i+1):
                        if lists[x:x+i] not in grams:
                            grams.append('_'.join(lists[x:x+i]))
                    gram_list.append(grams)
                data[f'{i}gram'] = gram_list           
            # Add labels
            match = re.search(r'\b[0-9]{4}\.[0-9]{1,2}\b', filename)
            if match:
                month = match.group(0)
                if len(month)==6:
                    ym = month.split('.')
                    ym[1] = '0' + ym[1]
                    year_month = '-'.join(ym)
                elif len(month)==7:
                    year_month = '-'.join(month.split('.')[:2])
                label = label_dict.get(year_month)
            if label is not None:
                data['label'] = label
            else:
                print(f"No label found for {year_month}")


            with open(os.path.join(n_gram_json, f'{filename[:-5]}_ngram.json'), 'w', encoding='utf-8') as j:
                json.dump(data, j, ensure_ascii=False, indent=4)
    return print('n-gram이 추가된 json 파일 저장완료')

txt_to_json()
ngram()