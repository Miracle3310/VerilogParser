from rtl_parser import *
import os
import argparse

side_list = ["left", "top", "right", "bottom"]
# 0=>left 1=>top 2=>right 3=>bottom
layer_list = ["M1", "M1", "M1", "M1"]
offset_list = ["L_offset", "T_offset", "R_offset", "B_offset"]
space_list = ["L_space", "T_space", "R_space", "B_space"]


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", required=True)

    options = parser.parse_args()
    return options


def get_arg(options, option):
    if hasattr(options, option):
        arg = getattr(options, option)
        return arg
    else:
        return None


def get_pin_list(rtl: rtl_parser):
    in_pin_list = []
    out_pin_list = []
    pin_list = []
    for unit in rtl.port_list:
        bitwidth = unit["width_v"]
        if bitwidth == 1:
            if unit["direction"] == "input":
                in_pin_list.append("{}".format(unit["name"]))
            else:
                out_pin_list.append("{}".format(unit["name"]))
        else:
            for i in range(bitwidth):
                if unit["direction"] == "input":
                    in_pin_list.append("{}[{}]".format(unit["name"], str(i)))
                else:
                    out_pin_list.append("{}[{}]".format(unit["name"], str(i)))
    pin_list = in_pin_list + out_pin_list
    return pin_list, in_pin_list, out_pin_list


def gen_pin_oneside(pin_list, side: int, idx_start: int, side_pin_num: int):
    line_list = []

    for i in range(idx_start, idx_start + side_pin_num):
        s_cmd = "set_pin_physical_constraints "
        s_pinname = "-pin_name {{{}}} ".format(pin_list[i])
        s_layers = "-layers {} ".format(layer_list[side])
        s_width = "-width $PIN_WIDTH -depth $PIN_DEPTH "
        s_side = "-side {} ".format(str(side + 1))  # icc: 1=>left, ...
        s_offset = "-offset [expr ${}+${}*{}]".format(
            offset_list[side], space_list[side], str(i - idx_start)
        )
        line = s_cmd + s_pinname + s_layers + s_width + s_side + s_offset
        line_list.append(line)

    return "\n".join(line_list)


def gen_pin(rtl: rtl_parser):
    gen_pin_line_list = []
    pin_list, in_pin_list, out_pin_list = get_pin_list(rtl)
    pin_num = len(pin_list)
    oneside_pin_num = int(pin_num / 4)
    lastside_pin_num = pin_num - 3 * oneside_pin_num

    gen_pin_line_list.append(
        gen_pin_oneside(pin_list, 0, 0 * oneside_pin_num, oneside_pin_num)
    )
    gen_pin_line_list.append(
        gen_pin_oneside(pin_list, 1, 1 * oneside_pin_num, oneside_pin_num)
    )
    gen_pin_line_list.append(
        gen_pin_oneside(pin_list, 2, 2 * oneside_pin_num, oneside_pin_num)
    )
    gen_pin_line_list.append(
        gen_pin_oneside(pin_list, 3, 3 * oneside_pin_num, lastside_pin_num)
    )

    print("IN_PORT:")
    print(" ".join(in_pin_list))
    print("OUT_PORT:")
    print(" ".join(out_pin_list))
    # print(pin_list)
    for i in range(4):
        print("# {}-side".format(side_list[i]))
        print(gen_pin_line_list[i])


if __name__ == "__main__":
    options = create_arg_parser()
    # print(options)
    file_name_arg = get_arg(options, "v")
    work_mode_arg = get_arg(options, "mode")

    (filepath, filename_we) = os.path.split(file_name_arg)
    (filename, ext) = os.path.splitext(filename_we)

    module_name = filename

    rtl = rtl_parser(file_name_arg, module_name)
    gen_pin(rtl)
