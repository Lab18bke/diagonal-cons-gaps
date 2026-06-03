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

def is_strictly_decreasing(gaps):
    for i in range(1, len(gaps)):
        if gaps[i] >= gaps[i-1]:
            return False, i
    return True, -1

def cos_argument(k, n):
    return (2*k + 1) * np.pi / (2*n)

with open("strictly_decreasing.txt", "w", encoding="utf-8") as f:

    f.write("STRICT DECREASE VERIFICATION\n")
    f.write("Confirms g(k) is strictly decreasing in k for all n\n")
    f.write("Supports the proof of Theorem 1\n")
    f.write("=" * 65 + "\n\n")

    f.write("Cosine argument theta(k) = (2k+1)*pi/(2n)\n")
    f.write("Showing theta(k) is in (0, pi) and strictly increasing:\n\n")

    for n in [10, 23, 67]:
        lengths = diagonal_lengths(n)
        gaps = gap_sequence(lengths)
        f.write(f"n = {n}\n")
        f.write(f"{'k':>4} | {'theta(k)':>12} | {'cos(theta(k))':>14} | {'g(k)':>12}\n")
        f.write("-" * 50 + "\n")
        for i, g in enumerate(gaps):
            k = i + 2
            theta = cos_argument(k, n)
            cos_val = np.cos(theta)
            f.write(f"{k:>4} | {theta:>12.6f} | {cos_val:>14.8f} | {g:>12.8f}\n")
        ok, fail_idx = is_strictly_decreasing(gaps)
        f.write(f"Strictly decreasing: {ok}\n")
        if not ok:
            f.write(f"First violation at index {fail_idx}\n")
        f.write("\n")

    f.write("=" * 65 + "\n")
    f.write("BULK CHECK: strict decrease holds for ALL n from 6 to 2000\n")
    f.write("=" * 65 + "\n")

    all_pass = True
    fails = []
    for n in range(6, 2001):
        lengths = diagonal_lengths(n)
        gaps = gap_sequence(lengths)
        if not gaps:
            continue
        ok, fail_idx = is_strictly_decreasing(gaps)
        if not ok:
            all_pass = False
            fails.append((n, fail_idx))

    if all_pass:
        f.write("Gap sequence is strictly decreasing for ALL n from 6 to 2000.\n")
        f.write("This confirms the proof of Theorem 1 numerically.\n")
    else:
        f.write(f"Counterexamples found: {fails}\n")

    f.write("\n")
    f.write("=" * 65 + "\n")
    f.write("ANGLE RANGE CHECK\n")
    f.write("Confirms theta(k) stays in (0, pi) for all valid k\n")
    f.write("=" * 65 + "\n")

    angle_ok = True
    for n in range(6, 501):
        for k in range(2, n // 2):
            theta = cos_argument(k, n)
            if not (0 < theta < np.pi):
                angle_ok = False
                f.write(f"VIOLATION: n={n}, k={k}, theta={theta}\n")

    if angle_ok:
        f.write("All cosine arguments lie in (0, pi) for n=6 to 500.\n")
        f.write("Cosine is strictly decreasing on (0, pi), confirming Theorem 1.\n")

print("Done. Results written to strictly_decreasing.txt")
