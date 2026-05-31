import subprocess
import shutil
import re
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tempfile
from datetime import datetime
import json

# =========================
# AYARLAR
# =========================
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/135.0.0.0 Safari/537.36"
)

class DownloadTask:
    def __init__(self, m3u8, vtt, referer, dosya_adi, audio_id, audio_label, altyazi_gom):
        self.m3u8 = m3u8
        self.vtt = vtt
        self.referer = referer
        self.dosya_adi = dosya_adi
        self.audio_id = audio_id
        self.audio_label = audio_label
        self.altyazi_gom = altyazi_gom
        
        self.status = "Bekliyor"
        self.progress = 0
        self.speed = "0 MB/s"
        self.eta = "Bilinmiyor"
        self.id = datetime.now().strftime("%H%M%S")
        self.ui_elements = None
        self.process = None
        self.cancelled = False


class DownloaderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("M3U8 Video Downloader & Subtitle Embedder")
        self.root.geometry("1080x1020")
        self.root.resizable(True, True)
        
        self.download_dir = Path.home() / "Desktop"
        self.tasks = []
        self.audio_map = {}
        
        self.check_dependencies()
        self.create_scrollable_ui()

    def check_dependencies(self):
        eksik = [p for p in ["ffmpeg", "ffprobe", "yt-dlp"] if not shutil.which(p)]
        if eksik:
            messagebox.showerror("Eksik Program", f"Eksik: {', '.join(eksik)}\nLütfen kurun.")
            raise SystemExit

    def create_scrollable_ui(self):
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        content = self.scrollable_frame

        tk.Label(content, text="M3U8 Video Downloader", font=("Arial", 18, "bold")).pack(pady=15)

        main_frame = ttk.Frame(content)
        main_frame.pack(fill="x", padx=20, pady=8)

        # M3U8
        ttk.Label(main_frame, text="M3U8 Linki:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=4)
        self.entry_m3u8 = ttk.Entry(main_frame, width=140)
        self.entry_m3u8.grid(row=1, column=0, sticky="ew", pady=4)

        # Ses Tarama
        ttk.Label(main_frame, text="Ses Seçimi:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=(12,4))
        audio_frame = ttk.Frame(main_frame)
        audio_frame.grid(row=3, column=0, sticky="ew", pady=4)
        self.combo_audio = ttk.Combobox(audio_frame, width=95, state="readonly")
        self.combo_audio.pack(side="left", padx=(0,8))
        ttk.Button(audio_frame, text="Sesleri Tara", command=self.scan_audio).pack(side="left")

        # VTT
        ttk.Label(main_frame, text="VTT Altyazı Linki:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=(12,4))
        self.entry_vtt = ttk.Entry(main_frame, width=140)
        self.entry_vtt.grid(row=5, column=0, sticky="ew", pady=4)

        # Referer
        ttk.Label(main_frame, text="Referer (opsiyonel):").grid(row=6, column=0, sticky="w", pady=(12,4))
        self.entry_referer = ttk.Entry(main_frame, width=140)
        self.entry_referer.grid(row=7, column=0, sticky="ew", pady=4)

        # Dosya Adı
        ttk.Label(main_frame, text="Dosya Adı:", font=("Arial", 10, "bold")).grid(row=8, column=0, sticky="w", pady=(12,4))
        self.entry_isim = ttk.Entry(main_frame, width=140)
        self.entry_isim.insert(0, "video")
        self.entry_isim.grid(row=9, column=0, sticky="ew", pady=4)

        # Altyazı Tipi
        ttk.Label(main_frame, text="Altyazı:", font=("Arial", 10, "bold")).grid(row=10, column=0, sticky="w", pady=(12,4))
        self.altyazi_var = tk.StringVar(value="göm")
        f = ttk.Frame(main_frame)
        f.grid(row=11, column=0, sticky="w", pady=4)
        ttk.Radiobutton(f, text="Videoya Göm (Önerilen)", variable=self.altyazi_var, value="göm").pack(side="left", padx=15)
        ttk.Radiobutton(f, text="Ayrı İndir", variable=self.altyazi_var, value="ayri").pack(side="left")

        self.btn_indir = ttk.Button(main_frame, text="İNDİR", command=self.start_download)
        self.btn_indir.grid(row=12, column=0, pady=25, ipadx=80, ipady=12)

        # Klasör
        folder_frame = ttk.Frame(content)
        folder_frame.pack(fill="x", padx=20, pady=10)
        ttk.Label(folder_frame, text="İndirme Klasörü:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.lbl_folder = ttk.Label(folder_frame, text=str(self.download_dir), foreground="blue")
        self.lbl_folder.pack(fill="x", pady=2)
        ttk.Button(folder_frame, text="Klasör Seç", command=self.select_folder).pack(anchor="w")

        # Aktif İndirmeler
        ttk.Separator(content, orient="horizontal").pack(fill="x", padx=20, pady=15)
        ttk.Label(content, text="Aktif İndirmeler", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=5)
        self.active_frame = ttk.Frame(content)
        self.active_frame.pack(fill="both", expand=True, padx=20, pady=5)

        main_frame.columnconfigure(0, weight=1)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def select_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_dir)
        if folder:
            self.download_dir = Path(folder)
            self.lbl_folder.config(text=str(self.download_dir))

    # ================= SES TARAMA =================
    def scan_audio(self):
        url = self.entry_m3u8.get().strip()
        if not url:
            messagebox.showwarning("Hata", "Önce M3U8 linkini girin!")
            return

        try:
            cmd = [
                "yt-dlp", "-J", "--no-download",
                "--user-agent", DEFAULT_USER_AGENT,
                "--impersonate", "chrome",
                "--extractor-args", "generic:impersonate",
                url
            ]

            if self.entry_referer.get().strip():
                cmd += ["--referer", self.entry_referer.get().strip()]

            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=30)

            if r.returncode != 0:
                messagebox.showerror("yt-dlp Hatası", r.stderr[-800:])
                return

            data = json.loads(r.stdout)

            self.audio_map.clear()
            items = []

            for f in data.get("formats", []):
                if f.get("vcodec") != "none" and f.get("vcodec") is not None:
                    continue
                fid = f.get("format_id")
                if not fid:
                    continue
                lang = f.get("language") or "und"
                note = f.get("format_note") or f.get("audio_channels") or ""
                label = f"{lang.upper()} | {note} | ID: {fid}"
                
                self.audio_map[label] = fid
                items.append(label)

            if not items:
                messagebox.showinfo("Bilgi", "Ses formatı bulunamadı.")
                return

            self.combo_audio["values"] = items
            self.combo_audio.set(items[0])
            messagebox.showinfo("Başarılı", f"{len(items)} adet ses formatı bulundu.")

        except Exception as e:
            messagebox.showerror("Hata", f"Ses tarama hatası:\n{str(e)}")

    def add_task_to_ui(self, task):
        frame = ttk.LabelFrame(self.active_frame, text=f"İndirme {task.id} - {task.dosya_adi}", padding=10)
        frame.pack(fill="x", pady=8)

        progress = ttk.Progressbar(frame, length=680, mode='determinate')
        progress.pack(fill="x", pady=6)

        info = ttk.Frame(frame)
        info.pack(fill="x", pady=6)
        speed_lbl = ttk.Label(info, text=f"Hız: {task.speed}", font=("Arial", 10))
        speed_lbl.pack(side="left", padx=15)
        eta_lbl = ttk.Label(info, text=f"ETA: {task.eta}", font=("Arial", 10))
        eta_lbl.pack(side="left", padx=15)

        status_lbl = ttk.Label(frame, text=task.status, foreground="blue")
        status_lbl.pack(anchor="w", pady=4)

        # Butonlar
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=8)

        btn_durdur = ttk.Button(btn_frame, text="⏸️ Durdur", command=lambda t=task: self.stop_task(t))
        btn_durdur.pack(side="left", padx=5)

        btn_iptal = ttk.Button(btn_frame, text="❌ İptal Et", command=lambda t=task: self.cancel_task(t))
        btn_iptal.pack(side="left", padx=5)

        task.ui_elements = {
            "progress": progress,
            "status": status_lbl,
            "speed": speed_lbl,
            "eta": eta_lbl,
            "frame": frame,
            "durdur_btn": btn_durdur,
            "iptal_btn": btn_iptal
        }

    def stop_task(self, task):
        if task.process and task.process.poll() is None:
            try:
                task.process.terminate()
                task.status = "⏸️ Durduruldu"
            except:
                pass
        self.update_task_ui(task)

    def cancel_task(self, task):
        if task.process and task.process.poll() is None:
            try:
                task.process.kill()
            except:
                pass
        task.cancelled = True
        task.status = "❌ İptal Edildi"
        if task.ui_elements and task.ui_elements.get("frame"):
            self.root.after(2500, lambda f=task.ui_elements["frame"]: f.destroy())
        self.update_task_ui(task)

    def clear_fields(self):
        self.entry_m3u8.delete(0, tk.END)
        self.entry_vtt.delete(0, tk.END)
        self.entry_isim.delete(0, tk.END)
        self.entry_isim.insert(0, "video")
        self.combo_audio.set("")

    def start_download(self):
        m3u8 = self.entry_m3u8.get().strip()
        vtt = self.entry_vtt.get().strip()

        if not m3u8 or not vtt:
            messagebox.showwarning("Eksik Bilgi", "M3U8 ve VTT linki zorunludur!")
            return

        audio_label = self.combo_audio.get()
        audio_id = self.audio_map.get(audio_label)
        if not audio_id:
            messagebox.showwarning("Ses Seçimi", "Lütfen 'Sesleri Tara' butonuna basıp ses seçin!")
            return

        dosya_adi = re.sub(r'[\\/*?:"<>|]', "", self.entry_isim.get().strip() or "video")

        task = DownloadTask(
            m3u8=m3u8, vtt=vtt, referer=self.entry_referer.get().strip(),
            dosya_adi=dosya_adi, audio_id=audio_id, audio_label=audio_label,
            altyazi_gom=self.altyazi_var.get() == "göm"
        )
        
        self.tasks.append(task)
        self.add_task_to_ui(task)
        self.clear_fields()
        
        threading.Thread(target=self.download_process, args=(task,), daemon=True).start()

    def download_process(self, task):
        try:
            task.status = "Video indiriliyor..."
            self.root.after(0, lambda: self.update_task_ui(task))

            self.download_dir.mkdir(exist_ok=True)
            video_temp = self.download_dir / f"{task.dosya_adi}_temp.mp4"
            final_file = self.download_dir / f"{task.dosya_adi}.mp4"

            ytdlp_cmd = [
                "yt-dlp",
                "--user-agent", DEFAULT_USER_AGENT,
                "--impersonate", "chrome",
                "--extractor-args", "generic:impersonate",
                "-f", f"bv*+ba[format_id={task.audio_id}]",
                "--merge-output-format", "mp4",
                "-o", str(video_temp),
                task.m3u8
            ]

            if task.referer:
                ytdlp_cmd.extend(["--referer", task.referer])

            task.process = subprocess.Popen(
                ytdlp_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            self.run_command(task)

            if task.cancelled:
                return

            if video_temp.exists():
                if final_file.exists():
                    final_file.unlink()
                video_temp.rename(final_file)

            # ================= ALTYAZI İŞLEMLERİ =================
            task.status = "Altyazı indiriliyor..."
            task.progress = 75
            self.root.after(0, lambda: self.update_task_ui(task))

            subtitle_lang = self.get_subtitle_language_from_url(task.vtt)
            vtt_file = (Path(tempfile.gettempdir()) if task.altyazi_gom else self.download_dir) / f"{task.dosya_adi}_{subtitle_lang}.vtt"

            curl_cmd = ["curl", "-L", "--fail", "--user-agent", DEFAULT_USER_AGENT, "-o", str(vtt_file)]
            if task.referer:
                curl_cmd.extend(["-H", f"Referer: {task.referer}"])
            curl_cmd.append(task.vtt)

            self.run_command_with_simple_process(curl_cmd)

            if task.altyazi_gom and vtt_file.exists():
                task.status = "Altyazı gömülüyor..."
                task.progress = 85
                self.root.after(0, lambda: self.update_task_ui(task))

                temp_final = self.download_dir / f"{task.dosya_adi}_gomulu.mp4"
                ffmpeg_cmd = [
                    "ffmpeg", "-y", "-i", str(final_file), "-i", str(vtt_file),
                    "-map", "0", "-map", "1", "-c", "copy", "-c:s", "mov_text",
                    "-metadata:s:s:0", f"language={subtitle_lang}",
                    str(temp_final)
                ]
                self.run_command_with_simple_process(ffmpeg_cmd)

                if temp_final.exists():
                    if final_file.exists():
                        final_file.unlink()
                    temp_final.rename(final_file)

            if not task.cancelled:
                task.status = "✅ Tamamlandı"
                task.progress = 100

        except Exception as e:
            if not task.cancelled:
                task.status = f"❌ Hata: {str(e)[:70]}"
        finally:
            self.root.after(0, lambda: self.update_task_ui(task))

    def run_command(self, task):
        try:
            for line in task.process.stdout:
                if line.strip():
                    self.parse_progress(line.strip(), task)
                self.root.after(0, lambda: self.update_task_ui(task))
            task.process.wait()
        except:
            pass

    def run_command_with_simple_process(self, cmd):
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        except:
            pass

    def update_task_ui(self, task):
        if not task.ui_elements:
            return
        task.ui_elements["progress"]["value"] = task.progress
        task.ui_elements["status"].config(text=task.status)
        task.ui_elements["speed"].config(text=f"Hız: {task.speed}")
        task.ui_elements["eta"].config(text=f"ETA: {task.eta}")

    def parse_progress(self, line, task):
        line = line.strip()
        perc = re.search(r'(\d+\.?\d*)%', line)
        if perc:
            task.progress = min(float(perc.group(1)), 100)
        speed = re.search(r'(\d+\.?\d*\s*[KMGT]i?B/s)', line)
        if speed:
            task.speed = speed.group(1)
        eta = re.search(r'ETA\s+([0-9:]+)', line)
        if eta:
            task.eta = eta.group(1)

    def get_subtitle_language_from_url(self, vtt_url):
        filename = Path(vtt_url.split("?")[0]).name.lower()
        matches = re.findall(r'(?<![a-z])([a-z]{2,3})(?![a-z])', filename)
        if matches:
            for code in reversed(matches):
                if code not in ("vtt", "webvtt", "sub", "txt"):
                    return code
        return "und"


if __name__ == "__main__":
    app = DownloaderGUI()
    app.root.mainloop()
