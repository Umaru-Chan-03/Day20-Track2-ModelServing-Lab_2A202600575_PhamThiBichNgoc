# Bonus — Thread sweep

Model: `qwen2.5-1.5b-instruct-q4_k_m.gguf`  ·  GPU layers: `99`

| threads | tg128 (tok/s) |
|---:|---:|
| 1 | 8.9 |
| 2 | 14.5 |
| 4 | 19.4 |
| 8 | 20.5 |
| 16 | 17.0 |

**Best**: `-t 8` at 20.5 tok/s.

Look at the curve. If it peaks around your **physical** core count and drops as you go higher, that's the memory-bandwidth ceiling: extra threads fight over the same memory channels and slow each other down.
