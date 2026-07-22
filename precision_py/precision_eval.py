import numpy as np

N     = 4
NCASE = 15

CONFIGS = {4: 16, 8: 32, 16: 64}


def mat_to_hex(mat, bits):
    mask   = (1 << bits) - 1
    digits = bits // 4
    return " ".join(f"{int(v) & mask:0{digits}X}" for v in mat.flatten())


# ========== Part 1 : RTL 검증용 케이스 ==========
def build_cases(bits):
    """sparse 5 / boundary 5 / random 5"""
    qmax = (1 << (bits - 1)) - 1        # +7 / +127 / +32767
    qmin = -(1 << (bits - 1))           # -8 / -128 / -32768
    rng  = np.random.default_rng(42)    # 정밀도 무관하게 같은 구조
    C    = []

    def ri(shape):
        return rng.integers(qmin, qmax + 1, shape).astype(np.int64)

    # --- sparse ---
    for density in (0.25, 0.50, 0.75):
        A = np.where(rng.random((N, N)) < density, ri((N, N)), 0)
        B = np.where(rng.random((N, N)) < density, ri((N, N)), 0)
        C.append((A, B))

    C.append((np.eye(N, dtype=np.int64) * qmax, ri((N, N))))          # 대각

    A = np.zeros((N, N), dtype=np.int64); A[1, 2] = qmin
    B = np.zeros((N, N), dtype=np.int64); B[2, 3] = qmin
    C.append((A, B))                                                  # 단일 원소

    # --- boundary ---
    F = lambda v: np.full((N, N), v, dtype=np.int64)
    C.append((F(qmax), F(qmax)))                                      # +max x +max
    C.append((F(qmin), F(qmin)))                                      # -min x -min → |C|max
    C.append((F(qmin), F(qmax)))                                      # 부호 혼합
    C.append((F(qmin), np.eye(N, dtype=np.int64)))                    # 부호 확장
    C.append((np.tile([qmin, qmax, -1, 1], (N, 1)).astype(np.int64),
              np.tile([[qmax], [qmin], [1], [-1]], (1, N)).astype(np.int64)))

    # --- random ---
    for _ in range(5):
        C.append((ri((N, N)), ri((N, N))))

    return C


def gen_mem():
    print("=" * 58)
    print(" Part 1 : RTL 검증용 .mem 생성")
    print("=" * 58)

    for bits, aw in CONFIGS.items():
        cases   = build_cases(bits)
        max_abs = 0

        with open(f'A_int{bits}.mem', 'w') as fa, \
             open(f'B_int{bits}.mem', 'w') as fb, \
             open(f'C_int{bits}_golden.mem', 'w') as fc:

            for A, B in cases:
                Cm = A @ B                       # 반드시 양자화된 A, B로
                max_abs = max(max_abs, int(np.abs(Cm).max()))
                fa.write(mat_to_hex(A,  bits) + "\n")
                fb.write(mat_to_hex(B,  bits) + "\n")
                fc.write(mat_to_hex(Cm, aw)   + "\n")

        need = int(max_abs).bit_length() + 1
        ok   = "OK" if need <= aw else "← AW 부족!"
        print(f" INT{bits:<2}  DW={bits:<2} AW={aw:<2}  "
              f"|C|max={max_abs:<12} 필요={need:>2}bit  {ok}")
        print(f"        A_int{bits}.mem / B_int{bits}.mem / "
              f"C_int{bits}_golden.mem  ({NCASE}줄 x {N*N}워드)")


# ========== Part 2 : SQNR ==========
def quantize(x, bits):
    qmax = (1 << (bits - 1)) - 1
    s    = np.abs(x).max() / qmax
    q    = np.clip(np.round(x / s), -qmax - 1, qmax).astype(np.int64)
    return q, s


def sqnr(ref, out):
    return 10 * np.log10((ref ** 2).sum() / ((ref - out) ** 2).sum())


def acc_report(size=64, trials=20):
    print()
    print("=" * 58)
    print(f" Part 2 : 정확도 (FP32 기준, {size}x{size} x {trials}회 평균)")
    print("=" * 58)
    rng = np.random.default_rng(0)

    acc = {b: [] for b in CONFIGS}
    for _ in range(trials):
        A_fp  = rng.standard_normal((size, size))
        B_fp  = rng.standard_normal((size, size))
        C_ref = A_fp @ B_fp                       # FP32 ground truth

        for bits in CONFIGS:
            qa, sa = quantize(A_fp, bits)
            qb, sb = quantize(B_fp, bits)
            C_deq  = (qa @ qb) * sa * sb          # 정수연산 → 역양자화
            acc[bits].append(sqnr(C_ref, C_deq))

    print(f" {'bits':>5} {'SQNR(dB)':>10} {'이론(6.02/bit)':>15} {'INT8 대비':>12}")
    base = np.mean(acc[8])
    for bits in CONFIGS:
        m = np.mean(acc[bits])
        print(f" {bits:>5} {m:>10.2f} {6.02*bits - 6.6:>15.1f} "
              f"{m - base:>+11.1f}")
    print()
    print(" * SQNR은 round()에서 발생 — Vivado가 아니라 여기서만 측정됨")
    print(" * Part 1이 전부 PASS여야 이 숫자가 곧 HW 정확도임")


if __name__ == '__main__':
    gen_mem()
    acc_report()
