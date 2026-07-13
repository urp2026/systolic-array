## 1. 100MHz 시스템 클럭
set_property -dict { PACKAGE_PIN E3    IOSTANDARD LVCMOS33 } [get_ports CLK100MHZ]
create_clock -add -name sys_clk -period 10.000 -waveform {0 5} [get_ports CLK100MHZ]

## 2. 버튼
set_property -dict { PACKAGE_PIN N17   IOSTANDARD LVCMOS33 } [get_ports btnC] ;# 연산 시작 (start)
set_property -dict { PACKAGE_PIN M18   IOSTANDARD LVCMOS33 } [get_ports btnU] ;# 시스템 리셋 (rst)

## 3. 비동기 버튼 입력은 타이밍 분석(Fmax)에서 제외
set_false_path -from [get_ports btnC]
set_false_path -from [get_ports btnU]

## 4. 슬라이드 스위치 SW[15:0] 전체
##    (코드에서 SW[15:0] 포트를 선언하므로 16개 모두 제약 — 미사용 핀도 포함)
##    주의: SW8, SW9는 보드 회로상 1.8V 뱅크라 LVCMOS18이 맞음
set_property -dict { PACKAGE_PIN J15   IOSTANDARD LVCMOS33 } [get_ports {SW[0]}]  ;# 원소 인덱스 bit0
set_property -dict { PACKAGE_PIN L16   IOSTANDARD LVCMOS33 } [get_ports {SW[1]}]  ;# 원소 인덱스 bit1
set_property -dict { PACKAGE_PIN M13   IOSTANDARD LVCMOS33 } [get_ports {SW[2]}]  ;# 원소 인덱스 bit2
set_property -dict { PACKAGE_PIN R15   IOSTANDARD LVCMOS33 } [get_ports {SW[3]}]  ;# 원소 인덱스 bit3
set_property -dict { PACKAGE_PIN R17   IOSTANDARD LVCMOS33 } [get_ports {SW[4]}]
set_property -dict { PACKAGE_PIN T18   IOSTANDARD LVCMOS33 } [get_ports {SW[5]}]
set_property -dict { PACKAGE_PIN U18   IOSTANDARD LVCMOS33 } [get_ports {SW[6]}]
set_property -dict { PACKAGE_PIN R13   IOSTANDARD LVCMOS33 } [get_ports {SW[7]}]
set_property -dict { PACKAGE_PIN T8    IOSTANDARD LVCMOS18 } [get_ports {SW[8]}]
set_property -dict { PACKAGE_PIN U8    IOSTANDARD LVCMOS18 } [get_ports {SW[9]}]
set_property -dict { PACKAGE_PIN R16   IOSTANDARD LVCMOS33 } [get_ports {SW[10]}]
set_property -dict { PACKAGE_PIN T13   IOSTANDARD LVCMOS33 } [get_ports {SW[11]}]
set_property -dict { PACKAGE_PIN H6    IOSTANDARD LVCMOS33 } [get_ports {SW[12]}]
set_property -dict { PACKAGE_PIN U12   IOSTANDARD LVCMOS33 } [get_ports {SW[13]}]
set_property -dict { PACKAGE_PIN U11   IOSTANDARD LVCMOS33 } [get_ports {SW[14]}]
set_property -dict { PACKAGE_PIN V10   IOSTANDARD LVCMOS33 } [get_ports {SW[15]}] ;# 데이터셋 선택 (test1/test2)

## 5. 7-세그먼트 세그먼트 — seg[0]=CA ... seg[6]=CG (active low)
##    ★ 수정된 부분: 코드의 디코더 패턴(예: 0 = 7'b1000000, seg[6]=CG만 off)과
##      일치하도록 인덱스 순서를 교정
set_property -dict { PACKAGE_PIN T10   IOSTANDARD LVCMOS33 } [get_ports {seg[0]}] ;# CA (위)
set_property -dict { PACKAGE_PIN R10   IOSTANDARD LVCMOS33 } [get_ports {seg[1]}] ;# CB (오른쪽 위)
set_property -dict { PACKAGE_PIN K16   IOSTANDARD LVCMOS33 } [get_ports {seg[2]}] ;# CC (오른쪽 아래)
set_property -dict { PACKAGE_PIN K13   IOSTANDARD LVCMOS33 } [get_ports {seg[3]}] ;# CD (아래)
set_property -dict { PACKAGE_PIN P15   IOSTANDARD LVCMOS33 } [get_ports {seg[4]}] ;# CE (왼쪽 아래)
set_property -dict { PACKAGE_PIN T11   IOSTANDARD LVCMOS33 } [get_ports {seg[5]}] ;# CF (왼쪽 위)
set_property -dict { PACKAGE_PIN L18   IOSTANDARD LVCMOS33 } [get_ports {seg[6]}] ;# CG (가운데)
set_property -dict { PACKAGE_PIN H15   IOSTANDARD LVCMOS33 } [get_ports dp]

## 6. 7-세그먼트 자리 선택 애노드 an[7:0] (active low, an[0]=가장 오른쪽 자리)
set_property -dict { PACKAGE_PIN J17   IOSTANDARD LVCMOS33 } [get_ports {an[0]}] ;# 1의 자리
set_property -dict { PACKAGE_PIN J18   IOSTANDARD LVCMOS33 } [get_ports {an[1]}] ;# 10의 자리
set_property -dict { PACKAGE_PIN T9    IOSTANDARD LVCMOS33 } [get_ports {an[2]}] ;# 100의 자리
set_property -dict { PACKAGE_PIN J14   IOSTANDARD LVCMOS33 } [get_ports {an[3]}] ;# 부호(-) 자리
set_property -dict { PACKAGE_PIN P14   IOSTANDARD LVCMOS33 } [get_ports {an[4]}]
set_property -dict { PACKAGE_PIN T14   IOSTANDARD LVCMOS33 } [get_ports {an[5]}]
set_property -dict { PACKAGE_PIN K2    IOSTANDARD LVCMOS33 } [get_ports {an[6]}]
set_property -dict { PACKAGE_PIN U13   IOSTANDARD LVCMOS33 } [get_ports {an[7]}]
