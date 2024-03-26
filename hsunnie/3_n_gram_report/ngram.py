import os
import json

json_folder = './reportjson/'
file_lists = os.listdir(json_folder)

n_gram_json = './ngram/'
if not os.path.exists(n_gram_json):
    os.makedirs(n_gram_json)

def ngram(file_lists):
    for filename in file_lists:
        with open(os.path.join(json_folder, filename), encoding='utf-8') as f: # Specify encoding explicitly
            data = json.load(f)
            value_lists = data[filename[:-5]] # 파일명을 키로 사용하여 문장들을 담은 리스트 가져오기
            
            for i in range(1, 6): # ngram 만들기
                gram_list = []
                for lists in value_lists:
                    grams = [lists[x:x+i] for x in range(0, len(lists)-i+1)]
                    gram_list.append(grams)
                    data[f'{i}gram'] = gram_list
            
            with open(os.path.join(n_gram_json, f'{filename[:-5]}_ngram.json'), 'w', encoding='utf-8') as j: # Specify encoding explicitly
                json.dump(data, j, ensure_ascii=False, indent=4)
    print('n-gram이 추가된 json 파일 저장완료')

ngram(file_lists)
