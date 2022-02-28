module s2001 #(
         parameter BITS_DATA = 8,
         parameter BITS_CTRL = 4
       )
       (
         input [BITS_CTRL - 1: 0] c_in,
         output reg [BITS_DATA - 1: 0] d_out
       );
endmodule
