
# Türkçe karakter sorunlarını çözmek için 
def normalize(text):
    return text.replace('İ', 'i').replace('I', 'i').replace('Ü', 'ü') \
               .replace('Ö', 'ö').replace('Ç', 'ç').replace('Ş', 'ş') \
               .replace('Ğ', 'ğ').lower()


def delete_neighborhood(data, il_adi, ilce_adi, mahalle_adi):

    # inputları küçük harfe çevirip Türkçe karakter sorununa çözüm
    il = normalize(il_adi)
    ilce = normalize(ilce_adi)
    mahalle = normalize(mahalle_adi)

    # eşleşen mahalleleri döngüyle bul
    eslesenler = [
        item for item in data
        if item['il'] == il and item['ilce'] == ilce and item['mahalle'] == mahalle
    ]

    if not eslesenler:
        print("❗ Girilen bilgilere uygun mahalle bulunamadı.")
        return

    # Eşleşen mahalleleri ram'den silmek için (çakışma olmaması için )
    data[:] = [
        item for item in data
        if not (
            item['il'] == il and
            item['ilce'] == ilce and
            item['mahalle'] == mahalle
        )
    ]

    print(f"\n✅ '{mahalle_adi.upper()}' mahallesi başarıyla silindi.")

    # Silinen verilerden sonra kalan mahalleleri gösterme döngüsü
    kalanlar = [
        item for item in data
        if item['il'] == il and item['ilce'] == ilce
    ]

    print(f"\n📍 {il_adi.upper()} / {ilce_adi.upper()} ilçesindeki güncel mahalleler:")

    if not kalanlar:
        print("➡️ Bu ilçede artık mahalle kalmadı.")
    else:
        for n in kalanlar:
            print(f"İl: {n['il'].capitalize()}, İlçe: {n['ilce'].capitalize()}, "
                  f"Mahalle: {n['mahalle'].capitalize()}, Belde: {n['belde']}")

    # değişiklikleri kalıcı olarak dosyaya kaydetmek için:
    try:
        with open("neighborhoods.txt", "w", encoding="utf-8") as file:
            for item in data:
                line = f"{item['mahalle'].upper()} {item['il'].upper()} -> {item['ilce'].upper()} -> {item['belde']}\n"  # dict yapısı
                file.write(line)
        print("\n💾 Değişiklikler dosyaya kaydedildi.")
    except Exception as e:
        print("❌ Dosya kaydedilirken hata oluştu:", e)


#main py'ye entegra olabilmesi için interface fonksiyonu:
def run_deleting(data):
    """
    Kullanıcıdan bilgi alır ve silme işlemini başlatır.
    """
    print("\n--- Mahalle Silme ---")
    il = input("İl adı: ").strip()
    ilce = input("İlçe adı: ").strip()
    mahalle = input("Silinecek mahalle adı: ").strip()

    delete_neighborhood(data, il, ilce, mahalle)
    print("Operasyon tamamlandı.")
