# AI Lead Finders video engine

Renders 1080x1920 branded videos (navy #000723, gold #FCBF49, orange #F77F00, Roboto) with
animated presenters (Maya, Daniel), drone flyovers, SMS threads, pipeline, inventory, checks,
and a persistent footer: aileadfinders.com · 908-332-9330.

Setup (cloud session):
- pip install kokoro-onnx soundfile numpy pillow --break-system-packages
- Kokoro model: https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx and voices-v1.0.bin -> /tmp/kokoro/
- Roboto: https://github.com/googlefonts/roboto-3-classic/releases/download/v3.010/Roboto_v3.010.zip -> unzip in /tmp/fonts/
- engine.py expects VOICE path for piper but engine2.py uses Kokoro (voices af_heart / am_michael).
- Copy engine.py, engine2.py, a videos file to /tmp/ailf/ and run: python3 videos_xxx.py <key> [...]
  Output: /tmp/ailf/out3/<key>.mp4

Script pattern (every video): hook -> message -> mid contact card -> second hook -> proof
(drone / inventory / checks / SMS / calendar) -> presenter line -> end card. Checks always show
masked amounts with "Illustration only · results vary". No guarantees or invented stats.
