CLASS_NAMES_FILE = ARTIFACTS_DIR / "class_names.json"

print("=" * 60)
print("CLASS_NAMES_FILE:", CLASS_NAMES_FILE)
print("Exists:", CLASS_NAMES_FILE.exists())

if CLASS_NAMES_FILE.exists():
    with open(CLASS_NAMES_FILE, "r", encoding="utf-8") as file:
        CLASS_NAMES = json.load(file)

    print("Type:", type(CLASS_NAMES))
    print("Length:", len(CLASS_NAMES))

    if len(CLASS_NAMES) > 0:
        print("First class:", CLASS_NAMES[0])

else:
    print("File not found!")
    CLASS_NAMES = []

NUM_CLASSES = len(CLASS_NAMES)
print("NUM_CLASSES =", NUM_CLASSES)
print("=" * 60)