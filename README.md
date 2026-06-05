# elabs / Kokoro 82M TTS

Kokoro 82M lightweight TTS supporting 9 languages. Fast inference with high-quality audio output.

[![Docker Build](https://github.com/ELABS-AI/kokoro-82m-runpod-worker/actions/workflows/build.yml/badge.svg)](https://github.com/ELABS-AI/kokoro-82m-runpod-worker/actions/workflows/build.yml)

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MODEL_ID` | `hexgrad/Kokoro-82M` | HuggingFace model ID |
| `HF_HOME` | `/runpod-volume/models/huggingface` | HuggingFace cache directory |
| `HUGGINGFACE_HUB_CACHE` | `/runpod-volume/models/huggingface/hub` | HuggingFace hub cache |

## Input

```json
{"input": {"text": "Hello world!", "voice": "af_bella", "lang": "en"}}
```

## Output

```json
{"audio_b64": "<base64 WAV>", "wall_time_s": 0.8}
```

## Available Voices

`af_bella`, `af_sarah`, `am_adam`, `am_michael`, `bf_emma`, `bf_isabella`, `bm_george`, `bm_lewis`, `af_nicole`

## Supported Languages

English (en), Spanish (es), French (fr), German (de), Italian (it), Japanese (ja), Korean (ko), Chinese (zh), Portuguese (pt)

## GPU Requirements

RTX 3090+ (24GB VRAM) | <1s per utterance | Apache 2.0 license

## Built by [E-Labs AI](https://www.elabsai.com)
