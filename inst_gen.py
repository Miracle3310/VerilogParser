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
    # print(rtl.param_list)
    # print(rtl.port_list)
    # print(rtl.max_len_port_name)
    gen_param_declaration(rtl)
    gen_port_declaration(rtl)
    gen_module_instance(rtl)
