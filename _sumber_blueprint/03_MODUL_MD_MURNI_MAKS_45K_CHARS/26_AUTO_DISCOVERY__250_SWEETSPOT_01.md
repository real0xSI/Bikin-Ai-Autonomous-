
<!-- [ID:26_AUTO_DISCOVERY__250_S001] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: :250 -->
## Halaman 384

                   return {
                       "safe": proc.returncode == 0,
                       "exit_code": proc.returncode,
                       "format": "SCANNED_BY_PROTECTAI_MODELSCAN",
                       "detail": (proc.stdout or proc.stderr or "")[:250].strip(),
                   }
               except Exception as e:
                   return {
                       "safe": False,
                       "exit_code": 2,
                       "format": "MODELSCAN_ERROR",
                       "detail": f"ModelScan error: {e}",
                   }
       if low.endswith(cls.RISKY_PICKLE_EXTENSIONS):
           return {
               "safe": False,
               "exit_code": 1,
               "format": "UNSAFE_PICKLE_BLOCKED",
               "detail": "Berkas Pickle/PyTorch mentah (.pt/.bin/.pkl) ditolak untuk mencegah Model Serializa
           }
       return {
           "safe": True,
           "exit_code": 0,
           "format": "REMOTE_API_OR_HF_SAFE",
           "detail": "Repositori model diizinkan (Wajib tarik varian Safetensors/GGUF).",
       }
