module wr_ctr (
// Global input
input  clk,
input  rst_n,
// CPU(or other controllers) input
input  rw_n, 
input  rq_n, // valid for requesting write data
input  [1:0]i_cim_sel,
input  i_bank_sel, // select TOP or BOTTOM bank, write 2 banks once
input  [7:0]row,
input  [10:0] i_inbuffer_adr, // TODO: inbuffer ports to be determined
// CPU output
output  reg o_busy,
// CIMs input
input  [3:0]i_com_busy,
// CIMs output
output  reg [3:0]o_cim_cs_n,
output  reg [1:0]o_op_sel,
output  reg [11:0]o_op_adr, // [11:4] for row [3:0] for column
output  reg o_op_rw_n,
// MUX output
output  reg [3:0]o_mux_sel, // Select 72bits of buffer's 1152bits to output
// Buffer output
output  reg [10:0] o_inbuffer_adr, //TODO: inbuffer ports to be determined
// Comparator input
input  [1:0]i_isequal // valid for comparing 72 bit data
);


localparam
  IDLE         = 4'd0,         
  SELECT       = 4'd1,      
  WRITE        = 4'd2,    
  WRITE_NEXT   = 4'd3,           
  WRITE_WAIT   = 4'd4,           
  READ         = 4'd5,     
  READ_NEXT    = 4'd6,         
  READ_WAIT    = 4'd7,         
  CHECK        = 4'd8;     
reg [3:0] state;


reg [1:0] cim_sel;
reg [4:0]counter; // Write 32 times
always @(posedge clk or !rst_n) begin
  if (!rst_n) 
    begin
      state <= IDLE;
      counter <= 5'b0;
    end 
  else 
    begin
      case (state)
        IDLE: 
          begin
            if (rw_n && rq_n) 
              begin
                state <= SELECT;
                // Sample cim_sel, bank_sel, buffer_adr
                cim_sel <= i_cim_sel;
                o_op_sel[1] <= i_bank_sel;
                o_op_adr[11:4] <= row[7:0];
                o_inbuffer_adr <= i_inbuffer_adr;
              end
            o_cim_cs_n <= 4'b1111;
            o_op_rw_n <= 1'b1;
          end

        SELECT: 
          begin
            state <= WRITE;
            // Initialize op_sel and op_adr
            o_op_sel[0] <= 1'b0;
            o_mux_sel <= 4'b0;
            o_op_adr[3:0] <= 4'b0000;
          end
        
        WRITE:
          begin
            state <= WRITE_NEXT;
            o_cim_cs_n[cim_sel] <= 1'b0;
            o_op_rw_n <= 1'b0;
          end

        WRITE_NEXT:
          begin
            state <= WRITE_WAIT;
            o_cim_cs_n[cim_sel] <= 1'b1;
          end
        
        WRITE_WAIT:
          begin
            if (i_com_busy[cim_sel] == 1'b0) 
            // Wait for busy free
              begin
                state <= READ;
              end
          end
        
        READ:
          begin
            state <= READ_NEXT;
            o_cim_cs_n[cim_sel] <= 1'b0;
            o_op_rw_n <= 1'b1;
          end
        
        READ_NEXT:
          begin
            o_cim_cs_n[cim_sel] <= 1'b1;
          end

        READ_WAIT:
          begin
            if (i_com_busy[cim_sel] == 1'b0) 
            // Wait for busy free
              begin
                state <= CHECK;
              end
          end
        
        CHECK:
          begin
            if (i_isequal != 2'b11)
            // Send Correct
              begin
                if (counter == 5'd31)
                // Finish Write 2 Banks
                  begin
                    state <= IDLE;
                  end
                else
                // Not Finish yet,Write Next 72bits
                  begin
                    state <= WRITE;
                    counter <= counter + 1;
                    o_op_adr <= o_op_adr + 1;
                    o_mux_sel <= counter[3:0];
                    if (counter == 5'd15)
                    // Switch bank
                      begin
                        o_op_sel[0] <= 1'b1;
                        o_inbuffer_adr <= o_inbuffer_adr + 1;
                      end
                  end
              end
            else
            // Send Wrong! Resend
              begin
                state <= WRITE;
              end
          end

        default: 
          begin
            o_cim_cs_n <= 4'b1111;
            o_op_rw_n <= 1'b1;
          end
      endcase
    end
end
endmodule