// Round robin arbiter

`timescale 1ns/1ps

module arbiter (
    input logic clk,
    input logic rst,
    input logic [3:0] req,
    output logic [3:0] grant
);


    typedef logic [1:0] Counter;
    Counter counter;

    always_ff @(posedge clk) begin
        if (rst) begin
            grant <= '0;
            counter <= '0;
        end else begin
            grant <= '0;

            if (req[counter]) begin
                grant[counter] <= 1;
                counter <= counter + 1;
            end else if (req[counter + 1]) begin
                grant[counter + 1] <= 1;
                counter <= counter + 2;
            end else if (req[counter + 2]) begin
                grant[counter + 2] <= 1;
                counter <= counter + 3;
            end else if (req[counter + 3]) begin
                grant[counter + 3] <= 1;
                counter <= counter;
            end
        end
    end

endmodule