"""
RunPod serverless handler for Kokoro 82M TTS — text → audio generation.

Architecture:
  - Kokoro 82M (~82M params) based on E2-TTS
  - Supports multiple voices and languages
  - Runs on any GPU with >=2GB VRAM
  - ~0.2s for short sentences on RTX 4090

Environment:
  - RUNPOD_POD_ID       — auto
  - RUNPOD_AI_API_KEY   — auto

Input schema (via RunPod serverless job):
  {
    "input": {
      "text": "Hello world!",                   // REQUIRED — text to synthesize
      "voice": "af_bella",                       // optional — voice ID
      "speed": 1.0                               // optional — speed multiplier (0.5-2.0)
    }
  }

Output:
  {
    "audio_base64": "<base64-encoded WAV>",
    "text": "Hello world!",
    "voice": "af_bella",
    "wall_time_s": 0.2
  }
"""

import base64
import os
import time
import traceback
from io import BytesIO

# ── Environment setup ─────────────────────────────────────────────────────────
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

import torch

# Disable flash/mem-efficient SDPA for broad GPU compatibility
torch.backends.cuda.enable_flash_sdp(False)
torch.backends.cuda.enable_mem_efficient_sdp(False)
torch.backends.cuda.enable_math_sdp(True)

# ── Model path (baked into image at BUILD TIME) ──────────────────────────────
MODEL_ID = "/models/kokoro"

# ── Global pipeline (loaded once, reused across jobs) ─────────────────────────
_pipe = None
_device = None


def load_pipeline():
    """Load Kokoro 82M model once and cache globally."""
    global _pipe, _device
    if _pipe is not None:
        return _pipe, _device

    print("[Cold Start] Loading Kokoro 82M model...", flush=True)
    t0 = time.time()

    _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    print(f"  Device: {_device}, dtype: {dtype}", flush=True)

    # Import Kokoro TTS
    from kokoro import KPipeline

    # Load pipeline from local model path
    pipe = KPipeline(
        model_path=f"{MODEL_ID}/kokoro-v1.0.pth",
        voice_dir=f"{MODEL_ID}/voices",
        device=str(_device),
        dtype=dtype,
    )

    print(f"[Cold Start] Pipeline ready in {time.time() - t0:.1f}s", flush=True)

    _pipe = pipe
    return _pipe, _device


def audio_to_wav_b64(audio_array, sample_rate: int = 24000) -> str:
    """Convert numpy audio array to base64 WAV string."""
    import numpy as np
    from scipy.io import wavfile

    buf = BytesIO()
    # Ensure int16 range
    audio_int16 = np.clip(audio_array * 32767, -32768, 32767).astype(np.int16)
    wavfile.write(buf, sample_rate, audio_int16)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def run_inference(
    text: str,
    voice: str = "af_bella",
    speed: float = 1.0,
) -> tuple:
    """
    Run Kokoro 82M inference.
    Returns (audio_base64, actual_voice, wall_time_s).
    """
    pipe, device = load_pipeline()

    print(f"[Inference] Synthesizing: text='{text[:80]}'", flush=True)
    print(f"  voice={voice}, speed={speed}", flush=True)

    t_start = time.time()

    # Run inference
    with torch.inference_mode():
        gen = pipe(text, voice=voice, speed=speed)
        audio_frames = []
        for i, (gs, ps, audio) in enumerate(gen):
            audio_frames.append(audio)
        if audio_frames:
            import numpy as np
            audio_out = np.concatenate(audio_frames)
        else:
            audio_out = None

    wall_time = time.time() - t_start
    print(f"[Done] Synthesis took {wall_time:.2f}s", flush=True)

    # Convert to base64 WAV
    audio_b64 = audio_to_wav_b64(audio_out) if audio_out is not None else ""

    return audio_b64, voice, wall_time


# ═══════════════════════════════════════════════════════════════════════════════
# RunPod Serverless Handler
# ═══════════════════════════════════════════════════════════════════════════════


def handler(job):
    """
    RunPod serverless handler: text → base64 WAV audio.

    Called once per job. The pipeline stays loaded across jobs (global).
    """
    job_input = job.get("input", {})
    text = job_input.get("text", "")

    if not text:
        return {"error": "Missing required field: text"}

    voice = str(job_input.get("voice", "af_bella"))
    speed = float(job_input.get("speed", 1.0))

    # Validate speed range
    speed = max(0.5, min(2.0, speed))

    try:
        # Run inference
        audio_b64, actual_voice, wall_time = run_inference(
            text=text,
            voice=voice,
            speed=speed,
        )

        return {
            "audio_base64": audio_b64,
            "text": text,
            "voice": actual_voice,
            "wall_time_s": round(wall_time, 2),
        }

    except Exception as exc:
        traceback.print_exc()
        return {
            "error": f"Kokoro inference failed: {str(exc)}",
            "traceback": traceback.format_exc(),
        }


# ── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import runpod

    runpod.serverless.start({"handler": handler})
