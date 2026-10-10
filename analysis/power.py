"""Power and sample-size for the paired non-inferiority test of C2 (interface context vs comparator).

Design: paired binary outcomes per instance (same instance, two arms). Let pi_d be the probability
the two arms disagree on an instance. Under H0 of a true difference 0, the paired difference
d = p_A1 - p_comp has SE ~= sqrt(pi_d / n). Non-inferiority at margin eps (one-sided alpha) is
declared when the lower bound of the (1 - 2*alpha) CI exceeds -eps, i.e. d_hat > -eps + z_a * SE.
Power at true difference 0: P(d_hat > -eps + z_a*SE) = Phi((eps - z_a*SE)/SE) = Phi(eps/SE - z_a).
Required n for power 1-beta: n = pi_d * (z_a + z_b)^2 / eps^2.

With k samples per cell, per-instance success probabilities are estimated and pi_d shrinks roughly
as the per-instance flip rate falls; we report a sensitivity table over pi_d instead of assuming.

Usage: python power.py [--eps 0.05 0.10] [--pid 0.10 0.15 0.20] [--n 100 200 300]
"""
import argparse, math

def Phi(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def z(p):  # inverse normal via bisection (no scipy dependency)
    lo, hi = -10, 10
    for _ in range(100):
        mid = (lo + hi) / 2
        if Phi(mid) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def power(n, pid, eps, alpha=0.05):
    se = math.sqrt(pid / n); return Phi(eps / se - z(1 - alpha))

def n_required(pid, eps, alpha=0.05, beta=0.2):
    return math.ceil(pid * (z(1 - alpha) + z(1 - beta)) ** 2 / eps ** 2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eps", type=float, nargs="+", default=[0.05, 0.075, 0.10])
    ap.add_argument("--pid", type=float, nargs="+", default=[0.10, 0.15, 0.20, 0.30])
    ap.add_argument("--n", type=int, nargs="+", default=[100, 150, 200, 300, 400])
    a = ap.parse_args()
    print("Power at true difference 0, one-sided alpha=0.05")
    print(f"{'eps':>6} {'pi_d':>6} " + " ".join(f"n={n:<4d}" for n in a.n) + "   n for 80% power")
    for eps in a.eps:
        for pid in a.pid:
            row = " ".join(f"{power(n, pid, eps):6.2f}" for n in a.n)
            print(f"{eps:6.3f} {pid:6.2f} {row}   {n_required(pid, eps):d}")

if __name__ == "__main__":
    main()
