import matplotlib.pyplot as plt
from collections import Counter

# ------------------------- BAR GRAFİK -------------------------
def plot_neighborhoods_bar_chart(data):
    """Seçilen ildeki ilçelere göre mahalle sayılarını çubuk grafikle gösterir."""

    # Türkçe karakter sıkıntısı olmaması için normalize fonksiyonu
    def normalize(text):
        return text.replace('İ', 'i').replace('I', 'i') \
                   .replace('Ü', 'ü').replace('Ö', 'ö') \
                   .replace('Ç', 'ç').replace('Ş', 'ş') \
                   .replace('Ğ', 'ğ').lower()

    # Kullanıcıdan il adı alınır
    il_adi = normalize(input("Bar grafik için il adı: ").strip())

    # Eğer il bulunamazsa kullanıcı uyarılır
    iller = set(item['il'] for item in data)
    if il_adi not in iller:
        print("❌ İl bulunamadı.")
        print(f"📌 Uygun iller: {', '.join(sorted([il.upper() for il in iller]))}")
        return

    # İlçeye göre mahalle sayısı hesaplanır
    district_counts = Counter()
    for item in data:
        if item['il'] == il_adi:
            temiz_ilce = item['ilce'].replace("district center", "").replace("province center", "") \
                                     .replace("district", "").strip().title()
            district_counts[temiz_ilce] += 1

    if not district_counts:
        print("❗ İlçelerde mahalle bulunamadı.")
        return

    # Bar grafik çizimi
    plt.figure(figsize=(16, 8))
    bars = plt.bar(district_counts.keys(), district_counts.values(), color=plt.cm.tab20.colors)

    # Her bar'ın üstüne mahalle sayısı yazılır
    for bar, count in zip(bars, district_counts.values()):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), str(count), ha='center', va='bottom')

    # Grafik başlık ve eksen etiketleri
    plt.title(f"{il_adi.upper()} İLİ İLÇE BAZLI MAHALLE SAYILARI", fontsize=14, fontweight='bold')
    plt.xlabel("İlçeler")
    plt.ylabel("Mahalle Sayısı")
    plt.xticks(rotation=65, ha='right')
    plt.tight_layout()
    plt.show()


# ------------------------- PIE GRAFİK -------------------------
def plot_neighborhoods_pie_chart(data):
    """Seçilen ildeki ilçelere göre mahalle sayılarını pasta grafikle gösterir."""

    # Türkçe karakter sıkıntısı olmaması için normalize fonksiyonu
    def normalize(text):
        return text.replace('İ', 'i').replace('I', 'ı') \
                   .replace('Ü', 'ü').replace('Ö', 'ö') \
                   .replace('Ç', 'ç').replace('Ş', 'ş') \
                   .replace('Ğ', 'ğ').lower()

    # Kullanıcıdan il adı alınır
    il_adi = normalize(input("Pie grafik için il adı: ").strip())

    # Eğer il bulunamazsa kullanıcı uyarılır
    iller = set(item['il'] for item in data)
    if il_adi not in iller:
        print("❌ İl bulunamadı.")
        print(f"📌 Uygun iller: {', '.join(sorted([il.upper() for il in iller]))}")
        return

    # İlçeye göre mahalle sayısı hesaplanır
    district_counts = Counter()
    for item in data:
        if item['il'] == il_adi:
            temiz_ilce = item['ilce'].replace("district center", "").replace("province center", "") \
                                     .replace("district", "").strip().title()
            district_counts[temiz_ilce] += 1

    if not district_counts:
        print("❗ İlçelerde mahalle bulunamadı.")
        return

    # Veri ayrıştırma
    labels = list(district_counts.keys())
    sizes = list(district_counts.values())
    colors = plt.cm.Set3.colors[:len(labels)]

    # Pie grafik çizimi
    plt.figure(figsize=(10, 8))
    wedges, texts, autotexts = plt.pie(
        sizes,
        autopct='%1.0f%%',
        startangle=90,
        colors=colors,
        textprops=dict(color="black", fontsize=10)
    )

    # Legend (açıklama kutusu) sağda
    plt.legend(wedges, labels, title="İlçeler", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9)

    # Grafik başlık
    plt.title(f"{il_adi.upper()} İLİNE AİT MAHALLE ORANLARI", fontsize=14, weight='bold')
    plt.axis("equal")  # Daire düzgün görünmesi için
    plt.tight_layout()
    plt.show()
