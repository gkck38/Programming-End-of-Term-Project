def update_neighborhood(data):
    """Var olan bir mahalleyi yeni adla değiştirir."""

    # 🔤 Türkçe karakterleri normalize eden yardımcı fonksiyon
    def normalize(text):
        return text.replace('İ', 'i').replace('I', 'i') \
                   .replace('Ü', 'ü').replace('Ö', 'ö') \
                   .replace('Ç', 'ç').replace('Ş', 'ş') \
                   .replace('Ğ', 'ğ').lower().strip()

    # Kullanıcıdan veriler alınır ve normalize edilir
    il_adi = normalize(input("Güncellemek istediğiniz il: ").strip())
    ilce_adi = normalize(input(f"{il_adi.title()} ilinin ilçesi: ").strip())
    eski_mahalle = normalize(input("Güncellenecek mahalle: ").strip())
    yeni_mahalle = normalize(input("Yeni mahalle adı: ").strip())

    bulundu = False
    for item in data:
        if (normalize(item["il"]) == il_adi and
            normalize(item["ilce"]) == ilce_adi and
            normalize(item["mahalle"]) == eski_mahalle):
            item["mahalle"] = yeni_mahalle
            bulundu = True
            break

    if not bulundu:
        print("❗ Girilen mahalle bulunamadı.")
        return

    # Değişiklikleri kalıcı olarak dosyaya yaz
    try:
        with open("neighborhoods.txt", "w", encoding="utf-8") as f:
            for item in data:
                f.write(
                    f"{item['mahalle'].upper()} {item['il'].upper()} -> {item['ilce'].upper()} -> {item['belde']}\n"
                )
        print(f"\n✅ {eski_mahalle.title()} mahallesi {yeni_mahalle.title()} olarak güncellendi.")
    except Exception as e:
        print(f"❌ Dosya yazılırken hata oluştu: {e}")
