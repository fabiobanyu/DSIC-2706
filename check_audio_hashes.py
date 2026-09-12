import glob, hashlib, os

files = glob.glob('d:\\TUGAS AKHIR\\DSIC-2706-main\\data\\xeno_canto\\**\\*.*', recursive=True)
hashes = {}
leak = False

print(f"Checking {len(files)} local files for identical content...")

for f in files:
    if not os.path.isfile(f): continue
    h = hashlib.sha256(open(f, 'rb').read()).hexdigest()
    if h in hashes:
        print(f"DUPLICATE DETECTED:\n  1) {f}\n  2) {hashes[h]}")
        leak = True
    hashes[h] = f

if not leak:
    print("No duplicate audio content found locally.")
