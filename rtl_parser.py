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

        self.regex_module_ports = re.compile(r'''
        (output|input|inout)          #1 direction
        (\s*)                         #2
        (wire|reg)?                   #3 type
        (\s*)                         #4
        (signed|unsigned)?            #5 sign
        (\s*)                         #6
        (\[.*?\])?                    #7 width
        (\s*)?                        #8
        (\w+)                         #9 port name
        (\s*;\s*)                     #10
        (\/*\/*\s*)                   #11 '// '
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
        self.extract_ports_info()
        self.extract_list = []  # release memory

    def get_module_specified_lines(self):
        print('input function: get_module_specified\n')
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

    def extract_ports_info(self):
        print('input function: get_ports_info\n')
        for unit in self.extract_list:
            re_ports_obj = re.search(self.regex_module_ports, unit)
            if re_ports_obj is not None:
                port_direction = re_ports_obj.group(1)
                port_type = re_ports_obj.group(3)
                port_sign = re_ports_obj.group(5)
                port_width = re_ports_obj.group(7)
                port_name = re_ports_obj.group(9)
                port_comment = re_ports_obj.group(12)
                if port_type is None:
                    port_type = 'reg' if (
                        port_direction == 'output') else 'wire'
                if port_width is None:
                    port_width = ''
                if len(port_name) > self.max_len_port_name:
                    self.max_len_port_name = len(port_name)
                if len(port_width) > self.max_len_port_width:
                    self.max_len_port_width = len(port_width)
                port_info = {'name': port_name,
                             'direction': port_direction,
                             'width': port_width,
                             'type': port_type,
                             'sign': port_sign,
                             'comment': port_comment}
                self.port_list.append(port_info)

    def extract_param(self):
        print('input function: extract_param\n')
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
