
<!-- [ID:26_AUTO_DISCOVERY_TAHAP_4_S001] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: TAHAP 4, SIAP -->
# ==========================================
print("⚙️ [TAHAP 4] Menyalakan Mesin ComfyUI...")
subprocess.Popen(["python", "main.py", "--port", "8188"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
time.sleep(45) 
print("🚀 [SIAP] Bot Agentic God Mode (Auto-Translate) AKTIF!")

<!-- [ID:26_AUTO_DISCOVERY_TAHAP_4_S002] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: TAHAP 4 -->
## Halaman 105

   # Catatan: Model ControlNet OpenPose & IP-Adapter besarnya bisa bergiga-giga, nanti bisa ditambahkan opsio
]
for file_path, url in models:
   if not os.path.exists(file_path):
       print(f"Mendownload {file_path.split('/')[-1]}...")
       os.system(f'wget -c -q --show-progress -O {file_path} {url}')
print("⚙️ [TAHAP 4] Menyalakan Mesin ComfyUI...")
subprocess.Popen(["python", "main.py", "--port", "8188"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
time.sleep(45)

<!-- [ID:26_AUTO_DISCOVERY_TAHAP_4_S003] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: TAHAP 4 -->
# Menyamarkan Pony_V6_XL.safetensors menjadi "model_utama.safetensors"
models = [
   ('models/checkpoints/model_utama.safetensors', 'https://huggingface.co/WhiteAiZ/PonyXL/resolve/main/PonyDi
   ('models/upscale_models/4x-UltraSharp-v2.pth', 'https://huggingface.co/lokcx/4x-Ultrasharp/resolve/main/4x
   ('models/insightface/inswapper_128.onnx', 'https://github.com/facefusion/facefusion-assets/releases/downlo
]
for file_path, url in models:
   if not os.path.exists(file_path):
       os.system(f'wget -c -q --show-progress -O {file_path} {url}')
print("⚙️ [TAHAP 4] Menyalakan Mesin di Port Rahasia...")
