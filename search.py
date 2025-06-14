# Gerekli kütüphaneleri yüklüyoruz
import re  # Metin parçalama ve düzenli ifadeler için
from collections import Counter  # Sayım işlemleri için
import matplotlib.pyplot as plt  # Grafik çizimi için
from file_loader import load_neighborhood_data  # Mahalle verilerini yüklemek için özel fonksiyon

# ------------------------- TAM MAHALLE ADI ARAMA -------------------------
def normalize(text):
    return text.replace('İ', 'i').replace('I', 'i').replace('Ü', 'ü') \
               .replace('Ö', 'ö').replace('Ç', 'ç').replace('Ş', 'ş') \
               .replace('Ğ', 'ğ').lower()



def search_exact(data):
    """Kullanıcının girdiği mahalle adını tam olarak arar."""
    #data = load_neighborhood_data("neighborhoods.txt")  # Mahalle verisini dosyadan yüklüyoruz
    if not data:
        print("Veri yüklenemedi.")
        return

    while True:
        mahalle_adi = input("Tam olarak mahalle adını girin: ")
        mahalle_adi=normalize(mahalle_adi)   # Girişten boşlukları kaldır, küçük harfe çevir
        found = False  # Bulunup bulunmadığını kontrol etmek için bayrak
        for item in data:
            if item['mahalle'] == mahalle_adi:  # Mahalle tam eşleşirse
                print(f"{item['il'].title()} -> {item['ilce'].title()} -> {item['mahalle'].title()}")  # Formatlı çıktı ver
                found = True  # Eşleşme bulundu
        if found:
            break  # Döngüden çık
        else:
            print("❌ Tam eşleşme bulunamadı. Lütfen tekrar deneyin.\n")

# ------------------------- KISMİ MAHALLE ARAMA -------------------------
def search_partial(data):
    """Mahalle adı içinde geçen kısımlara göre arama yapar."""
    #data = load_neighborhood_data("neighborhoods.txt")  # Veriyi yüklüyoruz
    if not data:
        print("Veri yüklenemedi.")
        return

    while True:
        mahalle_adi = input("Aramak istediğiniz mahalle adını (kısmî olarak) girin: ")
        mahalle_adi = normalize(mahalle_adi)  # Girişten boşlukları kaldır, küçük harfe çevir
        found = False
        for item in data:
            if mahalle_adi in item['mahalle']:  # Mahalle içinde kısmi eşleşme aranıyor
                print(f"{item['il'].title()} -> {item['ilce'].title()} -> {item['mahalle'].title()}")
                found = True
        if found:
            break
        else:
            print("❌ Kısmi eşleşme bulunamadı. Lütfen tekrar deneyin.\n")

# ------------------------- MAHALLE EKLEME -------------------------
def adding_new_neighborhood(data):
    """Yeni bir mahalleyi uygun il ve ilçeye ekler."""
    file_path = "neighborhoods.txt"  # Dosya yolu tanımı
    #data = load_neighborhood_data(file_path)  # Veriyi içe aktar
    if data is None:
        print("Veri yüklenemedi. Mahalle eklenemiyor.")
        return

    while True:
        il_adi = input("Hangi ile eklemek istiyorsunuz?: ").strip().lower()  # Kullanıcıdan il al
        if any(item["il"] == il_adi for item in data):  # İl var mı kontrolü
            break
        print("Böyle bir il bulunamadı. Lütfen tekrar girin.")

    while True:
        ilce_giris = input(f"{il_adi.title()} ilinin hangi ilçesine?: ").strip().lower()  # İlçeyi al
        ilce_var, ilce_adi = False, ""
        for item in data:
            if item["il"] == il_adi and (ilce_giris == item["ilce"] or ilce_giris == item.get("belde", "")):
                ilce_var = True
                ilce_adi = item["ilce"]  # Eşleşen ilçe adı kaydediliyor
                break
        if ilce_var:
            break
        print("Böyle bir ilçe bulunamadı. Lütfen tekrar girin.")

    while True:
        yeni_mahalle_adi = input("Yeni mahalle adı: ").strip().lower()  # Yeni mahalle ismini al
        if any(item["il"] == il_adi and (item["ilce"] == ilce_adi or item.get("belde") == ilce_adi) and item["mahalle"] == yeni_mahalle_adi for item in data):
            print("Bu mahalle zaten var. Başka girin.")  # Aynı mahalle varsa uyar
        else:
            break

    formatted_ilce = f"{ilce_adi.title()}-DISTRICT CENTER"  # Varsayılan formatlı ilçe adı
    for item in data:
        if item["il"] == il_adi and item["ilce"] == ilce_adi:
            formatted_ilce = item.get("raw_ilce", formatted_ilce).title()  # Gerçek format varsa onu al
            break

    yeni_satir = f"{yeni_mahalle_adi.title()} {il_adi.title()} -> {formatted_ilce}"  # Eklenecek satır formatı
    try:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write("\n" + yeni_satir if not file.read().endswith("\n") else yeni_satir)  # Satır sonu kontrolü
        print("\nYeni mahalle eklendi.")

        data = load_neighborhood_data(file_path)  # Güncel veriyi yeniden yükle
        print(f"\n{il_adi.title()} - {ilce_adi.title()} içindeki mahalleler:")
        for item in data:
            if item["il"] == il_adi and (item["ilce"] == ilce_adi or item.get("belde") == ilce_adi):
                print("-", item["mahalle"].title())
    except Exception as e:
        print(f"Hata oluştu: {e}")

# ------------------------- MAHALLE GÜNCELLEME -------------------------
def update_neighborhood():
    """Var olan bir mahalleyi yeni adla değiştirir."""
    try:
        with open("neighborhoods.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()  # Tüm satırları oku
    except FileNotFoundError:
        print("neighborhoods.txt bulunamadı.")
        return

    data = []
    for line in lines:
        try:
            parts = line.strip().split(" -> ")
            mahalle_il = parts[0].split()
            mahalle = " ".join(mahalle_il[:-1])
            il = mahalle_il[-1]
            ilce = parts[1].replace("-DISTRICT CENTER", "").strip()
            data.append({"mahalle": mahalle, "il": il, "ilce": ilce})  # Eski formatı parse ediyoruz
        except:
            continue

    # Kullanıcıdan girişler alınır
    il_adi = input("Güncellemek istediğiniz il: ").strip()
    ilce_adi = input(f"{il_adi.title()} ilinin ilçesi: ").strip()
    eski_mahalle = input("Güncellenecek mahalle: ").strip()
    yeni_mahalle = input("Yeni mahalle adı: ").strip()

    bulundu = False
    for item in data:
        if item["il"].lower() == il_adi.lower() and item["ilce"].lower() == ilce_adi.lower() and item["mahalle"].lower() == eski_mahalle.lower():
            item["mahalle"] = yeni_mahalle  # Güncelleme yapılır
            bulundu = True
            break

    if not bulundu:
        print("Girilen mahalle bulunamadı.")
        return

    with open("neighborhoods.txt", "w", encoding="utf-8") as f:
        for item in data:
            f.write(f"{item['mahalle'].title()} {item['il'].title()} -> {item['ilce'].title()}-DISTRICT CENTER\n")  # Güncellenmiş hali kaydet

    print(f"{eski_mahalle.title()} mahallesi {yeni_mahalle.title()} olarak güncellendi.")



