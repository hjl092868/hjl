import xlrd

# 平台映射标准
SECTION_STATION_MAP = {
    "0": [0, ],#这个是在列车停靠时的next_station的值
    "1": [154,184,185],#这个为员村站之前的、增城广场之后的
    "2111": [101, 102],
    "2112": [104, 144, 103, 143],
    "2113": [106, 105],
    "2114": [108, 107],
    "2115": [110, 109],
    "2116": [112, 111],
    "2117": [114, 113],
    "2118": [116, 115],
    "2119": [118, 117],
    "2120": [120, 119],
    "2121": [122, 121],
    "2122": [124, 123, 145, 146],
    "2123": [126, 147, 125],
    "2124": [128, 127],
    "2125": [130, 129],
    "2126": [132, 131],
    "2127": [134, 133],
    "2128": [136, 150, 135, 149],
    "2129": [138, 151, 152, 137],
    "2130": [140, 139],
    "2131": [142, 141],
}
# 列控站台映射标准 奇数为下行，偶数为上行
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
}

def int_transfer_station(int_4):
    int_list = SECTION_STATION_MAP[int_4]
    int1 = int_list[0]
    station = list(filter(lambda x: int1 in x[1], [x for x in CMCS_STATION_MAP.items()]))[0][0]
    return station


def get_all_java_signal_switch_list(file):
    col_dict = {}
    data = xlrd.open_workbook(file)
    sheets = data.sheets()
    sheet1 = data.sheet_by_index(1)
    sheet2 = sheet1
    col6_list = sheet2.col_values(6)
    col12_list = sheet2.col_values(12)

    col6_list_afterdealwith = []
    for x,y in zip(col6_list, col12_list):
        if x != '' and x != 'symbol':
            dict1 = {}
            y = str(y).split('.')[0]
            dict1[x] = int_transfer_station(y)
            col6_list_afterdealwith.append(dict1)
            if col_dict.get(int_transfer_station(y), None):
                signal_list = col_dict.get(int_transfer_station(y))
            else:
                signal_list = []
            signal_list.append(x)
            col_dict[int_transfer_station(y)] = signal_list
    # print('col6_list_afterdealwith', col6_list_afterdealwith)
    print('java统计得到现场的结果','col_dict', col_dict) #java统计得到现场的结果
    return col6_list_afterdealwith, col_dict

# file = r'E:\广州项目\事件分析数据\事件分析数据\0316\驾驶智能分析结果2021-03-18 20_36_57.xls'
# file = r'E:\广州项目\事件分析数据\事件分析数据0318-0321\0321\驾驶智能分析结果2021-03-22 11_01_44.xls' #1
file = r'E:\广州项目\事件分析数据\事件分析数据0318-0321\0321\驾驶智能分析结果2021-03-22 11_01_54.xls' #2
col6_list_afterdealwith, col_dict = get_all_java_signal_switch_list(file)


def judge_initial(str1, list1):
    if list(filter(lambda x: x in str1, list1)):
        return True
    else:
        return False


def get_aciton_rule_dict(file):
    data = xlrd.open_workbook(file)
    sheets = data.sheets()
    sheet1 = data.sheet_by_index(0)

    initial_str_list = ['sw', 'SW']
    if '上行普' in file or '上行快' in file:
        initial_str_list = ['sw', 's', 'SW', 'S']
    if '下行普' in file or '下行快' in file:
        initial_str_list = ['sw', 'x', 'SW', 'X']
    # print('initial_str_list', initial_str_list)
    col0_list = sheet1.col_values(0)
    col0_list = list(map(lambda x: x.split('-')[0], col0_list))
    col3_list = sheet1.col_values(3)
    col3_list = list(map(lambda x: str(x), col3_list))
    col5_list = sheet1.col_values(5)
    col5_list = list(map(lambda x: str(x), col5_list))
    col6_list = sheet1.col_values(6)
    col6_list = list(map(lambda x: str(x), col6_list))
    # print(col0_list, col3_list, col5_list)

    station_dict = {}
    for w, x, y, z in zip(col0_list, col3_list, col5_list, col6_list):
        if w != '' and w != '区间':
            station = w
            dict1 = {}
            if judge_initial(x, initial_str_list):
                value = y in ['1','1.0'] and z or y
                dict1[x] = value
                if station_dict.get(station, None):
                    signal_list = station_dict.get(station)
                    signal_list.append(dict1)
                    # signal_list.append(x)
                else:
                    signal_list = [dict1]
                    # signal_list = [x]
                station_dict[station] = signal_list

    # print('得到规则表里所有的对应关系（区间与站、信号机）','station_dict', station_dict) #得到规则表里所有的对应关系（区间与站、信号机）
    return station_dict

# file3 = r'C:\Users\Administrator\Desktop\更新后文件20210226\修改版-测试用固定规则(下行普)1016.xlsx' #1
file3 = r'C:\Users\Administrator\Desktop\更新后文件20210226\修改版-测试用固定规则(上行普)1016.xlsx' #2
station_dict = get_aciton_rule_dict(file3)


