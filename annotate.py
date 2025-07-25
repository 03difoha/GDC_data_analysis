import os
import csv
import pymupdf  # PyMuPDF
import shutil
from collections import defaultdict
# === CONFIGURATION ===
textlist_folder = "~/GDC_data_analysis/manifests"   # Folder with .txt files
pdf_folder = "~/GDC_data_analysis/breast_lung copy/output/lung"             # Source folder for PDFs
output_folder = "~/GDC_data_analysis/breast_lung copy/lung_annotated"     # Folder to save annotated PDFs

os.makedirs(output_folder, exist_ok=True)

# === STEP 1: Map PDF filenames to a list of source .txt files ===
pdf_to_annotations = defaultdict(list)

for txt_file in os.listdir(textlist_folder):
    if txt_file.lower().endswith(".txt"):
        annotation_text = os.path.splitext(txt_file)[0]  # Remove .txt extension
        txt_path = os.path.join(textlist_folder, txt_file)

        try:
            with open(txt_path, "r", newline='') as file:
                reader = csv.DictReader(file, delimiter="\t")
                for row in reader:
                    filename = row["filename"].strip().lower()
                    pdf_to_annotations[filename].append(annotation_text)
        except Exception as e:
            print(f"❌ Error reading {txt_file}: {e}")

# === STEP 2: Annotate PDFs ===
for filename in os.listdir(pdf_folder):
    filename_lower = filename.lower()
    if filename_lower in pdf_to_annotations and filename_lower.endswith(".pdf"):
        src_pdf = os.path.join(pdf_folder, filename)
        dst_pdf = os.path.join(output_folder, filename)

        try:
            doc = pymupdf.open(src_pdf)

            # Create a new page at the end
            page = doc.new_page()
            x, y = 72, 72  # Starting position (1 inch margin)
            line_spacing = 18  # Vertical space between lines

            for i, annotation in enumerate(pdf_to_annotations[filename_lower]):
                page.insert_text(
                    (x, y + i * line_spacing),
                    annotation,
                    fontsize=14,
                    color=(0, 0, 0)
                )

            doc.save(dst_pdf)
            doc.close()

            print(f"✔ Annotated {filename} with {len(pdf_to_annotations[filename_lower])} labels")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

print("\n✅ All PDFs annotated with multiple source references.")