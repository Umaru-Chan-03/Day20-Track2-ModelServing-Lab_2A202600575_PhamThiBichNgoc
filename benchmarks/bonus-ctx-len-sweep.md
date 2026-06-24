# Bonus — Context-length sweep (prefill cost)

Model: `qwen2.5-1.5b-instruct-q4_k_m.gguf`  ·  threads: `4`  ·  n_gpu: `99`

| ctx tokens | pp (tok/s) | prefill latency (ms) |
|--:|--:|--:|
| 128 | 62.5 | 2049.3 |
| 256 | 62.9 | 4068.0 |
| 512 | 63.9 | 8015.0 |
| 1024 | 61.4 | 16677.5 |
| 2048 | 57.6 | 35549.4 |

Prefill scales **super-linearly** with context length — that's where TTFT comes from in long-context RAG. This is also why the deck's *disaggregated prefill/decode* pattern (Mooncake / llm-d / Dynamo) exists: give prefill its own GPU pool so long-context requests don't block decode.
