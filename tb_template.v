`timescale 1ns/1ps 
/****************************************
Define macros
*****************************************/
`define CLK_PERIOD 1000
`define END_TIME 1000_0000

/****************************************
TB module
****************************************/
module proj_tb ();

/****************************************
Declare variables and params
****************************************/

/****************************************
Initialize
****************************************/

/****************************************
Customisize verification input logic
****************************************/

/****************************************
Verification output vs reference 
****************************************/

/****************************************
Instantiate module
****************************************/

/****************************************
clk generate
****************************************/
initial
  begin
    forever
      #(`CLK_PERIOD / 2) clk = ~clk;
  end

/****************************************
Display test start/end
****************************************/
initial
  begin
    $display("--------------------");
    $display("------Test start----");
    #(`END_TIME)
     $display("------Test end------");
    $display("--------------------");
    $finish;
  end

/****************************************
Waveform generate
****************************************/
initial
  begin
    $dumpfile("./build/wave.vcd");
    $dumpvars;
  end
endmodule //P2S_tb
