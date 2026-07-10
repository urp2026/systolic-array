import numpy as np

N = 4
INPUT_BITS = 8
OUTPUT_BITS = 32

A_FILE = "all_A.mem"
B_FILE = "all_B.mem"
C_FILE = "all_C_golden.mem"


def hex_to_signed(hex_str, bits):
    hex_str = hex_str.strip()

    value = int(hex_str, 16)

    if value >= (1 << (bits - 1)):
        value -= (1 << bits)

    return value


def signed_to_hex(value, bits):
    if value < 0:
        value = (1 << bits) + value

    return f"{value:0{bits // 4}X}"


def read_mem_file(filename, bits):
    values = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            if line == "":
                continue

            # 주석 제거
            if "//" in line:
                line = line.split("//")[0].strip()

            if line == "":
                continue

            # 한 줄에 여러 hex 값이 있는 경우 처리
            tokens = line.split()

            for token in tokens:
                values.append(hex_to_signed(token, bits))

    return values


def main():
    A_values = read_mem_file(A_FILE, INPUT_BITS)
    B_values = read_mem_file(B_FILE, INPUT_BITS)

    print(f"A 원소 개수: {len(A_values)}")
    print(f"B 원소 개수: {len(B_values)}")

    if len(A_values) != len(B_values):
        raise ValueError(f"A와 B의 원소 개수가 다름: A={len(A_values)}, B={len(B_values)}")

    if len(A_values) % (N * N) != 0:
        raise ValueError(f"원소 개수가 16의 배수가 아님. 현재 {len(A_values)}개")

    num_tests = len(A_values) // (N * N)

    print(f"총 test case 개수: {num_tests}")

    all_C = []

    for t in range(num_tests):
        start = t * N * N
        end = start + N * N

        A = np.array(A_values[start:end], dtype=np.int32).reshape(N, N)
        B = np.array(B_values[start:end], dtype=np.int32).reshape(N, N)

        C = A @ B

        print(f"\n===== TEST {t} =====")
        print("A =")
        print(A)
        print("B =")
        print(B)
        print("C_golden =")
        print(C)

        for x in C.flatten():
            all_C.append(int(x))

    with open(C_FILE, "w") as f:
        for x in all_C:
            f.write(signed_to_hex(x, OUTPUT_BITS) + "\n")

    print(f"\n{C_FILE} 생성 완료")
    print(f"총 C 원소 개수: {len(all_C)}")


if __name__ == "__main__":
    main()
