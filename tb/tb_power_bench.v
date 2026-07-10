`timescale 1ns/1ps
// =====================================================================
//  tb_power_bench.v
//   power_bench_wrapper 구동 -> SAIF(토글) 기록용 시뮬레이션
//   clk만 넣으면 wrapper 내부 LFSR + 자동반복 FSM이 스스로 동작.
//   충분히 오래 돌려 여러 번의 행렬곱 토글(정상상태)을 확보한다.
// =====================================================================
module tb_power_bench;
    reg        CLK100MHZ = 1'b0;
    reg        rst_btn   = 1'b1;
    wire [7:0] led;

    // 100MHz 클럭 (주기 10ns)
    always #5 CLK100MHZ = ~CLK100MHZ;

    // 측정 대상 래퍼
    power_bench_wrapper dut (
        .CLK100MHZ (CLK100MHZ),
        .rst_btn   (rst_btn),
        .led       (led)
    );

    // led 변화 카운트(동작 확인용)
    reg [7:0] led_prev;
    integer   led_changes;
    initial led_changes = 0;
    always @(posedge CLK100MHZ) begin
        if (led !== led_prev) led_changes = led_changes + 1;
        led_prev <= led;
    end

    initial begin
        rst_btn = 1'b1;
        repeat (10) @(posedge CLK100MHZ);   // 리셋 유지
        rst_btn = 1'b0;                      // 리셋 해제 -> LFSR/반복 시작
        #20000;                              // 20us (2000 사이클) 지속 구동
        $display("=====================================");
        $display(" power_bench 구동 완료");
        $display(" led 변화 횟수 : %0d (0이 아니면 정상 토글)", led_changes);
        $display(" 최종 led = %h", led);
        $display("=====================================");
        $finish;
    end
endmodule
