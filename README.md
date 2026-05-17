# M3U8 Video Downloader & Subtitle Embedder

Modern arayüzlü, hızlı ve çoklu indirme destekli gelişmiş bir M3U8 video indirici.  
Program sayesinde `.m3u8` yayınlarını kolayca indirebilir, `.vtt` altyazıları videoya gömebilir veya ayrı olarak kaydedebilirsiniz.

---

# Özellikler

- ✅ Modern ve kullanıcı dostu arayüz
- ✅ Tkinter tabanlı GUI sistemi
- ✅ M3U8 video indirme desteği
- ✅ VTT altyazı indirme desteği
- ✅ Altyazıyı videoya gömme
- ✅ Altyazıyı ayrı dosya olarak kaydetme
- ✅ Çoklu indirme desteği
- ✅ Aynı anda birden fazla video indirebilme
- ✅ Her indirme için ayrı progress bar
- ✅ Gerçek zamanlı indirme yüzdesi
- ✅ Gerçek zamanlı hız göstergesi
- ✅ ETA (kalan süre) gösterimi
- ✅ Referer desteği
- ✅ Otomatik altyazı dili algılama
- ✅ Dublaj dili seçebilme
- ✅ ffmpeg ile otomatik video birleştirme
- ✅ yt-dlp ile kaliteli video/ses seçimi
- ✅ Scroll destekli gelişmiş arayüz
- ✅ Özel indirme klasörü seçebilme
- ✅ Geçersiz dosya karakterlerini otomatik temizleme
- ✅ Thread sistemi sayesinde donmayan arayüz
- ✅ Arka planda işlem yürütme
- ✅ MP4 çıktı desteği
- ✅ Otomatik geçici dosya yönetimi
- ✅ Hata yakalama sistemi

---

# Programın Çalışması İçin Gerekenler

Programın düzgün çalışabilmesi için aşağıdaki yazılımların bilgisayarınızda kurulu olması gerekir.

---

# 1. Python Kurulumu

## Python 3.10 veya daha yeni sürüm gerekli

İndir:
https://www.python.org/downloads/

## Kurulum sırasında MUTLAKA şunları yapın:

Kurulum ekranında:

- ✅ `Add Python to PATH`

kutucuğunu işaretleyin.

Daha sonra:

- `Install Now`

diyerek kurulumu tamamlayın.

---

# Python Kurulumunu Kontrol Etme

CMD açın ve şunu yazın:

```bash
python --version
```

Örnek çıktı:

```bash
Python 3.12.2
```

---

# 2. FFmpeg Kurulumu

Programın:
- video birleştirme
- altyazı gömme
- medya işleme

işlemleri için FFmpeg gereklidir.

## İndir:

https://ffmpeg.org/download.html

Windows için genellikle:

https://www.gyan.dev/ffmpeg/builds/

önerilir.

---

# FFmpeg Kurulumu

İndirdiğiniz ZIP dosyasını çıkarın.

Örneğin:

```text
C:\ffmpeg
```

şeklinde yerleştirin.

Sonrasında:

```text
C:\ffmpeg\bin
```

klasörünü PATH'e ekleyin.

---

# PATH Ayarı Yapma

## Windows'ta:

1. Başlat Menüsü
2. "Ortam Değişkenleri" yaz
3. `Sistem ortam değişkenlerini düzenle`
4. `Environment Variables`
5. `Path`
6. `Edit`
7. `New`
8. Şunu ekle:

```text
C:\ffmpeg\bin
```

9. OK → OK → OK

---

# FFmpeg Kurulumunu Kontrol Etme

CMD açın:

```bash
ffmpeg -version
```

ve:

```bash
ffprobe -version
```

çalıştırın.

Hata almıyorsanız kurulum başarılıdır.

---

# 3. yt-dlp Kurulumu

M3U8 videolarını indirmek için gerekir.

Kurulum:

```bash
pip install yt-dlp
```

Kontrol:

```bash
yt-dlp --version
```

---

# 4. curl Kontrolü

Windows 10/11 sistemlerinde genellikle hazır gelir.

Kontrol etmek için:

```bash
curl --version
```

---

# Gerekli Programların Özeti

| Program | Gerekli |
|---|---|
| Python | ✅ |
| ffmpeg | ✅ |
| ffprobe | ✅ |
| yt-dlp | ✅ |
| curl | ✅ |

---

# Program Dosyasını Çalıştırma

Kod dosyasını örnek olarak:

```text
main.py
```

ismiyle kaydedin.

CMD açın.

Dosyanın bulunduğu klasöre gidin:

```bash
cd Masaüstü
```

ve çalıştırın:

```bash
python main.py
```

---

# Kullanım Rehberi

# 1. M3U8 Linkini Girin

