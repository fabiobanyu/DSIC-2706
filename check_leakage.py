import pandas as pd
import itertools

df = pd.read_csv('d:\\TUGAS AKHIR\\DSIC-2706-main\\data\\manifests\\dataset_split.csv')

print("=== ID LEAKAGE AUDIT ===")
splits_id = df.groupby('split_role')['id'].apply(set).to_dict()
leak = False
for s1, s2 in itertools.combinations(splits_id.keys(), 2):
    intersect = splits_id[s1].intersection(splits_id[s2])
    if intersect:
        print(f"LEAKAGE between {s1} and {s2}: {len(intersect)} IDs overlap (e.g., {list(intersect)[:3]})")
        leak = True
if not leak:
    print("No ID leakage detected.")

print("\n=== RECORDIST OVERLAP AUDIT ===")
splits_rec = df.groupby('split_role')['recordist'].apply(set).to_dict()
rec_overlap = False
for s1, s2 in itertools.combinations(splits_rec.keys(), 2):
    intersect = splits_rec[s1].intersection(splits_rec[s2])
    if intersect:
        print(f"Recordist Overlap between {s1} and {s2}: {len(intersect)} recordists overlap")
        print(f"  Names: {list(intersect)[:5]}")
        rec_overlap = True
if not rec_overlap:
    print("No Recordist leakage detected.")
