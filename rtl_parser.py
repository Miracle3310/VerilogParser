import re


class rtl_parser:
    def __init__(self, file_v, module_name):
        self.file_v = file_v
        self.module_name = module_name
        self.extract_list = []  # exclude comment lines
        self.port_list = []  # name, direction, width, type, sign, comment
        self.max_len_port_name = 0

        self.regex_module_head = re.compile(r'''
        (module\s+) # 1 keyword(module)
        (%s)       # 2 module name
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

        self.get_module_specified_lines()
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
                port_width_str = re_ports_obj.group(7)
                port_name = re_ports_obj.group(9)
                port_comment = re_ports_obj.group(12)
                if port_type == '':
                    port_type = 'reg' if (
                        port_direction == 'output') else 'wire'
                if port_width_str == None:
                    port_width_str = ''
                if len(port_name) > self.max_len_port_name:
                    self.max_len_port_name = len(port_name)
                port_info = {'name': port_name,
                             'direction': port_direction,
                             'width': port_width_str,
                             'type': port_type,
                             'sign': port_sign,
                             'comment': port_comment}
                self.port_list.append(port_info)
