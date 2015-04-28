

module ODDR ( input wire D1, D2, 
              input wire C, CE, R, S,
              output wire Q );

              
reg Q1, Q2;

always@(posedge C)
    Q1 <= D1;
    
always@(negedge C)
    Q2 <= D2;

assign Q = C ? Q1 & CE : Q2 & CE;

endmodule
