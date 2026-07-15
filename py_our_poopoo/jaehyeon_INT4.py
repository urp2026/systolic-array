import numpy as np

file_a = 'all_A.mem'
file_b = 'all_B.mem'
file_c_golden = 'all_C_golden.mem'

# 2. INT4 16진수 문자열 리스트를 4x4 행렬로 변환하는 함수
def int4_hex_list_to_matrix(hex_list):
    
    # 4-bit 부호 있는 정수(2의 보수) 변환
    # 4비트 값(0~15) 중 7보다 크면(8~F) 16을 빼서 음수로 변환합니다.
    dec_list = [int(x, 16) - 16 if int(x, 16) > 7 else int(x, 16) for x in hex_list]
    
    return np.array(dec_list).reshape(4, 4)

# 3. 파일 읽기 및 처리
with open(file_a, 'r', encoding='utf-8') as fa, \
     open(file_b, 'r', encoding='utf-8') as fb, \
     open(file_c_golden, 'w', encoding='utf-8') as fc:
         
    for case_idx, (line_a, line_b) in enumerate(zip(fa, fb), start=1):
        line_a = line_a.strip()
        line_b = line_b.strip()

        # 파일 내에서 빈 줄이 있는지 검사
        if not line_a or not line_b:
            continue

        # 각 파일 내의 줄을 가져와 4x4 INT4 Matrix로 곧바로 변환
        A = int4_hex_list_to_matrix(line_a.split())
        B = int4_hex_list_to_matrix(line_b.split())

        # Matrix Multiplication (INT4 x INT4) 수행
        C = np.matmul(A, B)
        
        print(f"=== Test Case {case_idx} (Direct INT4) ===")
        print(C)
        print()
        
        # 출력 결과(C)는 하드웨어 규격(AW=16)에 맞추어 16비트 Hex(4자리) 형태로 기록합니다.
        c_hex_str = " ".join([hex(val & 0xFFFF)[2:].zfill(4).upper() for val in C.flatten()])
        
        fc.write(c_hex_str + "\n")
