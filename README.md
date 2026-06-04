# elabs / Kokoro 82M TTS

[![Deploy on RunPod](https://img.shields.io/badge/RunPod-Deploy-orange?logo=runpod)](https://console.runpod.io/hub)
[![CUDA 12.4](https://img.shields.io/badge/CUDA-12.4-green)](https://developer.nvidia.com/cuda-toolkit)
[![Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue)](https://opensource.org/licenses/Apache-2.0)

Lightweight **text-to-speech** synthesis with ~82M parameters. 14 built-in voices across 9 languages (English, Japanese, Chinese, Korean, French, Spanish, Hindi, Italian, Portuguese). Sub-second generation on any modern GPU.

![Kokoro TTS](https://pub-796a08821c1c483aaf5e274e0d03e350.r2.dev/hub-icons/kokoro.svg)

## Highlights

- ~82M parameters -- tiny footprint, high voice quality
- 14 voices -- American/British English, Japanese, Chinese, Korean, French + more
- Fast inference -- sub-second for short sentences on RTX 4090
- Low VRAM -- runs on any GPU with >=4GB VRAM (T4, L4, RTX 4090)
- Configurable speed -- 0.5x to 2.0x speaking rate

## Quick Start

```bash
curl -X POST https://api.runpod.ai/v2/{ENDPOINT_ID}/run \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"text": "Hello world", "voice": "af_bella"}}'
```

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

### Voices

| Voice ID | Language | Gender | Style |
|---|---|---|---|
| `af_bella` | English (US) | F | Warm, clear narration |
| `af_heart` | English (US) | F | Friendly, expressive |
| `am_adam` | English (US) | M | Professional |
| `bf_emma` | English (UK) | F | British neutral |
| `bm_george` | English (UK) | M | British authoritative |
| `jf_sakura` | Japanese | F | Natural Japanese |
| `zf_xiaobei` | Chinese | F | Mandarin female |
| `ff_siwis` | French | F | French natural |

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | string | required | Text to synthesize (max 5000 chars) |
| `voice` | string | `af_bella` | Voice ID |
| `speed` | float | `1.0` | Speaking rate (0.5-2.0) |

## GPU Requirements

- Minimum: >=2GB VRAM
- Recommended: RTX 4090, L4, T4 (>=4GB VRAM)
- CUDA: 12.4+

## Benchmarks

| GPU | 200 chars | 1000 chars |
|---|---|---|
| RTX 4090 | ~0.5s | ~1.8s |
| L4 | ~0.8s | ~3.0s |
| T4 | ~1.2s | ~4.5s |

## License

Apache-2.0. Based on [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M).
