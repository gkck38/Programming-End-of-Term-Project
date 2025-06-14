from collections import Counter
import math

#en çok geçen mahalle adlarını bulmak için Counter modülünü kullanır
def most_common_neighborhoods(data):
    counts = Counter([item['mahalle'] for item in data])
    max_count = max(counts.values()) #max_count değişkeni ile en çok geçen mahalle sayısını bulur

    most_common = [name for name, count in counts.items() if count == max_count] #items() ile mahalle adlarını ve sayısını alır
    print("\n En sık geçen mahalle ad(lar)ı:")
    for name in most_common:
        print(f"{name.upper()} ({max_count} kez)")

#en az ve en çok mahalleye sahip illeri bulmak için Counter modülünü kullanır
def province_neighborhood_extremes(data):
    province_counts = Counter([item['il'] for item in data])
    max_count = max(province_counts.values()) # max fonksiyonu ile en çok mahalleye sahip il(ler)in sayısını bulur
    min_count = min(province_counts.values()) # min fonksiyonu ile en az mahalleye sahip il(ler)in sayısını bulur

    most = [il for il, count in province_counts.items() if count == max_count] 
    least = [il for il, count in province_counts.items() if count == min_count]

    print("\n En çok mahalleye sahip il(ler):")
    for il in most:
        print(f"{il.upper()} ({max_count} mahalle)")

    print("\n En az mahalleye sahip il(ler):")
    for il in least:
        print(f"{il.upper()} ({min_count} mahalle)")

#standart sapma ve ortalama hesaplamak için
def province_neighborhood_stats(data):
    province_counts = Counter([item['il'] for item in data])
    counts = list(province_counts.values())

    mean = sum(counts) / len(counts)

    variance = sum((x - mean) ** 2 for x in counts) / len(counts)  #burdaki işlemleri intten buldum bilmiyom
    std_dev = math.sqrt(variance)

    print("\n İllerdeki mahalle sayısı ortalaması ve standart sapması:")
    print(f"Ortalama mahalle sayısı: {mean:.2f}")
    print(f"Standart sapma        : {std_dev:.2f}")


def run_analysis(data):
    print("\n--- MAHALLE VERİ ANALİZİ ---")
    most_common_neighborhoods(data)
    province_neighborhood_extremes(data)
    province_neighborhood_stats(data)
