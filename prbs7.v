`define BITS_DATA 8
`define BITS_CTRL BITS_DATA
module prbs7 (
         clk,
         rst_n,
         prbs
       );

parameter PN = 7,
          WIDTH = 24,
          TAP1 = 6,
          TAP2 = 5;

input clk;
input rst_n;
// output [WIDTH - 1: 0] prbs; // hello world
output prbs;
output d1;
output d2;
output d3;
output d4;
output d5;
output d6;
output d7;
output d8;
output d9;
output d10;
output d11;
output d12;
output d13;
output d14;
output d15;
output d16;
output d17;
output d18;
output d19;
output d20;
output d21;
output d22;


reg [WIDTH - 1: 0] d;
reg [WIDTH - 1: 0] prbs;

always @ (posedge clk)
  if (!rst_n)
    prbs <= 1; //anything but the all 0s case is fine.
  else
    begin
      d = prbs;
      repeat (WIDTH) d = {d, d[TAP1] ^ d[TAP2]};
      prbs <= d;
    end

endmodule // prbs7
