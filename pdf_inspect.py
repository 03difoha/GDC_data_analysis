import pymupdf
import os
import shutil  # for copying files

keywords = ["diagnosis", "markers", "type", "grade", "features", "treatment", "surgery", "status", "uuid", "date"]
count = 0
folder_path = "/GDC_data_analysis/breast_lung copy/lung_annotated"
target_folder = "/GDC_data_analysis/lung_final"

# Make sure the target folder exists
os.makedirs(target_folder, exist_ok=True)

for filename in os.listdir(folder_path):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(folder_path, filename)
        print(f"\n=== {filename} ===")
        try:
            doc = pymupdf.open(file_path)
            full_text = ""
            for page in doc:
                full_text += page.get_text().lower()

            found = [kw for kw in keywords if kw in full_text]

            if len(found) >= 6:
                count += 1
                # Copy the file to the lung folder
                target_path = os.path.join(target_folder, filename)
                shutil.copy(file_path, target_path)
                print(f"✔ Copied: {filename} | Found keywords: {found}")

            doc.close()
        except Exception as e:
            print(f"Error reading {filename}: {e}")

print(f"\nTotal files copied to {target_folder}: {count}")
