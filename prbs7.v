`define BITS_DATA 8
`define BITS_CTRL BITS_DATA
module prbs7 (
         clk,
         rst_n,
         prbs
       );

parameter PN = 7;
parameter WIDTH = 24;
parameter TAP1 = 6;
parameter TAP2 = 5;

input clk;
input rst_n;
// output [WIDTH - 1: 0] prbs; // hello world
// output [2: 0] prbs;
output [3 - 1: 0] d1, d2, d3 , d11;
output [WIDTH - 1: 0]d21;
output [20: 0]d22;


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
