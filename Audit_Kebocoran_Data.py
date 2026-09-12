import pandas as pd
import itertools
import os

print("="*60)
print("AUDIT KEBOCORAN DATA (DATA LEAKAGE) TA BIOAKUSTIK")
print("="*60)

# 1. Load dataset split
csv_path = r'data\manifests\dataset_split.csv'
if not os.path.exists(csv_path):
    print(f"Error: File {csv_path} tidak ditemukan. Pastikan script di-run dari root directory.")
    exit(1)

df = pd.read_csv(csv_path)
print(f"Total data dalam manifest: {len(df)} baris.\n")

# 2. Uji Kebocoran ID (Recording ID Xeno-Canto)
print("[1] MENGUJI KEBOCORAN ID XENO-CANTO (RECORDING ID)")
splits_id = df.groupby('split_role')['id'].apply(set).to_dict()
leak_id = False
for s1, s2 in itertools.combinations(splits_id.keys(), 2):
    intersect = splits_id[s1].intersection(splits_id[s2])
    if intersect:
        print(f"  [X] GAGAL: Ditemukan {len(intersect)} ID rekaman yang sama antara '{s1}' dan '{s2}'")
        leak_id = True
if not leak_id:
    print("  [V] AMAN: Tidak ada satu pun ID rekaman (XC) yang tumpang tindih antar himpunan (gallery/query/test/calib).\n")

# 3. Uji Kebocoran HASH (Duplicate File Content)
print("[2] MENGUJI KEBOCORAN KONTEN AUDIO SAMA PERSIS (SHA-256 HASH)")
# Abaikan data tanpa hash (NaN)
df_hash = df[df['sha256'].notna() & (df['sha256'] != '')]
splits_hash = df_hash.groupby('split_role')['sha256'].apply(set).to_dict()
leak_hash = False
for s1, s2 in itertools.combinations(splits_hash.keys(), 2):
    intersect = splits_hash[s1].intersection(splits_hash[s2])
    if intersect:
        print(f"  [X] GAGAL: Ditemukan {len(intersect)} file audio dengan hash identik antara '{s1}' dan '{s2}'")
        leak_hash = True
if not leak_hash:
    print("  [V] AMAN: Tidak ada file audio dengan isian suara identik yang bocor menyilang antar himpunan.\n")

# 4. Uji Kebocoran Sesi (Session Leakage) -> Spesies, Perekam, Tanggal, dan Lokasi yang sama
print("[3] MENGUJI KEBOCORAN SESI REKAMAN (SPESIES + PEREKAM + TANGGAL + LOKASI)")
gal = df[df['split_role'] == 'gallery']
q = df[df['split_role'] == 'query_clean']
merged_session = pd.merge(gal, q, on=['species_key', 'recordist', 'date', 'locality'], suffixes=('_gal', '_q'))
if len(merged_session) > 0:
    print(f"  [X] GAGAL: Terdapat {len(merged_session)} sesi rekaman yang bocor antara Gallery dan Query.")
else:
    print("  [V] AMAN: Tidak ada sesi perekaman yang sama persis terpisah ke dalam Gallery dan Query.\n")

# 5. Uji Kebocoran Kelas Open-Set
print("[4] MENGUJI KEBOCORAN KELAS OPEN-SET (GALLERY VS UNKNOWN TEST)")
gal_sps = set(df[df['split_role']=='gallery']['species_key'])
unk_sps = set(df[df['split_role']=='unknown_test']['species_key'])
species_leak = gal_sps.intersection(unk_sps)
if species_leak:
    print(f"  [X] GAGAL: Terdapat {len(species_leak)} spesies Gallery yang muncul di Unknown Test!")
else:
    print("  [V] AMAN: Seluruh data Unknown Test benar-benar berisi spesies asing yang tidak ada di Gallery.\n")

print("="*60)
print("KESIMPULAN:")
if leak_id or leak_hash or len(merged_session)>0 or len(species_leak)>0:
    print(">>> TERDAPAT KEBOCORAN DATA YANG FATAL. Anda harus memodifikasi split di dataset_split.csv")
else:
    print(">>> DATASET BERSIH DARI KEBOCORAN INTERNAL.")
    print(">>> Jika pembimbing menyatakan 'ada data yang sama', kemungkinan besar yang dimaksud adalah:")
    print("    1. BirdNET (R2) pernah dilatih dengan file Xeno-Canto tersebut di masa lalu (Pre-training Leakage).")
    print("    2. Ada recordist yang menyumbang rekaman berbeda untuk Gallery dan Query.")
print("="*60)
