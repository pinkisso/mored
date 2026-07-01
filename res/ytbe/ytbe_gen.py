import os
import subprocess

# Güncel ve doğrulanmış YouTube IPTV kanal listesi
kanallar = [
    ("cnnturk", "CNN Türk", "https://www.youtube.com/@cnnturk/live"),
    ("sozcutelevizyonu", "Sözcü TV", "https://www.youtube.com/@sozcutelevizyonu/live"),
    ("krttv", "KRT TV", "https://www.youtube.com/@krtcanli/live"),
    ("ulusalkanal", "Ulusal Kanal", "https://www.youtube.com/@ulusalkanalTV/live"),
    ("ekoturk", "Eko Türk", "https://www.youtube.com/@ekoturktv/live"),
    ("beinsportshaber", "Bein Spor Haber", "https://www.youtube.com/@beINSPORTST%C3%BCrkiye/live"),
]

# Çıktı klasörünü ayarla
streams_dir = "res/ytbe"
os.makedirs(streams_dir, exist_ok=True)

ana_m3u = "#EXTM3U\n"
print("📡 Kanal linkleri yerel temiz IP kullanılarak toplanıyor...\n")

for slug, isim, url in kanallar:
    try:
        # Cron altında çalışırken hata vermemesi için full path (/usr/local/bin/yt-dlp) kullanıyoruz
        result = subprocess.run(
            ["/usr/local/bin/yt-dlp", "-f", "best", "-g", url],
            capture_output=True, text=True, timeout=20
        )
        link = result.stdout.strip()
        
        if link and link.startswith("http"):
            # 1. Her kanal için tekil m3u8 dosyası üretimi
            kanal_m3u_icerik = f"#EXTM3U\n#EXT-X-STREAM-INF:BANDWIDTH=7680000\n{link}\n"
            with open(f"{streams_dir}/{slug}.m3u8", "w", encoding="utf-8") as f:
                f.write(kanal_m3u_icerik)
                
            # 2. Ana playlist.m3u dosyasına ekleme
            #ana_m3u += f'#EXTINF:-1,{isim}\n{link}\n'
            #print(f"✅ {isim} linki alındı ve dosyası üretildi.")
        else:
            print(f"❌ {isim} - Yayın linki çözülemedi.")
    except Exception as e:
        print(f"❌ {isim} - Hata oluştu: {e}")

# Toplu m3u listesini kaydet
#with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(ana_m3u)

print("\n💾 Dosyalar yerelde hazırlandı. GitHub'a pushlanıyor...")

# Git Otomasyonu
try:
    subprocess.run(["git", "config", "user.name", "Lokal Sunucu Proxy"], check=True)
    subprocess.run(["git", "config", "user.email", "sunucu@proxy.local"], check=True)
    
    # Yeni eklenen ve silinen dosyaların tamamını kapsama al
    subprocess.run(["git", "add", "-A"], check=True)
    
    # Değişiklik varsa commit fırlat
    subprocess.run("git diff-index --quiet HEAD || git commit -m 'Lokal Otomatik Güncelleme'", shell=True, check=True)
    
    # Aktif kullanılan branch adını tespit et ve ona pushla
    branch_check = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
    aktif_dal = branch_check.stdout.strip() or "main"
    
    subprocess.run(["git", "push", "origin", aktif_dal], check=True)
    print(f"\n🚀 Muazzam! GitHub yüklemesi '{aktif_dal}' dalına başarıyla tamamlandı!")
except Exception as e:
    print(f"\n❌ GitHub'a yüklenirken bir sorun çıktı: {e}")
