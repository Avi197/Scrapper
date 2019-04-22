import json


def fix_rating():
    with open('cooky.json') as json_file:
        data = json.load(json_file)

    for s in data:
        if s['price_rate'] == '-.-': s['price_rate'] = None
        if s['quality_rate'] == '-.-': s['quality_rate'] = None
        if s['service_rate'] == '-.-': s['service_rate'] = None

    with open("cooky_2.json", 'w') as json_data_out:
        json.dump(data, json_data_out, ensure_ascii=False, indent=2)


def fix_time():
    with open('cooky_2.json') as json_file:
        data = json.load(json_file)

    for s in data:
        # if s['opening-time'] == 'Cửa hàng 24h': s['opening-time'] = '00:00 - 00:00'
        s['opening-time'] = s['opening-time'].split(' - ')

    with open("cooky_2.json", 'w') as json_data_out:
        json.dump(data, json_data_out, ensure_ascii=False, indent=2)


def fix_phone_number():
    with open('cooky_2.json') as json_file:
        data = json.load(json_file)

    for s in data:
        # s['phone_number'] = s['phone_number']
        s['phone_number'] = s['phone_number'].strip().split(' - ') if s['phone_number'] else None
        print(s['phone_number'])

    with open("cooky_2.json", 'w') as json_data_out:
        json.dump(data, json_data_out, ensure_ascii=False, indent=2)


# fix_time()
fix_phone_number()

