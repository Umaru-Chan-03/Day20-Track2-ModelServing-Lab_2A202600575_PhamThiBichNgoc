# Bonus — batch-size sweep (prefill)

Model: `qwen2.5-1.5b-instruct-q4_k_m.gguf`  ·  threads: `4`  ·  n_gpu: `99`

| -b (logical) | -ub (micro) | pp512 (tok/s) |
|--:|--:|--:|
| 128 | 128 | 59.3 |
| 256 | 256 | 62.9 |
| 512 | 256 | 62.6 |
| 512 | 512 | 63.4 |
| 1024 | 512 | 64.4 |
| 2048 | 512 | 62.7 |

Larger batch lets prefill amortize per-step overhead (better tok/s) but also blocks the engine for longer (worse TTFT for queued requests). On a real serving stack you'd pick `--ubatch` based on the longest TTFT you can tolerate per slot under contention — exactly the chunked-prefill conversation from the deck.
