import numpy as np

def diagonal_lengths(n, R=1):
    lengths = []
    for k in range(2, n // 2 + 1):
        lengths.append((k, 2 * R * np.sin(k * np.pi / n)))
    return lengths

def gap_sequence(lengths):
    gaps = []
    for i in range(1, len(lengths)):
        gaps.append(lengths[i][1] - lengths[i-1][1])
    return gaps

def gap_formula(k, n, R=1):
    return 4 * R * np.cos((2*k + 1) * np.pi / (2*n)) * np.sin(np.pi / (2*n))

def verify_formula(n):
    lengths = diagonal_lengths(n)
    gaps = gap_sequence(lengths)
    results = []
    for i, g in enumerate(gaps):
        k = i + 2
        formula_val = gap_formula(k, n)
        error = abs(g - formula_val)
        results.append((k, round(g, 10), round(formula_val, 10), error))
    return results

def check_max_at_position_1(n):
    lengths = diagonal_lengths(n)
    gaps = gap_sequence(lengths)
    if not gaps:
        return True, 0
    max_pos = gaps.index(max(gaps)) + 1
    return max_pos == 1, max_pos

with open("gap_formula_results.txt", "w", encoding="utf-8") as f:

    f.write("GAP FORMULA VERIFICATION\n")
    f.write("g(k) = 4*cos((2k+1)*pi/(2n)) * sin(pi/(2n))\n")
    f.write("=" * 65 + "\n\n")

    for n in [10, 23, 67, 97, 128, 200, 500]:
        f.write(f"n = {n}\n")
        f.write(f"{'k':>4} | {'Actual gap':>14} | {'Formula val':>14} | {'Error':>12}\n")
        f.write("-" * 50 + "\n")
        for k, actual, formula, error in verify_formula(n):
            f.write(f"{k:>4} | {actual:>14.10f} | {formula:>14.10f} | {error:>12.2e}\n")
        t1_ok, pos = check_max_at_position_1(n)
        f.write(f"Max gap at position 1: {t1_ok} (actual position: {pos})\n\n")

    f.write("=" * 65 + "\n")
    f.write("THEOREM 1 VERIFICATION: all n from 6 to 2000\n")
    f.write("=" * 65 + "\n")
    all_pass = True
    fails = []
    for n in range(6, 2001):
        ok, pos = check_max_at_position_1(n)
        if not ok:
            all_pass = False
            fails.append((n, pos))
    if all_pass:
        f.write("Theorem 1 holds for ALL n from 6 to 2000.\n")
        f.write("Max gap is always at position 1 without exception.\n")
    else:
        f.write(f"FAILS for: {fails}\n")

print("Done. Results written to gap_formula_results.txt")
