import numpy as np
import time

def test_cpu_gemm(N):
    A = np.random.rand(N, N).astype(np.float64)
    B = np.random.rand(N, N).astype(np.float64)
    # 预热
    _ = A @ B
    start = time.time()
    C = A @ B
    t = time.time() - start
    gflops = (2 * N**3) / t / 1e9
    print(f"[CPU] Size={N:5d}, Time={t:.3f}s, GFLOPS={gflops:.2f}")

if __name__ == "__main__":
    for n in [1024, 2048, 4096]:
        test_cpu_gemm(n)
