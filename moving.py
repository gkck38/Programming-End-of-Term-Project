def run_moving(data):
    print("\n--- Mahalle Taşıma ---")
    
    # inputları alma yeri 
    old_il = input("Mevcut il adı: ").strip()
    old_ilce = input("Mevcut ilçe adı: ").strip()
    mahalle = input("Taşınacak mahalle adı: ").strip()
    new_il = input("Yeni il adı: ").strip()
    new_ilce = input("Yeni ilçe adı: ").strip()
    new_belde = input("Yeni belde/merkez adı (boş bırakırsan ilçe adı merkez olarak kabul edilir): ").strip() # eski belde beraberinde gelmesin diye 

    # Türkçe karakter düzeltme sıkıntı olmaması için
    def normalize(text):
        return text.replace('İ', 'i').replace('I', 'i').replace('Ü', 'ü') \
                   .replace('Ö', 'ö').replace('Ç', 'ç').replace('Ş', 'ş') \
                   .replace('Ğ', 'ğ').lower()
    #fonksiyonu aldığımız inputlara uyguluyoz :
    old_il = normalize(old_il)
    old_ilce = normalize(old_ilce)
    mahalle = normalize(mahalle)
    new_il = normalize(new_il)
    new_ilce = normalize(new_ilce)

    # Eğer kullanıcı belde girmezse otomatik belirle
    if not new_belde:
        belde_adaylari = list({
            item["belde"] for item in data
            if item["il"] == new_il and item["ilce"] == new_ilce
        })

        if len(belde_adaylari) == 1:
            new_belde = belde_adaylari[0]
            print(f"📌 Belde otomatik belirlendi: {new_belde}")
        elif len(belde_adaylari) > 1:
            print("\n📌 Yeni ilçede birden fazla belde bulundu:")
            for i, b in enumerate(belde_adaylari, 1):
                print(f"{i}. {b}")
            try:
                secim = int(input("Taşımak istediğiniz belde numarasını girin: "))
                new_belde = belde_adaylari[secim - 1]
            except:
                print("❗ Geçersiz giriş. Varsayılan belde atanıyor.")
                new_belde = f"{new_ilce.upper()}-DISTRICT CENTER"
        else:
            new_belde = f"{new_ilce.upper()}-DISTRICT CENTER"
            print(f"ℹ️ Bu ilçede belde bulunamadı. Varsayılan belde atandı: {new_belde}")

    # Eşleşen mahalleleri bul klasik döngü
    eslesenler = [
        item for item in data
        if item['il'] == old_il and item['ilce'] == old_ilce and item['mahalle'] == mahalle
    ]

    if not eslesenler:
        print("❗ Girilen bilgilerle eşleşen mahalle bulunamadı.")
        return

    # Eski kaydı ramden silip sonrasında çakışma olmamasını sağla
    data[:] = [
        item for item in data
        if not (
            item['il'] == old_il and
            item['ilce'] == old_ilce and
            item['mahalle'] == mahalle
        )
    ]

    # Yeni kaydı ekle
    data.append({
        "mahalle": mahalle,
        "il": new_il,
        "ilce": new_ilce,
        "belde": new_belde
    })

    print(f"\n✅ '{mahalle.upper()}' mahallesi başarıyla {old_ilce.upper()} → {new_ilce.upper()} taşındı.")  #bilgilendirme mesajı

    # Yeni ilçedeki güncel mahalleleri yazdır
    yeni_mahalleler = [
        item for item in data
        if item['il'] == new_il and item['ilce'] == new_ilce
    ]

    print(f"\n📍 {new_il.upper()} / {new_ilce.upper()} ilçesindeki güncel mahalleler:")
    if not yeni_mahalleler:
        print("❗ Bu ilçede mahalle bulunamadı.")
    else:
        for n in yeni_mahalleler:
            print(f"İl: {n['il'].capitalize()}, İlçe: {n['ilce'].capitalize()}, "
                  f"Mahalle: {n['mahalle'].capitalize()}, Belde: {n['belde']}")

    # Dosyaya kalıcı olarak kaydet
    try:
        with open("neighborhoods.txt", "w", encoding="utf-8") as file:
            for item in data:
                line = f"{item['mahalle'].upper()} {item['il'].upper()} -> {item['ilce'].upper()} -> {item['belde']}\n"
                file.write(line)
        print("\n💾 Değişiklikler dosyaya kaydedildi.")
    except Exception as e:
        print("❌ Dosya kaydı sırasında hata oluştu:", e)