Örnek:

```text
https://site.com/video/master.m3u8
```

---

# 2. Dublaj Dilini Seçin

Desteklenen diller:

- `en`
- `tr`

Program uygun ses kanalını otomatik seçmeye çalışır.

---

# 3. VTT Altyazı Linkini Girin

Örnek:

```text
https://site.com/subs/tr.vtt
```

---

# 4. Referer Girin (Opsiyonel)

Bazı siteler korumalıdır.

Bu durumda site adresini girmeniz gerekir.

Örnek:

```text
https://site.com
```

---

# 5. Dosya Adını Belirleyin

İndirilecek videonun adı.

Örnek:

```text
BreakingBad_S01E01
```

---

# 6. Altyazı Türünü Seçin

## Videoya Göm
- Önerilen yöntem
- MP4 içine gömülü altyazı oluşturur

## Ayrı İndir
- `.vtt` dosyası ayrı kaydedilir

---

# 7. İNDİR Butonuna Basın

Program otomatik olarak:

1. Videoyu indirir
2. Altyazıyı indirir
3. Videoyu birleştirir
4. Altyazıyı gömer
5. Final MP4 oluşturur

---

# Arayüz Özellikleri

# Aktif İndirmeler Paneli

Her indirme için:

- Ayrı kutu
- Ayrı progress bar
- Ayrı hız bilgisi
- Ayrı ETA bilgisi
- Ayrı durum mesajı

gösterilir.

---

# Çoklu İndirme Sistemi

Program aynı anda birden fazla indirme yapabilir.

Her indirme:
- Ayrı thread üzerinde çalışır
- Birbirinden bağımsızdır
- Arayüzü kilitlemez

---

# Referer Desteği

Korunan yayınlarda referer zorunlu olabilir.

Program:
- yt-dlp
- curl

komutlarına otomatik referer ekler.

Bu sayede:
- 403 Forbidden
- Access Denied

gibi hataların önüne geçilebilir.

---

# Altyazı Dili Algılama

Program `.vtt` dosya isminden altyazı dilini otomatik algılar.

Örnek:

```text
movie_tr.vtt → tr
movie_en.vtt → en
movie_de.vtt → de
```

---

# Kullanılan Teknolojiler

- Python
- Tkinter
- yt-dlp
- ffmpeg
- ffprobe
- curl
- threading
- subprocess
- pathlib
- tempfile

---

# Desteklenen Formatlar

# Giriş

- `.m3u8`
- `.vtt`

# Çıkış

- `.mp4`
- `.vtt`

---

# Olası Hatalar

# Eksik Program Hatası

Örnek:

```text
Eksik: ffmpeg, yt-dlp
```

## Çözüm

Eksik programları kurun ve PATH ayarını yapın.

---

# 403 Forbidden Hatası

Sebep:
- Referer eksik olabilir.

## Çözüm

Referer alanına site adresini girin.

Örnek:

```text
https://site.com
```

---

# ffmpeg Bulunamadı Hatası

Örnek:

```text
ffmpeg is not recognized
```

## Çözüm

FFmpeg PATH'e eklenmemiştir.

Şunu PATH'e ekleyin:

```text
C:\ffmpeg\bin
```

---

# yt-dlp Bulunamadı Hatası

Çözüm:

```bash
pip install yt-dlp
```

---

# Örnek Kullanım Akışı

```text
M3U8 Linki Gir →
VTT Linki Gir →
Referer Gir →
Dosya İsmi Belirle →
İNDİR →
Video İndir →
Altyazı İndir →
Birleştir →
Tamamlandı
```

---

# Performans Özellikleri

- Çok hızlı indirme
- Donmayan arayüz
- Düşük RAM kullanımı
- Paralel işlem desteği
- Arka planda işlem yürütme

---

# Güvenlik

Program:
- Kullanıcı verisi toplamaz
- Sunucu bağlantısı yapmaz
- Lokal çalışır
- Açık kaynak mantığında geliştirilmiştir

---

# Gelecekte Eklenebilecek Özellikler

- Dark Mode
- Cookie desteği
- Playlist desteği
- Toplu indirme sistemi
- İndirmeyi durdur/devam ettir
- Drag & Drop
- EXE dönüştürme
- MP3 dönüştürme
- Kalite seçme sistemi
- Video önizleme
- Log sistemi
- Hata kayıt sistemi
- Tema desteği

---

# Notlar

- Program yalnızca yasal kullanım amaçlıdır.
- DRM korumalı yayınlar indirilemeyebilir.
- Bazı yayınlarda token/cookie gerekebilir.
- Bazı siteler ek güvenlik sistemleri kullanabilir.

---

# Lisans

Bu proje eğitim ve kişisel kullanım amaçlı geliştirilmiştir.
