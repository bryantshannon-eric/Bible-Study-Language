import pandas as pd
import json

# == note- this script converts an excel file to a json file, need to update the source name and output name.

# === CONFIG ===
excel_file = "GreekNT for conversion.xlsx"   # Your Excel file
output_file = "GreekNT.json"
version_code = "Greek"
version_name = "KoineGreek"

# === LOAD EXCEL ===
excel_data = pd.ExcelFile(excel_file)
df = excel_data.parse(excel_data.sheet_names[0])

# Drop header rows
df = df.drop([0, 1]).reset_index(drop=True)

# Keep only needed columns
df = df[['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']]
df.columns = ['Book', 'Chapter', 'Verse', 'Text']

# Drop empty rows
df = df.dropna(subset=['Text'])

# === BUILD JSON ===
bible_json = {
    version_code: {
        "name": version_name,
        "books": {}
    }
}

for _, row in df.iterrows():
    book = str(row['Book'])
    chapter = str(row['Chapter'])
    verse = str(row['Verse'])
    text = str(row['Text'])

    books = bible_json[version_code]["books"]
    if book not in books:
        books[book] = {}
    if chapter not in books[book]:
        books[book][chapter] = {}
    books[book][chapter][verse] = text

# === SAVE JSON ===
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(bible_json, f, ensure_ascii=False, indent=2)

print(f"✅ Conversion complete! JSON saved as {output_file}")
