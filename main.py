import subprocess
import os
import shutil
import re
from pathlib import Path

# =========================
# AYARLAR
# =========================

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/147.0.0.0 Safari/537.36"
)

DOWNLOAD_DIR = "downloads"


# =========================
# YARDIMCI FONKSİYONLAR
# =========================

def temiz_dosya_adi(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)


def check_dependencies():
    eksik = []

    if not shutil.which("ffmpeg"):
        eksik.append("ffmpeg")

    if not shutil.which("yt-dlp"):
        eksik.append("yt-dlp")

    if eksik:
        print("\nEksik programlar bulundu:")
        for item in eksik:
            print(f"- {item}")

        print("\nKurulum Linkleri:")
        print("FFmpeg  : https://ffmpeg.org/download.html")
        print("yt-dlp  : https://github.com/yt-dlp/yt-dlp")

        exit()


def run_command(command_list, step_name):
    try:
        subprocess.run(command_list, check=True)
        return True

    except subprocess.CalledProcessError:
        print(f"\nHATA: {step_name} başarısız oldu.")
        return False

    except Exception as e:
        print(f"\nBeklenmeyen hata: {e}")
        return False


# =========================
# ANA PROGRAM
# =========================

def main():

    os.system("cls" if os.name == "nt" else "clear")

    print("=" * 50)
    print(" M3U8 Video Downloader & Subtitle Embedder ")
    print("=" * 50)

    check_dependencies()

    # Kullanıcı girdileri
    video_link = input("\nM3U8 linki: ").strip()

    video_isim = input("Dosya adı: ").strip()
    video_isim = temiz_dosya_adi(video_isim)

    altyazi_link = input("VTT altyazı linki: ").strip()

    subtitle_lang = input("Altyazı dili (tur/eng) [tur]: ").strip()
    if subtitle_lang == "":
        subtitle_lang = "tur"

    referer = input("Referer (boş bırakılabilir): ").strip()

    # Klasör oluştur
    Path(DOWNLOAD_DIR).mkdir(exist_ok=True)

    # Dosya yolları
    video_temp = os.path.join(DOWNLOAD_DIR, f"{video_isim}_temp.mp4")
    vtt_file = os.path.join(DOWNLOAD_DIR, f"{video_isim}.vtt")
    final_file = os.path.join(DOWNLOAD_DIR, f"{video_isim}.mp4")

    # =========================
    # 1. VİDEO İNDİR
    # =========================

    print("\n[1/3] Video indiriliyor...\n")

    ytdlp_cmd = [
        "yt-dlp",
        "--user-agent",
        DEFAULT_USER_AGENT,
    ]

    if referer:
        ytdlp_cmd.extend(["--referer", referer])

    ytdlp_cmd.extend([
        "--format",
        "bestvideo+bestaudio/best",
        "--merge-output-format",
        "mp4",
        "-o",
        video_temp,
        video_link
    ])

    if not run_command(ytdlp_cmd, "Video indirme"):
        return

    # =========================
    # 2. ALTYAZI İNDİR
    # =========================

    print("\n[2/3] Altyazı indiriliyor...\n")

    curl_cmd = [
        "curl",
        "-L",
        "--user-agent",
        DEFAULT_USER_AGENT
    ]

    if referer:
        curl_cmd.extend([
            "-H",
            f"Referer: {referer}"
        ])

    curl_cmd.extend([
        altyazi_link,
        "-o",
        vtt_file
    ])

    if not run_command(curl_cmd, "Altyazı indirme"):
        return

    # Dosya kontrolü
    if not os.path.exists(video_temp):
        print("\nVideo dosyası bulunamadı.")
        return

    if not os.path.exists(vtt_file):
        print("\nAltyazı dosyası bulunamadı.")
        return

    # =========================
    # 3. ALTYAZI GÖMME
    # =========================

    print("\n[3/3] Altyazı videoya gömülüyor...\n")

    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        video_temp,
        "-i",
        vtt_file,
        "-c",
        "copy",
        "-c:s",
        "mov_text",
        f"-metadata:s:s:0",
        f"language={subtitle_lang}",
        final_file,
        "-y"
    ]

    if not run_command(ffmpeg_cmd, "FFmpeg işlemi"):
        return

    # =========================
    # TEMİZLİK
    # =========================

    try:
        if os.path.exists(video_temp):
            os.remove(video_temp)

        if os.path.exists(vtt_file):
            os.remove(vtt_file)

    except:
        pass

    # =========================
    # BAŞARILI
    # =========================

    print("\n" + "=" * 50)
    print(" İŞLEM TAMAMLANDI ")
    print("=" * 50)

    print(f"\nDosya hazır:\n{final_file}\n")


if __name__ == "__main__":
    main()