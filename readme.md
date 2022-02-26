# VerilogParser

借助 python 完成 verilog 的辅助编写：

- 模块例化模板
- TB 模板
- DC、ICC 脚本自动更新

## 思路

思路和第一个参考一样，用一个对象解析 rtl 代码，得到模块名、端口信息，然后要例化模板就从解析出来的东西里拿然后打印字符串、要 dc、icc 模板也是同理。

所以需要一个 rtl_parser，初始化这个对象时，直接解析文件，获得以下信息，存储在该对象的内部变量里，然后外部可以调用，自己选择如何打印。

- 模块名 module_name
- 端口 port_list (用列表存字典)
  - 端口名 name
  - 方向 direction
  - 位宽 width （直接保留原始字符串）
  - 位宽数值 width_v
  - 符号 sign
  - 行尾注释 comment
- 为了打印整齐，存一下 name 和 width 的最大长度
- 参数、宏的定义值（可选）param_list define_list
  - name
  - value（数值）
- 端口后的注释信息能保留，同时自己生成 io、位宽的注释信息

`define` 有个问题是它不会在 module 块里，但是目前的 parser 会先定位 module 和 endmodule 之间的非注释行，然后再解析端口，这样就会错过 `define` 的内容。没想好怎么解决，那就代码规范里要求位宽不使用 `define` 好了。

## 特性

RTL 代码要求：

- 端口定义格式 `input [WIDTH-1:0] d1, d2;`
  - 以行为单位处理，所以不支持分行写法
  - 需要以分号结尾（不支持2001标准的 ANSI C 风格写法）
  - 如果不声明 `reg` 或者 `wire` 就根据方向判断
- 支持以 `[BITS_DATA-1:0]` 形式定义的位宽，会替换参数后计算实际位宽
  - 参数名不能带数字
  - 只检查冒号左边表达式，且只替换一次
- 支持一行内定义多个端口，如 `input clk, rst_n;`
- `define` 没有处理，所以定义位宽时不能用
- `parameter` 定义必须给出数值

例化模板与 tb 模板：

- 默认一个文件里一个 module，二者同名
- 生成的 tb 文件为“模块名_tb.v”
- 生成例化代码则直接打印在窗口里
- 还不能生成带参数例化
- 模板中端口的位宽直接取自原代码的写法（这点还有待考虑）

icc 引脚布置：

- 先打印输入和输出的所有端口，然后打印生成的印脚布置命令
- 四个方向平均分配，顺序左上右下

## 用法

```bash
python tb_inst_gen.py -v prbs7.v
// python tb_inst_gen.py -v prbs7.v -mode tb

python tb_inst_gen.py -v prbs7.v -mode inst

python icc_pin_gen.py -v prbs7.v
```

## 参考资料

- 最初的参考 <https://www.cnblogs.com/moluoqishi/p/11332152.html>
- python 的正则表达式 <https://www.runoob.com/python3/python3-reg-expressions.html>
- prbs RTL 代码 <http://fpgasrus.com/prbs.html>
- 正则表达测试网站 <https://regex101.com/>
- python 格式化字符串对齐 <https://blog.csdn.net/weixin_44630991/article/details/86767601>
- verilog-1995与2001的区别 <https://www.cnblogs.com/tshell/p/3236476.html>