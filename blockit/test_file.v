module rram (
  input clk,
  input rst_n,
  input [WIDTH-1:0] i_data,
  input rw_n,
  input [10:0] i_adr,
  output reg [WIDTH-1:0] o_data
);

reg[WIDTH-1:0] rram_reg [10:0];

integer  i;
always @(posedge clk or rst_n) begin
  if (!rst_n)
    begin
        for(i=0;i<2048;i=i+1)
          begin
            rram_reg[i] <= 0;
          end
    end
  else
    if (rw_n) 
    // Read
      begin
        o_data <= rram_reg[i_adr];
      end
    else
    // Write
      begin
        rram_reg[i_adr] <= i_data;
      end
end
endmodule