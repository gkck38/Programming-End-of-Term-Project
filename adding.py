def adding_new_neighborhood(data):
    """Yeni bir mahalleyi uygun il ve ilçeye ekler."""
    file_path = "neighborhoods.txt"  # Dosya yolu tanımı için

    if data is None:
        print("Veri yüklenemedi. Mahalle eklenemiyor.")
        return

    while True:
        il_adi = input("Hangi ile eklemek istiyorsunuz?: ").strip().lower()
        if any(item["il"] == il_adi for item in data):
            break
        print("❌ Böyle bir il bulunamadı. Lütfen tekrar girin.")

    while True:
        ilce_giris = input(f"{il_adi.title()} ilinin hangi ilçesine?: ").strip().lower()
        ilce_var, ilce_adi = False, ""
        for item in data:
            if item["il"] == il_adi and (ilce_giris == item["ilce"] or ilce_giris == item.get("belde", "")):
                ilce_var = True
                ilce_adi = item["ilce"]
                break
        if ilce_var:
            break
        print("❌ Böyle bir ilçe bulunamadı. Lütfen tekrar girin.")

    while True:
        yeni_mahalle_adi = input("Yeni mahalle adı: ").strip().lower()
        if any(
            item["il"] == il_adi and
            (item["ilce"] == ilce_adi or item.get("belde") == ilce_adi) and
            item["mahalle"] == yeni_mahalle_adi
            for item in data
        ):
            print("⚠️ Bu mahalle zaten var. Lütfen başka bir isim girin.")
        else:
            break

    # Belde/ilçe formatı alınması için
    formatted_ilce = f"{ilce_adi.title()}-DISTRICT CENTER"
    for item in data:
        if item["il"] == il_adi and item["ilce"] == ilce_adi:
            formatted_ilce = item.get("raw_ilce", formatted_ilce).title()
            break

    yeni_satir = f"{yeni_mahalle_adi.title()} {il_adi.title()} -> {formatted_ilce}"

    #Dosya sonu newline kontrolü
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            ends_with_newline = file.read().endswith("\n")
    except FileNotFoundError:
        ends_with_newline = True

    #Dosyaya yaz
    try:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(("\n" if not ends_with_newline else "") + yeni_satir)
        print("\n✅ Yeni mahalle başarıyla eklendi.")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        return

    #RAM içindeki veriye yeni mahalleyi ekle (isteğe bağlı)
    data.append({
        "il": il_adi,
        "ilce": ilce_adi,
        "belde": ilce_adi,  # Belde = ilçe kabul ediliyor
        "mahalle": yeni_mahalle_adi
    })

    # Güncel listeyi göster
    print(f"\n📍 {il_adi.title()} - {ilce_adi.title()} içindeki güncel mahalleler:")
    for item in data:
        if item["il"] == il_adi and (item["ilce"] == ilce_adi or item.get("belde") == ilce_adi):
            print("•", item["mahalle"].title())
