import pandas as pd

df = pd.read_csv('d:\\TUGAS AKHIR\\DSIC-2706-main\\data\\manifests\\dataset_split.csv')
gal = df[df['split_role'] == 'gallery']
q = df[df['split_role'] == 'query_clean']

# Check for session leakage: same species, same recordist, same date, same locality
merged = pd.merge(gal, q, on=['species_key', 'recordist', 'date', 'locality'], suffixes=('_gal', '_q'))

print(f"Number of Session Leakages: {len(merged)}")
if len(merged) > 0:
    print(merged[['species_key', 'recordist', 'date', 'locality', 'id_gal', 'id_q']])

# Also let's check between Calibration and Test, etc.
# Actually, the simplest check is: does any recordist have files in Gallery and Query?
gal_recordists = set(gal['recordist'].dropna())
q_recordists = set(q['recordist'].dropna())
overlap_rec = gal_recordists.intersection(q_recordists)
print(f"Recordist overlap Gallery vs Query: {overlap_rec}")
