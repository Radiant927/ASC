import torch
import time

def test_gpu_gemm(N):
    A = torch.randn(N, N, device="cuda", dtype=torch.float32)
    B = torch.randn(N, N, device="cuda", dtype=torch.float32)
    # GPU 预热
    for _ in range(3):
        _ = A @ B
    torch.cuda.synchronize()
    start = time.time()
    C = A @ B
    torch.cuda.synchronize()
    t = time.time() - start
    gflops = (2 * N**3) / t / 1e9
    print(f"[GPU] Size={N:5d}, Time={t:.3f}s, GFLOPS={gflops:.2f}")

if __name__ == "__main__":
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    for n in [2048, 4096, 8192]:
        test_gpu_gemm(n)
