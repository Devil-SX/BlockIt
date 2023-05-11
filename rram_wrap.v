
`timescale 1ns/1ps

module rram_wrap(
input         por_n               ,
input         clk                 ,
input    [1:0]sel                 ,
input         csa_b               ,//array
input         csr_b               ,//register
input         csb_b               ,//matrix b
input         rw_b                ,
input   [13:0]adr                 ,
input   [31:0]din                 ,
output  [31:0]dout                ,
input  [575:0]com0_a4bit          ,
output[1727:0]com0_a4bitxb        ,
input  [575:0]com1_a4bit          ,
output[1727:0]com1_a4bitxb        ,
input  [575:0]com2_a4bit          ,
output[1727:0]com2_a4bitxb        ,
input  [575:0]com3_a4bit          ,
output[1727:0]com3_a4bitxb        ,
output   [3:0]pass_b              ,
output   [3:0]busy_b               
);

wire [31:0]macro0_dout ;
wire [31:0]macro1_dout ;
wire [31:0]macro2_dout ;
wire [31:0]macro3_dout ;

wire macro0_csa_b  = (sel==2'd0) ? csa_b : 1'b1 ;
wire macro0_csr_b  = (sel==2'd0) ? csr_b : 1'b1 ;
wire macro0_csb_b  = csb_b ;

wire macro1_csa_b  = (sel==2'd1) ? csa_b : 1'b1 ;
wire macro1_csr_b  = (sel==2'd1) ? csr_b : 1'b1 ;
wire macro1_csb_b  = csb_b ;

wire macro2_csa_b  = (sel==2'd2) ? csa_b : 1'b1 ;
wire macro2_csr_b  = (sel==2'd2) ? csr_b : 1'b1 ;
wire macro2_csb_b  = csb_b ;

wire macro3_csa_b  = (sel==2'd3) ? csa_b : 1'b1 ;
wire macro3_csr_b  = (sel==2'd3) ? csr_b : 1'b1 ;
wire macro3_csb_b  = csb_b ;

assign dout = (sel==2'd3) ? macro3_dout :
                (sel==2'd2) ? macro2_dout :
                  (sel==2'd1) ? macro1_dout : macro0_dout ;

rram_macro u_macro0(
 .por_n        (por_n        ) ,
 .clk          (clk          ) ,
 .csa_b        (macro0_csa_b ) ,
 .csr_b        (macro0_csr_b ) ,
 .csb_b        (macro0_csb_b ) ,
 .rw_b         (rw_b         ) ,
 .adr          (adr          ) ,
 .din          (din          ) ,
 .dout         (macro0_dout  ) ,
 .a4bit        (com0_a4bit   ) ,
 .a4bitxb      (com0_a4bitxb ) ,
 .pass_b       (pass_b[0]    ) ,
 .busy_b       (busy_b[0]    )  
);


rram_macro u_macro1(
 .por_n        (por_n        ) ,
 .clk          (clk          ) ,
 .csa_b        (macro1_csa_b ) ,
 .csr_b        (macro1_csr_b ) ,
 .csb_b        (macro1_csb_b ) ,
 .rw_b         (rw_b         ) ,
 .adr          (adr          ) ,
 .din          (din          ) ,
 .dout         (macro1_dout  ) ,
 .a4bit        (com1_a4bit   ) ,
 .a4bitxb      (com1_a4bitxb ) ,
 .pass_b       (pass_b[1]    ) ,
 .busy_b       (busy_b[1]    )  
);

rram_macro u_macro2(
 .por_n        (por_n        ) ,
 .clk          (clk          ) ,
 .csa_b        (macro2_csa_b ) ,
 .csr_b        (macro2_csr_b ) ,
 .csb_b        (macro2_csb_b ) ,
 .rw_b         (rw_b         ) ,
 .adr          (adr          ) ,
 .din          (din          ) ,
 .dout         (macro2_dout  ) ,
 .a4bit        (com2_a4bit   ) ,
 .a4bitxb      (com2_a4bitxb ) ,
 .pass_b       (pass_b[2]    ) ,
 .busy_b       (busy_b[2]    )  
);

rram_macro u_macro3(
 .por_n        (por_n        ) ,
 .clk          (clk          ) ,
 .csa_b        (macro3_csa_b ) ,
 .csr_b        (macro3_csr_b ) ,
 .csb_b        (macro3_csb_b ) ,
 .rw_b         (rw_b         ) ,
 .adr          (adr          ) ,
 .din          (din          ) ,
 .dout         (macro3_dout  ) ,
 .a4bit        (com3_a4bit   ) ,
 .a4bitxb      (com3_a4bitxb ) ,
 .pass_b       (pass_b[3]    ) ,
 .busy_b       (busy_b[3]    )  
);

endmodule


module rram_macro(
input         por_n               ,
input         clk                 ,
input         csa_b               ,//array
input         csr_b               ,//register
input         csb_b               ,//matrix b
input         rw_b                ,
input   [13:0]adr                 ,
input   [31:0]din                 ,
output  [31:0]dout                ,
input  [575:0]a4bit               ,
output[1727:0]a4bitxb             ,
output        pass_b              ,
output        busy_b               
);

parameter tWRT = 100 ; //max 120us

integer i,j ;
reg [7:0]mem[255:0][143:0] ; //256row*144col*8bit

reg    [7:0]matrix_b[143:0] ;
reg    [3:0]matrix_a[143:0] ;
reg   [11:0]matrix_c[143:0] ;
reg [1727:0]matrix_c_pack   ;
reg   [31:0]dato = 0 ;
reg         pass = 1 ;
reg         busy = 1 ;             

initial begin
  pass  = 1 ;
  busy  = 1 ;
  for(i=0;i<256;i=i+1) 
   for(j=0;j<144;j=j+1)
    mem[i][j] <= #1 8'bxxxx_xxxx ;
  #1000;
  busy = 0 ;
end

assign pass_b = ~pass ;
assign busy_b = ~busy ;
assign dout   = dato  ;

wire      rram_rst_n = por_n ;

wire [7:0]row =  adr[7:0]  ;
wire [5:0]col =  adr[13:8] ;


assign a4bitxb = matrix_c_pack ;

always@(*) begin
  for(i=0;i<144;i=i+1) begin
    matrix_a[i] = a4bit[4*i+:4] ;
    matrix_c[i] = matrix_a[i]*matrix_b[i] ;
    matrix_c_pack[i*12+:12] = matrix_c[i] ;
  end
end

always@(posedge clk) begin
  if((~csa_b)&(~rw_b)) begin
    #1;busy = 1 ;
    #(tWRT*1000);
    busy = 0 ;
    mem[row][col*4+0] = din[7:0]  ;
    mem[row][col*4+1] = din[15:8] ;
    mem[row][col*4+2] = din[23:16];
    mem[row][col*4+3] = din[31:24];
  end
end

always@(*)
begin
  if(rram_rst_n) begin
    if((~csa_b)&rw_b) begin
      @(posedge clk); # 2 ; busy = 1 ;
      repeat(4)@(posedge clk) ;
      #5 ;
      busy = 0 ;
      dato = {mem[row][col*4+3],mem[row][col*4+2],mem[row][col*4+1],mem[row][col*4]} ;
    end
    if((~csb_b)&rw_b) begin
      @(posedge clk); # 2 ; busy = 1 ;
      repeat(4)@(posedge clk) ;
      #5 ;
      busy = 0 ;
      for(i=0;i<144;i=i+1) begin
        matrix_b[i] = mem[row][i] ;
      end
    end
  end
end

endmodule
