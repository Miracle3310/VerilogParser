module s1995
       (
         c_in, d_out
       );
parameter BITS_DATA = 8;
parameter BITS_CTRL = 4;
// parameter BITS_TH = 2, BITS_TL = 3;
input [BITS_CTRL - 1: 0] c_in;
output [BITS_DATA - 1: 0] d_out;
wire [BITS_CTRL - 1: 0] c_in;
reg [BITS_DATA - 1: 0] d_out;
endmodule