def split_by_brackets(str1):
    try:
        result = str1.split('{')[1]
    except:
        result = ''
    return  result


def get_ydas_data(file):
    # f = open(r'E:\广州项目\acceptydas_0316_0645_0753.log','r')
    f = open(file,'r')
    content = f.read()
    # print(type(content), content)
    f_content_list = content.split('}')
    f_content_list = list(map(lambda x: split_by_brackets(x), f_content_list))
    f_content_list = list(filter(lambda x: x != '', f_content_list))
    f_content_list = list(map(lambda x:  eval('{' + x + '}'), f_content_list))
    # a = eval(f_content_list[0])
    # print(len(f_content_list), type(f_content_list[0]), f_content_list[0])
    f.close()
    return f_content_list

# file2 = r'E:\广州项目\acceptydas_0316_0645_0753.log'
# file2 = r'E:\广州项目\事件分析数据\事件分析数据0318-0321\0321\acceptydas_20210321_1803_1908.log' #1
file2 = r'E:\广州项目\事件分析数据\事件分析数据0318-0321\0321\acceptydas_0321_1644_1753.log' #2
f_content_list = get_ydas_data(file2)
# print('f_content_list', f_content_list)


statistics_ydas_dict = {}
for ydas_dict in f_content_list:
    if ydas_dict['next_station'] == 0 or ydas_dict['now_station'] == 0 or ydas_dict['final_station'] == 0 or ydas_dict['final_station'] == 141:
        pass
    else:
        ydas_now_station = ydas_dict['now_station']
        ydas_now_station = list(filter(lambda x: ydas_now_station in x[1], [x for x in CMCS_STATION_MAP.items()]))[0][0]
        signal_section_list = station_dict[ydas_now_station]
        ydas_section = ydas_dict['section']
        for signal_section in signal_section_list:
            signal, section = [x for x in signal_section.items()][0]
            if float(section) == ydas_section:
                if statistics_ydas_dict.get(ydas_now_station, None):
                    list1 = statistics_ydas_dict.get(ydas_now_station)
                else:
                    list1 = []
                if signal not in list1:
                    list1.append(signal)
                statistics_ydas_dict[ydas_now_station] = list1
print('ydas列控得到的应该各个站所经过的信号机/道岔','statistics_ydas_dict', statistics_ydas_dict) #ydas列控得到的应该各个站所经过的信号机/道岔

not_exist_dict = {}
for station, signal_list in statistics_ydas_dict.items():
    statictis_signal_list = col_dict[station]
    differece_list = list(set(signal_list).difference(
        set(statictis_signal_list)))  # 在ydas_signal_switch_list但不在col6_list_afterdealwith里的元素
    if not_exist_dict.get(station, None):
        list1 = not_exist_dict.get(station)
    else:
        list1 = []
    list1 += differece_list
    not_exist_dict[station] = list1
print('初步判断，不存在与java后天得出的结果，但是存在与ydas得出的结果','not_exist_dict', not_exist_dict) #初步判断，存在与java后天得出的结果，但是不存在与ydas得出的结果


def station_transfer_int4(station):
    int_list = CMCS_STATION_MAP[station]
    int1 = int_list[0]
    int4 = list(filter(lambda x: int1 in x[1], [x for x in SECTION_STATION_MAP.items()]))[0][0]
    return int4

final_not_exist_dict = {}
for station, signal_list in not_exist_dict.items():
    int4 = station_transfer_int4(station)
    for signal in signal_list:
        if station != '增城广场':
            previous_station = int_transfer_station(str(float(int4) + 1).split('.')[0])
            if signal in statistics_ydas_dict.get(previous_station,[]) and signal in statistics_ydas_dict[station] and signal in col_dict.get(previous_station,[]):
                pass
            else:
                if final_not_exist_dict.get(station, None):
                    list1 = final_not_exist_dict.get(station)
                else:
                    list1 = []
                if signal not in list1:
                    list1.append(signal)
                final_not_exist_dict[station] = list1
print('去除与上一站重复的内容','final_not_exist_dict', final_not_exist_dict) #去除与上一站重复的内容

final2_not_exist_dict = {}
for station, signal_list in final_not_exist_dict.items():
    int4 = station_transfer_int4(station)
    for signal in signal_list:
        if station != '员村':
            next_station = int_transfer_station(str(float(int4) - 1).split('.')[0])
            if signal in statistics_ydas_dict.get(next_station,[]) and signal in statistics_ydas_dict[station] and signal in col_dict.get(next_station,[]):
                pass
            else:
                if final2_not_exist_dict.get(station, None):
                    list1 = final2_not_exist_dict.get(station)
                else:
                    list1 = []
                if signal not in list1:
                    list1.append(signal)
                    final2_not_exist_dict[station] = list1
print('去除与下一站重复的内容','final2_not_exist_dict', final2_not_exist_dict)
