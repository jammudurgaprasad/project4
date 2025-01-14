import chardet

# Detect file encoding
with open("data.json", "rb") as f:
    raw_data = f.read()
    detected = chardet.detect(raw_data)
    encoding = detected['encoding']
    print(f"Detected Encoding: {encoding}")

# Re-encode to UTF-8
with open("data.json", "rb") as f:
    content = f.read()

with open("cleaned_data.json", "w", encoding="utf-8") as f:
    f.write(content.decode(encoding))
print("File re-encoded to UTF-8 as 'cleaned_data.json'.")
