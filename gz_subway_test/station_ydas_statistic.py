import json


def split_by_brackets(str1):
    try:
        result = str1.split('{')[1]
    except:
        result = ''
    return  result


def get_ydas_data(file):
    f = open(file,'r')
    content = f.read()
    f_content_list = content.split('}')
    f_content_list = list(map(lambda x: split_by_brackets(x), f_content_list))
    f_content_list = list(filter(lambda x: x != '', f_content_list))
    f_content_list = list(map(lambda x:  eval('{' + x + '}'), f_content_list))
    f.close()
    return f_content_list

file2 = r'E:\广州项目\acceptydas_bk_0322_0328.log' #2
f_content_list = get_ydas_data(file2)


CMCS_STATION_MAP = {
    "员村": [101, 102],
    "天河公园": [104, 144, 103, 143],
    "棠东": [106, 105],
    "黄村": [108, 107],
    "大观南路": [110, 109],
    "天河智慧城": [112, 111],
    "神舟路": [114, 113],
    "科学城": [116, 115],
    "苏元": [118, 117],
    "水西": [120, 119],
    "长平": [122, 121],
    "金坑": [124, 123, 145, 146],
    "镇龙西": [126, 147, 125],
    "镇龙": [128, 127],
    "中新": [130, 129],
    "坑贝": [132, 131],
    "凤岗": [134, 133],
    "朱村": [136, 150, 135, 149],
    "山田": [138, 151, 152, 137],
    "钟岗": [140, 139],
    "增城广场": [142, 141],
    "0": [0, ],#这个是在列车停靠时的next_station的值
    "1": [154,184,185],#这个为员村站之前的、增城广场之后的
}


exist_stations = []
for k, v in CMCS_STATION_MAP.items():
    for station in v:
        exist_stations.append(station)

not_exist_stations = []
for data in f_content_list:
    if data['now_station'] not in exist_stations and data['year'] != 0:
        print(data, "\n")
        not_exist_stations.append(data)
# print('not_exist_stations', not_exist_stations)


def write_ydas_txt(file, list1):
    f = open(file, 'w')
    for x in list1:
        f.write(str(x) + "," + "\n")
    f.close()

file2_2 =  r'E:\广州项目\acceptydas_bk_0322_0328_result.txt'
write_ydas_txt(file2_2, not_exist_stations)