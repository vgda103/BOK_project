import os
import json

# 토큰화된 텍스트 파일을 json 파일로 변환하여 저장
def txt_to_json():
    textpath = './reporttxt/'
    file_lists = os.listdir(textpath)
    dir = './reportjson/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    result_dict = {}
    for filename in file_lists:
        with open(os.path.join(textpath, filename), 'r', encoding='utf-8') as f:  # Specify encoding explicitly
            data = f.read()
            data = eval(data)  # 파일 내용을 Python 데이터 구조로 변환
            result_dict[filename[:-4]] = data

    for key, value in result_dict.items(): # 각 파일명과 해당 파일의 내용을 가진 딕셔너리를 JSON 파일로 저장
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

    for filename in file_lists:
        with open(os.path.join(json_folder, filename), encoding='utf-8') as f: # Specify encoding explicitly
            data = json.load(f)
            value_lists = data[filename[:-5]] # 파일명을 키로 사용하여 문장들을 담은 리스트 가져오기
            
            for i in range(1, 6): # ngram 만들기
                gram_list = []
                for lists in value_lists:
                    grams = []
                    for x in range(0, len(lists)-i+1):
                        if lists[x:x+i] not in grams:
                            grams.append(lists[x:x+i])
                    # grams = [lists[x:x+i] for x in range(0, len(lists)-i+1)]
                    gram_list.append(grams)
                    data[f'{i}gram'] = gram_list
            
            with open(os.path.join(n_gram_json, f'{filename[:-5]}_ngram.json'), 'w', encoding='utf-8') as j: # Specify encoding explicitly
                json.dump(data, j, ensure_ascii=False, indent=4)
    return print('n-gram이 추가된 json 파일 저장완료')

txt_to_json()
ngram()