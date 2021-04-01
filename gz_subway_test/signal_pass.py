import xlrd

"""
信号机、道岔如果在停站前（列车开始减速进入站台的那段时间）被计算在计入的范围之内（信号机30m，
道岔50m），则应该排除掉；
"""

CMCS_STATION_MAP = {
    "员村":"2111",
    "天河公园": "2112",
    "棠东": "2113",
    "黄村": "2114",
    "大观南路": "2115",
    "天河智慧城": "2116",
    "神舟路": "2117",
    "科学城": "2118",
    "苏元": "2119",
    "水西": "2120",
    "长平": "2121",
    "金坑": "2122",
    "镇龙西": "2123",
    "镇龙": "2124",
    "中新": "2125",
    "坑贝": "2126",
    "凤岗": "2127",
    "朱村": "2128",
    "山田": "2128",
    "钟岗": "2130",
    "增城广场": "2131",
}


def get_excel_content(file):
    data = xlrd.open_workbook(file)
    sheets = data.sheets()
    sheet1 = data.sheet_by_index(0)
    sheet2 = sheet1

    station_list = sheet2.col_values(0)
    type_list = sheet2.col_values(1)
    signal_list = sheet2.col_values(3)
    distance_list = sheet2.col_values(4)

    return station_list, type_list, signal_list, distance_list

file = r'E:\广州项目\计算在停车前的道岔信号机\修改版-测试用固定规则(上行普)1016.xlsx'
station_list, type_list, signal_list, distance_list = get_excel_content(file)

# station_standard_list = list(map(lambda x: {'station': x[0].split('-')[0], 'distance': x[3]}, list(filter(lambda x: x[1] == 8001, [x for x in zip(station_list, type_list, signal_list, distance_list)]))))
station_standard_list = list(map(lambda x: {'station': x[0], 'distance': x[3]}, list(filter(lambda x: x[1] == 8001, [x for x in zip(station_list, type_list, signal_list, distance_list)]))))
print('station_standard_list', station_standard_list)

pass_list = []
pass_dict = {}
for station, type, signal, distance in zip(station_list, type_list, signal_list, distance_list):
    if type not in [1001, 1002]:
        continue
    # station = station.split('-')[0]
    station = station
    # station_code = CMCS_STATION_MAP[station]
    station_code = CMCS_STATION_MAP[station.split('-')[0]] + '-' +  CMCS_STATION_MAP[station.split('-')[1]]
    station_distance = list(filter(lambda x: x['station'] == station, station_standard_list))
    if not station_distance:
        continue
    # print('station_distance', station_distance)
    station_distance = station_distance[0]['distance']
    if type == 1001 and 0 < distance - station_distance < 30:
        pass_list.append((station, type, signal, distance))
        list1 = pass_dict.get(station_code, [])
        # if (type, signal, distance) not in list1:
        #     list1.append((type, signal, distance))
        if signal not in list1:
            list1.append(signal)
        pass_dict[station_code] = list1
    elif type == 1002 and 0 < distance - station_distance < 50:
        pass_list.append((station, type, signal, distance))
        list1 = pass_dict.get(station_code, [])
        # if (type, signal, distance) not in list1:
        #     list1.append((type, signal, distance))
        if signal not in list1:
            list1.append(signal)
        pass_dict[station_code] = list1
print('pass_list', list(set(pass_list)))
print('pass_dict', pass_dict)

