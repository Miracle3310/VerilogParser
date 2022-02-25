from rtl_parser import *
import argparse
import os

mode_list = ['tb', 'only']


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-filename", required=True)
    parser.add_argument("-target", default='wrapper.v')
    parser.add_argument("-modulename")
    parser.add_argument("-mode", choices=mode_list, default=mode_list[0])

    options = parser.parse_args()
    return options


def get_arg(options, option):
    if hasattr(options, option):
        arg = getattr(options, option)
        return arg
    else:
        return None


def gen_module_instance(rtl: rtl_parser):
    ports_num = len(rtl.port_list)
    index = 0
    line_list = []
    line_list.append('{} u_{}'.format(rtl.module_name, rtl.module_name))
    line_list.append('(')

    len_port_name = rtl.max_len_port_name
    len_width = rtl.max_len_width

    for unit in rtl.port_list:
        post_fix = ' //{:<6} width:{:<{}} {}'.format(
            unit['direction'], unit['width'], len_width, unit['comment'])
        if index == ports_num - 1:
            post_fix = ' ' + post_fix
        else:
            post_fix = ',' + post_fix
        line_list.append('\t.{:<{}}({:<{}}){}'.format(
            unit['name'], len_port_name, unit['name'], len_port_name, post_fix))
        index += 1
    line_list.append(');')

    for unit in line_list:
        print(unit)


def gen_port_declaration(rtl: rtl_parser):
    line_list = []
    len_port_name = rtl.max_len_port_name
    len_width = rtl.max_len_width

    for unit in rtl.port_list:
        line_list.append('{:<4} {:<{}} {:<{}};'.format(
            unit['type'], unit['width'], len_width, unit['name'], len_port_name))
    line_list.append(');')

    for unit in line_list:
        print(unit)


def gen_tb(rtl: rtl_parser):
    pass


if __name__ == "__main__":
    options = create_arg_parser()
    # print(options)
    file_name_arg = get_arg(options, "filename")
    module_name_arg = get_arg(options, "modulename")
    work_mode_arg = get_arg(options, "mode")
    target_file_arg = get_arg(options, "target")

    (filepath, filename_we) = os.path.split(file_name_arg)
    (filename, ext) = os.path.splitext(filename_we)

    module_name = filename

    rtl = rtl_parser(file_name_arg, module_name)
    print('file name:{}\tmodule name:{}'.format(filename_we, rtl.module_name))
    # print(rtl.port_list)
    # print(rtl.max_len_port_name)
    gen_module_instance(rtl)
    gen_port_declaration(rtl)
