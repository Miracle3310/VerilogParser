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

output [WIDTH - 1: 0] prbs; // hello world
// output [23: 0] prbs; // hello
input clk;
input rst_n;

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
