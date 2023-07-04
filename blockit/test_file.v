module sparse_adder64 
(
  input [63:0] A,
  input [63:0] B,
  output [63:0] SUM,
  output CO
);

  // 64 = 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 + (11-1)
  wire carry_interconnect[10:0];
  assign carry_interconnect[0] = 1'b0;

  genvar i;
  generate

    for (i = 2; i <= 10; i=i+1) begin : adder_instance
      select_adder #(.COUNT(i)) sel(
        .A(A[end_calculate(i):start_calculate(i)]),
        .B(B[end_calculate(i):start_calculate(i)]),
        .Cin(carry_interconnect[i-2]),
        .S(SUM[end_calculate(i):start_calculate(i)]),
        .Cout(carry_interconnect[i-1])
      );
    end
  endgenerate
  
    select_adder #(.COUNT(10)) sel(
    .A(A[63:54]),
    .B(B[63:54]),
    .Cin(carry_interconnect[9]),
    .S(SUM[63:54]),
    .Cout(carry_interconnect[10])
  );

  assign CO = carry_interconnect[10];

  function integer start_calculate;
    input integer x;
    start_calculate = x*(x-1)/2 -1;
  endfunction

  function integer end_calculate;
    input integer x;
    end_calculate = x*(x-1)/2 +x -2;
  endfunction

endmodule

