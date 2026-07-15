import numpy as np

file_a = 'all_A.mem'
file_b = 'all_B.mem'
file_c_golden = 'all_C_golden.mem'

# 2. 8비트 16진수 리스트에서 상위 4비트(INT4)만 추출하여 4x4 행렬로 변환하는 함수
def hex_list_to_int4_matrix(hex_list):
    dec_list = []
    for x in hex_list:
        # 1. 먼저 8비트 정수로 읽어옵니다. (예: '1A' -> 26, 'D4' -> 212)
        val_8bit = int(x, 16)
        
        # 2. 상위 4비트(MSB 4-bit)만 추출합니다. 
        # (예: '1A'의 상위 4비트는 '1', 'D4'의 상위 4비트는 'D')
        val_4bit = (val_8bit >> 4) & 0xF
        
        # 3. 4-bit 부호 있는 정수(Signed INT4, 범위: -8 ~ +7)로 변환
        # 4비트 값이 7보다 크면(즉, 8 ~ 15/Hex 8 ~ F) 음수로 인식하여 16을 빼줍니다.
        if val_4bit > 7:
            val_signed = val_4bit - 16
        else:
            val_signed = val_4bit
            
        dec_list.append(val_signed)
        
    # dec_list를 numpy array로 변환 후 4x4 형태로 재배치
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

        # 각 파일 내의 8비트 줄에서 상위 4비트(INT4)만 가져와 matrix로 변환
        A = hex_list_to_int4_matrix(line_a.split())
        B = hex_list_to_int4_matrix(line_b.split())

        # Matrix Multiplication (INT4 x INT4) 수행
        C = np.matmul(A, B)
        
        print(f"=== Test Case {case_idx} (INT4 computation) ===")
        print(C)
        print()
        
        # C의 결과값은 16비트 부호 있는 정수(AW=16) 규격에 맞춰 16진수로 변환합니다.
        # 음수 처리를 위해 0xFFFF로 마스킹하고, zfill(4)를 통해 4자리(16비트)로 맞춥니다.
        c_hex_str = " ".join([hex(val & 0xFFFF)[2:].zfill(4).upper() for val in C.flatten()])
        
        fc.write(c_hex_str + "\n")
