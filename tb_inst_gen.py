from rtl_parser import *
import argparse
import os

mode_list = ['tb', 'inst']


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", required=True)
    parser.add_argument("-mode", choices=mode_list, default=mode_list[0])

    options = parser.parse_args()
    return options


def get_arg(options, option):
    if hasattr(options, option):
        arg = getattr(options, option)
        return arg
    else:
        return None


def gen_tb(rtl: rtl_parser, filepath_tb_template):
    with open(filepath_tb_template, 'r') as file_tb_template:
        tb_str = file_tb_template.read()

        module_name_str = rtl.module_name
        module_name_regex = r"(?<=module )proj"
        tb_str = re.sub(module_name_regex, module_name_str, tb_str)

        port_str = gen_port_declaration(rtl)
        port_str = '\n' + port_str + '\n\n'
        port_regex = r"(?<=Declare variables and params\n\*{40}/\n)\n"
        tb_str = re.sub(port_regex, port_str, tb_str)

        param_str = gen_param_declaration(rtl)
        param_str = param_str + '\n\n'
        param_regex = r"(?<=Declare variables and params\n\*{40}/\n)\n"
        tb_str = re.sub(param_regex, param_str, tb_str)

        init_str = gen_initialize(rtl)
        init_str = init_str + '\n\n'
        init_regex = r"(?<=Initialize\n\*{40}/\n)\n"
        tb_str = re.sub(init_regex, init_str, tb_str)

        inst_str = gen_module_instance(rtl)
        inst_str = inst_str + '\n\n'
        inst_regex = r"(?<=Instantiate module\n\*{40}/\n)\n"
        tb_str = re.sub(inst_regex, inst_str, tb_str)

        # print(tb_str)
        with open(module_name_str + '_tb.v', 'w') as file_tb:
            file_tb.write(tb_str)


if __name__ == "__main__":
    options = create_arg_parser()
    # print(options)
    file_name_arg = get_arg(options, "v")
    work_mode_arg = get_arg(options, "mode")

    (filepath, filename_we) = os.path.split(file_name_arg)
    (filename, ext) = os.path.splitext(filename_we)

    module_name = filename

    rtl = rtl_parser(file_name_arg, module_name)
    # print('file name:{}\tmodule name:{}'.format(filename_we, rtl.module_name))
    # print(rtl.param_list)
    # print(rtl.port_list)
    # print(rtl.max_len_port_name)
    # gen_param_declaration(rtl)
    # gen_port_declaration(rtl)
    # gen_module_instance(rtl)
    if work_mode_arg == mode_list[0]:
        gen_tb(rtl, 'tb_template.v')
    elif work_mode_arg == mode_list[1]:
        inst_str = gen_module_instance(rtl)
        print(inst_str)
