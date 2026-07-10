import numpy as np

file_a = 'all_A.mem'
file_b = 'all_B.mem'
file_c_golden = 'all_C_golden.mem'

# 2. 16진수 문자열 리스트를 4x4 행렬로 변환하는 함수
def hex_list_to_matrix(hex_list):
    
    # 8-bit 부호 있는 정수(2의 보수) 변환
    dec_list = [int(x, 16) - 256 if int(x, 16) > 127 else int(x, 16) for x in hex_list]

    #8-bit이기에 16진수 0x80 ~ 0xFF는 음수가 아닌 양수로 인식됨 -> 코드상으로 이 수들을 음수로 바꿔줘야함
    #int(x,16) : x를 16진수로 인식해서 10진수로 출력
    #x가 127보다 크다면 (>=0x80) 256을 빼서 음수로 처리
    
    return np.array(dec_list).reshape(4, 4)

    #dec_list를 numpy가 계산 가능한 array로 변환 뒤 reshape 함수를 통해 4 by 4 array형태로 수정
    
# 3. 파일 읽기 및 처리
with open(file_a, 'r', encoding='utf-8') as fa, \
     open(file_b, 'r', encoding='utf-8') as fb, \
     open(file_c_golden, 'w', encoding='utf-8') as fc:
         
# '\'은 같은 기능을 수행하지만 줄을 구획해주기 위해 필요함
# with : pyhton에서는 file을 open하고 close하지 않으면 오류 발생 -> with문법을 사용하면 이 행이 실행된 이후 바로 file이 close됨 
     
    for case_idx, (line_a, line_b) in enumerate(zip(fa, fb), start=1):
    #enumerate : for문을 돌때마다 번호를 붙여서 내보냄(이 코드의 경우 case_idx에 번호 전달)
    #zip : fa, fb에 있는 각 줄을 묶어 각각 line_a, line_b로 전달함(같은 줄에 있는 것을 동시에 전달)
        
        line_a = line_a.strip()
        line_b = line_b.strip()

        #file내에서 중간에 비어있는 줄이 있는지 검
        if not line_a or not line_b:
            continue

        #각 file내의 줄 -> matrix 변환
        A = hex_list_to_matrix(line_a.split())
        B = hex_list_to_matrix(line_b.split())

        #matrix multiply 수행
        C = np.matmul(A, B)
        print(f"=== Test Case {case_idx} ===")
        print(C)
        print()
        
        c_hex_str = " ".join([hex(val & 0xFFFFFFFF)[2:].zfill(8).upper() for val in C.flatten()])
        
        #C.flatten() : matrix 형태의 C를 일자로 늘려서 저장
        #for문에서 val에 C의 각 원소가 들어감
        #val & 0xFFFFFFFF : 32bit로 val을 잘라냄
        #hex : 16진수로 변환
        #[2:] python에서 16진수로 변환시 생기는 0x를 잘라냄
        #.zfill() 길이가 8자리가 안된다면 앞에서부터 0으로 채움
        
        fc.write(c_hex_str + "\n")
