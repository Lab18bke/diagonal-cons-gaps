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

def gap_ratio(n):
    lengths = diagonal_lengths(n)
    gaps = gap_sequence(lengths)
    if not gaps:
        return None, None, None
    g_max = max(gaps)
    g_min = min(gaps)
    if g_min <= 0:
        return None, None, None
    return g_max, g_min, g_max / g_min

with open("paper_table.txt", "w", encoding="utf-8") as f:

    f.write("TABLE FOR PAPER\n")
    f.write("n | g(2) | g(floor(n/2)-1) | g(2) / g_min\n")
    f.write("=" * 60 + "\n")
    f.write(f"{'n':>6} | {'g(2)':>10} | {'g_min':>10} | {'ratio':>10}\n")
    f.write("-" * 46 + "\n")

    for n in [10, 23, 67, 97, 128]:
        g_max, g_min, ratio = gap_ratio(n)
        f.write(f"{n:>6} | {g_max:>10.5f} | {g_min:>10.5f} | {ratio:>10.3f}\n")

    f.write("\n")
    f.write("=" * 60 + "\n")
    f.write("FULL DATA: n from 6 to 200\n")
    f.write("=" * 60 + "\n")
    f.write(f"{'n':>5} | {'g_max':>12} | {'g_min':>12} | {'ratio':>10} | {'max at pos 1':>14}\n")
    f.write("-" * 62 + "\n")

    for n in range(6, 201):
        lengths = diagonal_lengths(n)
        gaps = gap_sequence(lengths)
        if not gaps:
            continue
        g_max = max(gaps)
        g_min = min(gaps)
        ratio = g_max / g_min
        max_pos = gaps.index(g_max) + 1
        f.write(f"{n:>5} | {g_max:>12.8f} | {g_min:>12.8f} | {ratio:>10.5f} | {str(max_pos == 1):>14}\n")

print("Done. Results written to paper_table.txt")
