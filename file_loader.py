import re

# Türkçe karakter sıkıntısı olmaması için
def normalize(text):
    return text.replace('İ', 'i').replace('Ü', 'ü').replace('I', 'i') \
               .replace('Ö', 'ö').replace('Ç', 'ç').replace('Ş', 'ş') \
               .replace('Ğ', 'ğ').lower()

def load_neighborhood_data(file_path):
    neighborhoods_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or '->' not in line:  # Boş satırları ve '->' olmayan satırları atlamaya yarıyor
                    continue

                parts = [part.strip() for part in re.split(r'->', line)]  # '->' ile ayırma
                if len(parts) < 2 or len(parts) > 3:  # 2 veya 3 parçadan fazlası varsa geçersiz format
                    print(f"UYARI: Beklenmeyen format: {line}")
                    continue

                # Mahalle + İl bilgisi her zaman parts[0]'dadır
                mahalle_il_bilgisi = parts[0]
                kelimeler = mahalle_il_bilgisi.split()

                if not kelimeler:
                    print(f"UYARI: İl/Mahalle bilgisi boş: {mahalle_il_bilgisi}")
                    continue

                il_ham = kelimeler[-1]
                mahalle_ham = " ".join(kelimeler[:-1])

                # Türkçe karakter sıkıntısı olmaması için normalize işlemleri
                il = normalize(il_ham)
                mahalle = normalize(mahalle_ham)

                # İlçe ve belde bilgileri satır yapısına göre belirlenir
                if len(parts) == 3:  # Eğer 3 parçaysa, ilçe ve belde bilgisi var demektir
                    ilce_ham = parts[1]
                    belde_ham = parts[2]
                elif "-DISTRICT CENTER" in parts[-1].upper() or "-PROVINCE CENTER" in parts[-1].upper():
                    ilce_ham = il
                    belde_ham = il
                else:
                    ilce_ham = parts[-1].split()[0]
                    belde_ham = ilce_ham

                ilce = normalize(ilce_ham)
                belde = normalize(belde_ham).replace('-district center', '').replace('-province center', '').strip()

                # Verileri listeye ekleme
                neighborhoods_data.append({
                    'il': il,
                    'ilce': ilce,
                    'mahalle': mahalle,
                    'belde': belde
                })

        return neighborhoods_data
    except FileNotFoundError:
        print(f"Hata: '{file_path}' dosyası bulunamadı.")
        return None
    except Exception as e:
        print(f"Hata: Dosya okunurken bir sorun oluştu: {e}")
        return None
