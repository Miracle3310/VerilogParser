import re


class rtl_parser:
    def __init__(self, file_v, module_name):
        self.file_v = file_v
        self.module_name = module_name
        self.extract_list = []  # exclude comment lines
        self.port_list = []  # name, direction, width, type, sign, comment
        self.max_len_port_name = 0
        self.max_len_port_width = 0

        self.param_list = []
        self.max_len_param_name = 0
        self.max_len_param_value = 0

        self.regex_module_head = re.compile(r'''
        (module\s+) #1 keyword(module)
        (%s)        #2 module name
        ''' % (self.module_name), re.VERBOSE)

        self.regex_module_port = re.compile(r'''
        (output|input|inout)          #1 direction
        (\s*)                         #2
        (wire|reg)?                   #3 type
        (\s*)                         #4
        (signed|unsigned)?            #5 sign
        (\s*)                         #6
        (\[.*?\])?                    #7 width
        (\s*)?                        #8
        ([^;]+)                       #9 port name
        (;)                           #10 ;
        (\s*\/*\/*\s*)                #11 '//'
        (.*)                          #12 comment
        ''', re.VERBOSE)

        self.regex_module_param = re.compile(r'''
        (parameter) #1 parameter
        (\s+)       #2
        (\w+)       #3 name
        (\s*=\s*)   #4
        (\w+)       #5 value
        ''', re.VERBOSE)

        self.get_module_specified_lines()
        self.extract_param()
        self.extract_port_info()
        self.calculate_port_width_v()
        self.extract_list = []  # release memory

    def get_module_specified_lines(self):
        # print('input function: get_module_specified\n')
        with open(self.file_v, 'r') as file_obj:
            add_flag = 0
            for line in file_obj:
                line = line.strip()
                if not line.startswith('//'):
                    re_head_obj = re.match(self.regex_module_head, line)
                    re_tail_obj = re.match(r'endmodule', line)
                    if re_head_obj is not None:
                        add_flag = 1
                    elif add_flag == 1 and re_tail_obj is not None:
                        add_flag = 0
                        break
                else:
                    continue

                if add_flag == 1:
                    self.extract_list.append(line)

    def extract_port_info(self):
        # print('input function: get_port_info\n')
        for unit in self.extract_list:
            re_port_obj = re.search(self.regex_module_port, unit)
            if re_port_obj is not None:
                port_direction = re_port_obj.group(1)
                port_type = re_port_obj.group(3)
                port_sign = re_port_obj.group(5)
                port_width = re_port_obj.group(7)
                port_name = re_port_obj.group(9)
                port_comment = re_port_obj.group(12)

                if port_type is None:
                    port_type = 'reg' if (
                        port_direction == 'output') else 'wire'
                if port_width is None:
                    port_width = ''
                if len(port_width) > self.max_len_port_width:
                    self.max_len_port_width = len(port_width)

                port_name = port_name.split(',')  # multi port in one line
                for i_port_name in port_name:
                    i_port_name = i_port_name.strip()
                    if len(i_port_name) > self.max_len_port_name:
                        self.max_len_port_name = len(i_port_name)
                    port_info = {'name': i_port_name,
                                 'direction': port_direction,
                                 'width': port_width,
                                 'type': port_type,
                                 'sign': port_sign,
                                 'comment': port_comment}
                    self.port_list.append(port_info)

    def extract_param(self):
        # print('input function: extract_param\n')
        for unit in self.extract_list:
            re_param_obj = re.search(self.regex_module_param, unit)
            if re_param_obj is not None:
                param_name = re_param_obj.group(3)
                param_value = re_param_obj.group(5)
                if len(param_name) > self.max_len_param_name:
                    self.max_len_param_name = len(param_name)
                if len(param_value) > self.max_len_param_value:
                    self.max_len_param_value = len(param_value)
                param_info = {'name': param_name, 'value': param_value}
                self.param_list.append(param_info)

    def calculate_port_width_v(self):
        for unit in self.port_list:
            if unit['width'] == '':
                unit['width_v'] = 1
                continue

            # [BITS_DATA-1:0]
            l_str, r_str = unit['width'].strip('[]').split(':')

            param_str = re.search(r'[a-zA-Z_]+', l_str)
            if param_str is not None:
                param_str = param_str.group()
                for param in self.param_list:
                    flag = 1
                    if param['name'] == param_str:
                        l_str = l_str.replace(param_str, str(param['value']))
                        flag = 0
                        break
                if flag == 1:
                    raise Exception("BITWIDTH is not defined correctly.")
            l_val = eval(l_str)
            r_val = eval(r_str)
            unit['width_v'] = abs(l_val - r_val) + 1


def gen_module_instance(rtl: rtl_parser):
    port_num = len(rtl.port_list)
    index = 0
    line_list = []
    line_list.append('{} u_{}'.format(rtl.module_name, rtl.module_name))
    line_list.append('(')

    len_port_name = rtl.max_len_port_name
    len_port_width = rtl.max_len_port_width

    for unit in rtl.port_list:
        post_fix = ' //{:<6} width: {:<{}} {}'.format(
            unit['direction'], unit['width_v'], len_port_width, unit['comment'])
        if index == port_num - 1:
            post_fix = ' ' + post_fix
        else:
            post_fix = ',' + post_fix
        line_list.append('.{:<{}}\t({:<{}}){}'.format(
            unit['name'], len_port_name, unit['name'], len_port_name, post_fix))
        index += 1
    line_list.append(');')

    # for unit in line_list:
    #     print(unit)

    return '\n'.join(line_list)


def gen_param_declaration(rtl: rtl_parser):
    line_list = []
    len_param_name = rtl.max_len_param_name
    len_param_value = rtl.max_len_param_value

    for unit in rtl.param_list:
        line_list.append('parameter {:<{}} = {:<{}};'.format(
            unit['name'], len_param_name, unit['value'], len_param_value))

    # for unit in line_list:
    #     print(unit)

    return '\n'.join(line_list)


def gen_port_declaration(rtl: rtl_parser):
    line_list = []
    len_port_name = rtl.max_len_port_name
    len_port_width = rtl.max_len_port_width

    for unit in rtl.port_list:
        if unit['type'] == 'reg':
            line_list.append('{:<4} {:<{}} {:<{}};'.format(
                'wire', unit['width'], len_port_width, unit['name'], len_port_name))
        else:
            line_list.append('{:<4} {:<{}} {:<{}};'.format(
                'reg', unit['width'], len_port_width, unit['name'], len_port_name))

    # for unit in line_list:
    #     print(unit)

    return '\n'.join(line_list)


def gen_initialize(rtl: rtl_parser):
    line_list = []
    len_port_name = rtl.max_len_port_name
    line_list.append('initial begin')
    for unit in rtl.port_list:
        if(unit['type'] == 'wire'):
            line_list.append('\t{:<{}} = 0;'.format(
                unit['name'], len_port_name))
    line_list.append('end')

    return '\n'.join(line_list)
