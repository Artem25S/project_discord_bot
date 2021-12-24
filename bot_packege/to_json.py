import json
def create_json():
    ar = []

    with open('black_list.txt', encoding='utf-8')as r:
        for i in r:
            n = i.lower().split('\n')[0]
            if n != '':
                ar.append(n)
    print()
    print('Слова из black_list, вступившие в силу:', ar)
    print('Обновление black_list...........ОК')
    print()
    with open('black_list.json', 'w', encoding='utf-8') as e:
        json.dump(ar,e)