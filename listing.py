import file_loader

# Türkçe karakter sıkıntısı olmamasi için 
def normalize(text):
    return text.replace('İ', 'i').replace('I', 'i').replace('Ü', 'ü') \
               .replace('Ö', 'ö').replace('Ç', 'ç').replace('Ş', 'ş') \
               .replace('Ğ', 'ğ').lower()


# Belirtilen ildeki tüm mahalleleri listeler.
def list_neighborhoods_by_province(data, province_name, ascending=True):
    province_lower = normalize(province_name)
    filtered_neighborhoods = [
        n for n in data if normalize(n['il']) == province_lower
    ]
    sorted_neighborhoods = sorted(#sıraya dizme işlemi python yerleşik fonksiyonu
        filtered_neighborhoods, key=lambda x: x['mahalle'], reverse=not ascending#lambda fonksiyonu : mahalle ismine göre sıralama 
    )                                                                             #asceding parametresi ile artan/azalan sıralama

    if not sorted_neighborhoods:
        print(f"{province_name} ilinde mahalle bulunamadı.")
        return

    print(f"\n{province_name} ilindeki mahalleler:")
    for n in sorted_neighborhoods:
        print(f"İl: {n['il'].capitalize()}, İlçe: {n['ilce'].capitalize()}, Mahalle: {n['mahalle'].capitalize()}, Belde/Merkez: {n['belde'].capitalize()}")


#burda da aynı şeyi ilçe bazında yapıyor
def list_neighborhoods_by_district(data, province_name, district_name, ascending=True):
    province_lower = normalize(province_name)
    district_lower = normalize(district_name)
    filtered_neighborhoods = [
        n for n in data
        if normalize(n['il']) == province_lower and normalize(n['ilce']) == district_lower
    ]
    sorted_neighborhoods = sorted(
        filtered_neighborhoods, key=lambda x: x['mahalle'], reverse=not ascending
    )

    if not sorted_neighborhoods:
        print(f"{province_name}/{district_name} ilçesinde mahalle bulunamadı.")
        return

    print(f"\n{province_name}/{district_name} ilçesindeki mahalleler:")
    for n in sorted_neighborhoods:
        print(f"İl: {n['il'].capitalize()}, İlçe: {n['ilce'].capitalize()}, Mahalle: {n['mahalle'].capitalize()}, Belde/Merkez: {n['belde'].capitalize()}")


def get_sorting_choice():
    while True:
        choice = input("Artan (A) veya azalan (Z) sırada listelemek ister misiniz? (A/Z): ").strip().upper()
        if choice in ('A', 'Z'): # A ise 1 (artı), Z ise 0 (azalan) 
            return choice == 'A'
        else:
            print("Geçersiz seçim. Lütfen 'A' veya 'Z' girin.")


#burda da main.py ile entegre olabilmesi için interface fonksiyonu
def run_listing(data):
    tercih = input("İl mi ilçe mi listelemek istersiniz? (il/ilçe): ").strip().lower()

    if tercih == "il":
        il_adi = input("İl adını girin: ").strip()  # normalize ETME burada!
        ascending = get_sorting_choice()
        list_neighborhoods_by_province(data, il_adi, ascending)

    elif tercih == "ilçe":
        il_adi = input("İl adını girin: ").strip()  # normalize ETME burada!
        ilce_adi = input("İlçe adını girin: ").strip()
        ascending = get_sorting_choice()
        list_neighborhoods_by_district(data, il_adi, ilce_adi, ascending)

    else:
        print("❌ Geçersiz seçim. 'il' veya 'ilçe' yazmalısınız.")
