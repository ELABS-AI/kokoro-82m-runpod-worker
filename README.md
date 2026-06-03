# elabs / Kokoro 82M TTS

[![Run on RunPod](https://runpod.io/badge/runpod-hub)](https://runpod.io/console/hub)

Lightweight **text-to-speech** with ~82M parameters, supporting multiple voices and languages. Fast inference with minimal GPU memory footprint — runs on virtually any GPU.

## Highlights

- **~82M parameters** — tiny model, big voice quality
- **Multi-voice** — multiple built-in voices (American, British, Japanese, Korean, Chinese, French)
- **Fast inference** — sub-second generation on RTX 4090 for short sentences
- **Minimal VRAM** — works on any GPU with ≥2GB VRAM (T4, L4, RTX 4090, etc.)
- **Configurable speed** — adjust speaking rate via `speed` parameter

## API

### Input
```json
{
  "input": {
    "text": "Hello, welcome to Kokoro 82M text-to-speech.",
    "voice": "af_bella",
    "speed": 1.0
  }
}
```

### Output
```json
{
  "audio_base64": "<base64 WAV>",
  "text": "Hello, welcome to Kokoro 82M text-to-speech.",
  "voice": "af_bella",
  "wall_time_s": 0.4
}
```

### Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | string | **required** | Input text to synthesize |
| `voice` | string | `"af_bella"` | Voice ID (e.g., `af_bella`, `am_adam`, `bf_emma`, `bm_george`, `jf_sakura`, `zf_xiaobei`, `ff_siwis`) |
| `speed` | float | `1.0` | Speaking speed multiplier (0.5–2.0) |

## GPU Requirements
- **Recommended**: Any GPU with ≥4GB VRAM (RTX 4090, L4, T4, etc.)
- **Minimum**: Any GPU with ≥2GB VRAM
- **CUDA**: 12.0+

## Benchmark
| GPU | Text Length | Time |
|---|---|---|
| RTX 4090 | Short (30 chars) | ~0.2s |
| RTX 4090 | Medium (200 chars) | ~0.5s |
| RTX 4090 | Long (1000 chars) | ~1.8s |
| T4 | Medium (200 chars) | ~1.2s |

## License
Apache-2.0
