import pandas as pd
import itertools

df = pd.read_csv('d:\\TUGAS AKHIR\\DSIC-2706-main\\data\\manifests\\dataset_split.csv')

# Exclude empty hashes if any
df = df[df['sha256'].notna() & (df['sha256'] != '')]

dups = df[df.duplicated(subset=['sha256'], keep=False)]
print(f"Total files sharing hashes: {len(dups)}")

splits_hash = df.groupby('split_role')['sha256'].apply(set).to_dict()

leak = False
for s1, s2 in itertools.combinations(splits_hash.keys(), 2):
    intersect = splits_hash[s1].intersection(splits_hash[s2])
    if intersect:
        print(f"LEAKAGE FATAL between {s1} and {s2}: {len(intersect)} duplicated audio hashes!")
        leak = True

if not leak:
    print("No hash leakage between splits. The duplicates are internal to each split.")
