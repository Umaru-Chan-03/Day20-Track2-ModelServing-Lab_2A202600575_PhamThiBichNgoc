# Bonus — GPU-offload sweep

Model: `qwen2.5-1.5b-instruct-q4_k_m.gguf`  ·  threads: `4`

| -ngl | tg128 (tok/s) |
|--:|--:|
| 0 | 14.1 |
| 8 | 16.2 |
| 16 | 17.0 |
| 24 | 16.9 |
| 32 | 16.5 |
| 99 | 16.6 |

When the model fits in VRAM, `-ngl 99` (full offload) is fastest. When it doesn't, partial offload (`-ngl 16` or `-ngl 24`) keeps the most compute on the GPU while spilling weights to RAM — usually still beats CPU-only (`-ngl 0`). Watch for the curve flattening: after the layer count covers the model's actual depth, more `-ngl` does nothing.
