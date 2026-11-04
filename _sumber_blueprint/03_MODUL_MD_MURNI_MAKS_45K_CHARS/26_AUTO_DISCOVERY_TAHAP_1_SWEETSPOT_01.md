
<!-- [ID:26_AUTO_DISCOVERY_TAHAP_1_S001] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: TAHAP 1 -->
# ==========================================
print("⚙️ [TAHAP 1] Menyiapkan Lingkungan & Mengunduh ComfyUI...")
os.chdir('/content')
if not os.path.exists('ComfyUI'):
   os.system('git clone https://github.com/comfyanonymous/ComfyUI -q')



<!-- [ID:26_AUTO_DISCOVERY_TAHAP_1_S002] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: TAHAP 1, TAHAP 2 -->
# ==========================================
print("⚙️ [TAHAP 1] Menyiapkan Lingkungan Agentic...")
os.chdir('/content')
if not os.path.exists('ComfyUI'):
   os.system('git clone https://github.com/comfyanonymous/ComfyUI -q')
os.chdir('/content/ComfyUI')
os.system('pip install -r requirements.txt -q')
folder_list = ['checkpoints', 'upscale_models', 'ipadapter', 'insightface', 'inpaint', 'input']
for folder in folder_list:
   os.makedirs(f'models/{folder}', exist_ok=True)
print("⚙️ [TAHAP 2] Memasang Alat Dewa (ReActor, ControlNet, dll)...")
nodes = [
   "https://github.com/Gourieff/comfyui-reactor-node",
   "https://github.com/Fannovel16/comfyui_controlnet_aux",
   "https://github.com/cubiq/ComfyUI_IPAdapter_plus",
   "https://github.com/ltdrdata/ComfyUI-Impact-Pack",



<!-- [ID:26_AUTO_DISCOVERY_TAHAP_1_S003] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: TAHAP 1, TAHAP 2, TAHAP 3 -->
# ==========================================
print("⚙️ [TAHAP 1] Menyiapkan Lingkungan Uncensored...")
os.chdir('/content')
if not os.path.exists('ComfyUI'):
   os.system('git clone https://github.com/comfyanonymous/ComfyUI -q')
os.chdir('/content/ComfyUI')
os.system('pip install -r requirements.txt -q')
folder_list = ['checkpoints', 'input', 'upscale_models', 'insightface', 'ipadapter', 'controlnet']
for folder in folder_list:
   os.makedirs(f'models/{folder}', exist_ok=True)
print("⚙️ [TAHAP 2] Memasang Alat Dewa (ReActor, ControlNet, IP-Adapter)...")
nodes = [
   "https://github.com/Gourieff/comfyui-reactor-node",
   "https://github.com/Fannovel16/comfyui_controlnet_aux",
   "https://github.com/cubiq/ComfyUI_IPAdapter_plus",
]
for repo_url in nodes:
   node_name = repo_url.split('/')[-1].replace('.git', '')
   folder_path = f"custom_nodes/{node_name}"
   if not os.path.exists(folder_path):
       subprocess.run(f"git clone {repo_url} {folder_path} -q", shell=True)
       req_file = f"{folder_path}/requirements.txt"
       if os.path.exists(req_file):
           os.system(f"pip install -r {req_file} -q")
print("⚙️ [TAHAP 3] Mendownload Model Pony & Ekstraksinya...")
models = [
   ('models/checkpoints/Pony_V6_XL.safetensors', 'https://huggingface.co/WhiteAiZ/PonyXL/resolve/main/PonyDif
   ('models/upscale_models/4x-UltraSharp-v2.pth', 'https://huggingface.co/lokcx/4x-Ultrasharp/resolve/main/4x
   ('models/insightface/inswapper_128.onnx', 'https://github.com/facefusion/facefusion-assets/releases/downlo



<!-- [ID:26_AUTO_DISCOVERY_TAHAP_1_S004] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: TAHAP 1 -->
# ==========================================
print("⚙️ [TAHAP 1] Menyiapkan Sistem Siluman...")
os.chdir('/content')

<!-- [ID:26_AUTO_DISCOVERY_TAHAP_1_S005] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: TAHAP 1 -->
# ==========================================
import os
import time
import subprocess
import requests
from deep_translator import GoogleTranslator
TOKEN_UTAMA = "8885292945:AAGK66Dng-81kTW9-vv0Yoy4Pzi43nU3ns0"
URL_API_ANTREAN = "https://bikinaibot.pythonanywhere.com/get_task"
print("⚙️ [TAHAP 1] Memeriksa & Membersihkan Lingkungan Kerja...")
os.chdir('/content')


