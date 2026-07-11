`timescale 1ns/1ps

module tb_power_bench;
    reg        CLK100MHZ = 1'b0;
    reg        rst_btn   = 1'b1;
    wire [7:0] led;

    always #5 CLK100MHZ = ~CLK100MHZ;

    power_bench_wrapper dut (
        .CLK100MHZ (CLK100MHZ),
        .rst_btn   (rst_btn),
        .led       (led)
    );

    reg [7:0] led_prev;
    integer   led_changes;
    initial led_changes = 0;
    always @(posedge CLK100MHZ) begin
        if (led !== led_prev) led_changes = led_changes + 1;
        led_prev <= led;
    end

    initial begin
        rst_btn = 1'b1;
        repeat (10) @(posedge CLK100MHZ);
        rst_btn = 1'b0;
        #20000;
        $display("=====================================");
        $display(" power_bench 구동 완료");
        $display(" led 변화 횟수 : %0d (0이 아니면 정상 토글)", led_changes);
        $display(" 최종 led = %h", led);
        $display("=====================================");
        $finish;
    end
endmodule
