import xlrd


def get_all_java_signal_switch_list(file):
    data = xlrd.open_workbook(file)
    sheets = data.sheets()
    sheet1 = data.sheet_by_index(1)
    # sheet2 = data.sheet_by_name('数据库')
    sheet2 = sheet1
    # print(sheets, sheet1, sheet2)
    col6_list = sheet2.col_values(6)
    # print(col6_list)
    col6_list_afterdealwith = list(filter(lambda x: x != '' and x != 'symbol', col6_list))
    print('col6_list_afterdealwith', col6_list_afterdealwith)
    return col6_list_afterdealwith

# file = r'E:\广州项目\事件分析数据\事件分析数据\0316\驾驶智能分析结果2021-03-18 20_36_57.xls'
# file = r'E:\广州项目\事件分析数据\事件分析数据0318-0321\0321\驾驶智能分析结果2021-03-22 11_01_44.xls' #1
file = r'E:\广州项目\事件分析数据\事件分析数据0318-0321\0321\驾驶智能分析结果2021-03-22 11_01_54.xls' #2
col6_list_afterdealwith = get_all_java_signal_switch_list(file)


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


def write_ydas_txt(file, list1):
    f = open(file, 'w')
    for x in list1:
        f.write(str(x) + "," + "\n")
    f.close()

# file2_2 = r'E:\广州项目\acceptydas_0316_0645_0753.txt'
# file2_2 =  r'E:\广州项目\事件分析数据\事件分析数据0318-0321\0321\acceptydas_20210321_1803_1908.txt' #1
file2_2 =  r'E:\广州项目\事件分析数据\事件分析数据0318-0321\0321\acceptydas_0321_1644_1753.txt' #2
write_ydas_txt(file2_2, f_content_list)

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
    col3_list = sheet1.col_values(3)
    col3_list = list(map(lambda x: str(x), col3_list))
    col5_list = sheet1.col_values(5)
    col5_list = list(map(lambda x: str(x), col5_list))
    col6_list = sheet1.col_values(6)
    col6_list = list(map(lambda x: str(x), col6_list))
    # print(col3_list, col5_list)

    rule_dict = {}
    for x, y, z in zip(col3_list, col5_list, col6_list):
        if judge_initial(x, initial_str_list):
            value = y in ['1','1.0'] and z or y
            rule_dict[x] = value
    print('rule_dict', rule_dict)
    return rule_dict


# file3 = r'C:\Users\Administrator\Desktop\更新后文件20210226\修改版-测试用固定规则(下行普)1016.xlsx' #1
file3 = r'C:\Users\Administrator\Desktop\更新后文件20210226\修改版-测试用固定规则(上行普)1016.xlsx' #2
rule_dict = get_aciton_rule_dict(file3)


def lowercase_uppercase(str1):
    str1 = str1.replace('s','S').replace('w','W').replace('x','X')
    return str1


ydas_signal_switch_list = []
for dict1 in f_content_list:
    section = dict1['section']
    for k, y in rule_dict.items():
        if float(y) == section:
            if k not in ydas_signal_switch_list:
                ydas_signal_switch_list.append(k)

print('ydas_signal_switch_list', ydas_signal_switch_list)

# differece_list = list(set(col6_list_afterdealwith).difference(set(ydas_signal_switch_list)))
ydas_signal_switch_list = list(map(lambda x: lowercase_uppercase(x), ydas_signal_switch_list))
col6_list_afterdealwith = list(map(lambda x: lowercase_uppercase(x), col6_list_afterdealwith))

differece_list = list(set(ydas_signal_switch_list).difference(set(col6_list_afterdealwith))) # 在ydas_signal_switch_list但不在col6_list_afterdealwith里的元素
print('----',differece_list)