from listing import run_listing
from deleting import run_deleting
from file_loader import load_neighborhood_data
from moving import run_moving
from analyzing import run_analysis
from graphics import plot_neighborhoods_pie_chart, plot_neighborhoods_bar_chart
from search import search_exact, search_partial
from adding import adding_new_neighborhood
from updating import update_neighborhood
def main():
    data = load_neighborhood_data("neighborhoods.txt")

    if not data:
        print("❌ Veri yüklenemedi. Lütfen dosya adını ve konumunu kontrol edin.")
        return

    print("\n👋 Merhaba! Türkiye Mahalle Bilgi Sistemi'ne hoş geldiniz.")
    print("*"*20 + " NOT: 'ı'  yerine 'i' kullanınız " + "*" * 20)
    while True:
        print("\n" + "=" * 50)
        print("📋 ANA MENÜ")
        print("=" * 50)
        print("1️⃣  Mahalle arama")
        print("2️⃣  Mahalle listeleme")
        print("3️⃣  Mahalle ekleme")
        print("4️⃣  Mahalle silme")
        print("5️⃣  Mahalle güncelleme")
        print("6️⃣  Mahalle taşıma")
        print("7️⃣  Grafiklerle Görselleştirme")
        print("8️⃣  Mahalle analizi")
        print("0️⃣  Çıkış")

        secim = input("\n🔎 Bir işlem seçin (0-8): ").strip()
        print("\n" + "-" * 50 + "\n")

        if secim == "7":
            print("📊 Grafik Türü Seçin")
            print("7.1 → 🟦 Bar Grafik (İlçe bazlı mahalle sayısı)")
            print("7.2 → 🥧 Pie Grafik (İlçe oranlarına göre mahalle)")
            secim = input("Seçiminiz (7.1 / 7.2): ").strip()

        elif secim == "1":
            print("🔍 Arama Türü Seçin")
            print("1.1 → Tam eşleşme ile arama")
            print("1.2 → Kısmi eşleşme ile arama")
            secim = input("Seçiminiz (1.1 / 1.2): ").strip()

        # ----- SEÇİM İŞLEMLERİ -----
        if secim == "1.1":
            search_exact(data)
        elif secim == "1.2":
            search_partial(data)
        elif secim == "2":
            run_listing(data)
        elif secim == "3":
            adding_new_neighborhood(data)
        elif secim == "4":
            run_deleting(data)
        elif secim == "5":
            update_neighborhood(data)
        elif secim == "6":
            run_moving(data)
        elif secim == "7.1":
            plot_neighborhoods_bar_chart(data)
        elif secim == "7.2":
            plot_neighborhoods_pie_chart(data)
        elif secim == "8":
            run_analysis(data)
        elif secim == "0":
            print("👋 Programdan çıkılıyor. Görüşmek üzere!")
            break
        else:
            print("❌ Geçersiz giriş. Lütfen 0-8 arasında bir sayı veya alt seçim giriniz.")

if __name__ == "__main__":
    main()
