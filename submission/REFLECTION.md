# Reflection — Lab 20 (Personal Report)

> **Đây là báo cáo cá nhân.** Mỗi học viên chạy lab trên laptop của mình, với spec của mình. Số liệu của bạn không so sánh được với bạn cùng lớp — chỉ so sánh **before vs after trên chính máy bạn**. Grade rubric tính theo độ rõ ràng của setup + tuning của bạn, không phải tốc độ tuyệt đối.

---

**Họ Tên:** _<Họ Tên>_
**Cohort:** _<A20-K1 / A20-K2 / ...>_
**Ngày submit:** _<YYYY-MM-DD>_

---

## 1. Hardware spec (từ `00-setup/detect-hardware.py`)

> Paste output của `python 00-setup/detect-hardware.py` vào đây, hoặc điền thủ công:

- **OS:** _<macOS 14 / Windows 11 / Ubuntu 24.04 / ...>_
- **CPU:** _<Apple M2 / Intel i7-12700H / AMD Ryzen 7 5800H / ...>_
- **Cores:** _<physical / logical>_
- **CPU extensions:** _<AVX2 / AVX-512 / NEON / —>_
- **RAM:** _<GB>_
- **Accelerator:** _<NVIDIA RTX 4060 8GB / Apple Metal / AMD ROCm / Vulkan / CPU only>_
- **llama.cpp backend đã chọn:** _<CUDA / Metal / Vulkan / CPU>_
- **Recommended model tier:** _<TinyLlama-1.1B / Qwen2.5-1.5B / Llama-3.2-3B / Qwen2.5-7B>_

**Setup story** (≤ 80 chữ): những gì cần thay đổi để lab chạy được trên máy bạn (vd: dùng WSL2, install CUDA Toolkit, fall back sang Vulkan vì ROCm phiên bản kén, tắt antivirus để pip install nhanh hơn, v.v.):

_Answer here._

---

## 2. Track 01 — Quickstart numbers (từ `benchmarks/01-quickstart-results.md`)

> Paste bảng từ `benchmarks/01-quickstart-results.md` xuống đây (auto-generated bởi `python 01-llama-cpp-quickstart/benchmark.py`).

| Model | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | E2E P50/P95/P99 (ms) | Decode rate (tok/s) |
|---|--:|--:|--:|--:|--:|
| (Q4_K_M) | | | | | |
| (Q2_K)   | | | | | |

**Một quan sát** (≤ 50 chữ): Q4_K_M vs Q2_K trên máy bạn — số liệu nói gì? Quality đáng đánh đổi không?

_Answer here._

---

## 3. Track 02 — llama-server load test

> Chạy 2 lần locust ở concurrency 10 và 50, paste tóm tắt bên dưới.

| Concurrency | Total RPS | TTFB P50 (ms) | E2E P95 (ms) | E2E P99 (ms) | Failures |
|--:|--:|--:|--:|--:|--:|
| 10 | | | | | |
| 50 | | | | | |

**Batching observation** (từ `record-metrics.py`): peak `llamacpp:n_busy_slots_per_decode` / `requests_processing` ở concurrency 50 = _<…>_, nghĩa là …

_Answer here._

---

## 4. Track 03 — Milestone integration

- **N16 (Cloud/IaC):** _<piece you connected — k3d cluster / GCP project / docker-compose / "stub: localhost only">_
- **N17 (Data pipeline):** _<piece — Airflow DAG / batch job / "stub: in-memory dict">_
- **N18 (Lakehouse):** _<piece — Delta Lake table / Iceberg / "stub: SQLite">_
- **N19 (Vector + Feature Store):** _<piece — Qdrant index / Feast / "stub: TOY_DOCS">_

**Nơi tốn nhiều ms nhất** trong pipeline (đo bằng `time.perf_counter` trong `pipeline.py`):

- embed: _<ms>_
- retrieve: _<ms>_
- llama-server: _<ms>_

**Reflection** (≤ 60 chữ): bottleneck nằm ở đâu? Có khớp với kỳ vọng không?

_Answer here._

---

## 5. Bonus — The single change that mattered most

> **Most important section.** Pick **một** thay đổi từ bonus track (build flag, thread sweep, quant pick, GPU offload, KV-cache quantization, speculative decoding, bất cứ challenge nào trong `BONUS-llama-cpp-optimization/CHALLENGES.md`) đã tạo ra speedup lớn nhất trên máy bạn.

**Change:** `Tối ưu hóa số lượng CPU thread (-t 8 so với -t 1)`

**Before vs after** (paste 2-3 dòng từ sweep output):

```
before: t=  1  tg64=   8.9 tok/s
after:  t=  8  tg64=  20.5 tok/s
speedup: ~2.30×
```

**Tại sao nó work** (1–2 đoạn ngắn — đây là phần grader đọc kỹ nhất):

Việc tăng số lượng luồng từ 1 lên 8 giúp tận dụng tốt hơn 4 nhân vật lý (8 nhân logic/luồng ảo) của CPU Intel i7-6820HQ để thực hiện song song các phép tính nhân ma trận (GEMM) trong quá trình tự hồi quy của mô hình. Một luồng đơn lẻ hoàn toàn không thể khai thác hết hiệu năng đa nhân cũng như băng thông RAM của hệ thống.

Tuy nhiên, tốc độ giải mã không tăng tuyến tính theo số nhân (8 luồng chỉ đạt 20.5 tok/s, tăng 2.3× chứ không phải 8×) và sụt giảm đáng kể xuống còn 17.0 tok/s khi tăng lên 16 luồng (oversubscription). Điều này chứng minh quá trình sinh token (decode phase) cực kỳ bị giới hạn bởi băng thông bộ nhớ (memory-bandwidth bound) hơn là giới hạn tính toán (compute-bound). Khi chạy quá nhiều luồng ảo hoặc vượt quá cấu hình phần cứng thực tế, các nhân xử lý sẽ phải tranh chấp băng thông bus bộ nhớ RAM và làm mất dữ liệu cache liên tục (cache thrashing), dẫn tới thời gian chờ tăng và hiệu năng tổng thể bị sụt giảm.


---

## 6. (Optional) Điều ngạc nhiên nhất

_(1–2 câu — không bắt buộc, nhưng người grader đọc tất cả)_

_Answer here._

---

## 7. Self-graded checklist

- [ ] `hardware.json` đã commit
- [ ] `models/active.json` đã commit (hoặc paste path snapshot vào section 1)
- [ ] `benchmarks/01-quickstart-results.md` đã commit
- [ ] `benchmarks/02-server-results.md` (hoặc CSV từ `record-metrics.py`) đã commit
- [ ] `benchmarks/bonus-*.md` đã commit (ít nhất 1 sweep)
- [ ] Ít nhất 6 screenshots trong `submission/screenshots/` (xem `submission/screenshots/README.md`)
- [ ] `make verify` exit 0 (chạy ngay trước khi push)
- [ ] Repo trên GitHub ở chế độ **public**
- [ ] Đã paste public repo URL vào VinUni LMS

---

**Quan trọng:** repo phải **public** đến khi điểm được công bố. Nếu private, grader không xem được → 0 điểm.
