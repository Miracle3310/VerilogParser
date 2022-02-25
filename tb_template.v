`timescale 1ps/1ps
 `ifdef SDF_SIM
 `define SDF_FILE ""
 `define SDF_MTM "MAXIMUM"
 `define SDF_SACLE_FACTORS "1:1:1"
 `endif 
/****************************************
Define macros
*****************************************/
`define CLK_PERIOD 1000
`define END_TIME 1000_0000

/****************************************
TB module
****************************************/
module P2S_tb ();

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
    clk = 0;
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
SDF back-annotated and waveform generate
****************************************/
initial
  begin
    $vcdpluson;
`ifdef SDF_SIM

    $sdf_annotate(`SDF_FILE, inst_1, , "sdf.log", `SDF_MTM, `SDF_SACLE_FACTORS);
`endif

  end
endmodule //P2S_tb
