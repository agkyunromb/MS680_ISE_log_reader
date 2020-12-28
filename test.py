'''
Author: AG
Date: 2020-12-26 21:43:24
LastEditTime: 2020-12-28 09:38:51
LastEditors: AG
FilePath: /MS680_ISE_log_reader/test.py
Description: 
'''

import os
import re
import time
import copy

#base_work_dir = r"E:\git_work_dir\MS680_ISE_log_reader\work_dir"
base_work_dir = os.path.join(os.getcwd(), "work_dir")


def get_log_list(work_dir: str) -> list:
    """
    读取工作目录下的log文件完整路径+名称
    """
    file_list = []
    reg1 = re.compile("^Log_\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}.txt$")
    for item in list(
            filter(lambda file_name: re.match(reg1, file_name),
                   os.listdir(work_dir))):
        file_list.append(os.path.join(work_dir, item))
    return file_list


def file_reader(file_list: list) -> str:
    """
    读取过滤log文件
    """
    reg2 = re.compile(
        r"(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}.\d{1,2}) \| 调试 - \[\d+\] : ((收到ISE数据测试号:[0-9]+)|(Na[\u4e00-\u9fa5]{4}\w*):([-.0-9]+), (K[\u4e00-\u9fa5]{4}\w*):([-.0-9]+),(Cl[\u4e00-\u9fa5]{4}\w*):([-.0-9]+))"
    )

    data = ""

    for log_file in log_list:
        with open(log_file, encoding="utf-16-le") as f:
            for line in f.readlines():
                if re.match(reg2, line):
                    data += re.match(reg2, line).string.replace(
                        "| 调试 - [10] : ", "")
    return data


def data_filter(data: str) -> str:
    """
    清洗数据：
    删除空测试
    删除冗余的时间信息
    排版为csv样式
    """
    data2 = ""
    reg3 = re.compile(
        r"\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}.\d{1,2} ")
    v1list = data.splitlines()

    v2list = [v1list[i:i + 5] for i in range(0, len(v1list), 5)]
    v2list_temp = copy.deepcopy(v2list)
    for item in v2list_temp:
        if "收到ISE数据测试号:0" in item[0]:
            v2list.remove(item)
        else:
            for index, msg in enumerate(item):
                if index != 0:
                    item[index] = re.sub(reg3, "", msg)
                    item[index] = re.sub(r":", ",", item[index])
                    item[index] = re.sub(r" K", "K", item[index])
                data2 += (item[index] + "\n")
    return (data2)


def csv_output(data: str, output_dir=base_work_dir) -> int:
    """
    文件输出
    """
    output_filename = str(
        time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(
            time.time()))) + '-输出.csv'
    full_path = os.path.join(output_dir, output_filename)
    with open(full_path, "w", encoding="utf-8_sig") as f:
        f.write(data)

    return 1


if __name__ == "__main__":

    log_list = get_log_list(base_work_dir)
    file_data = file_reader(log_list)
    data = data_filter(file_data)
    csv_output(data)
    print("处理成功！窗口三秒后关闭。")
    time.sleep(3)