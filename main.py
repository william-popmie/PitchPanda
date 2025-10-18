from pypdf import PdfReader

reader = PdfReader("./Pitches.pdf")

links = []

for page in reader.pages:
    annots = page.get("/Annots")
    if annots:
        for annot in annots:
            uri = annot.get_object().get("/A", {}).get("/URI")
            if uri:
                links.append(uri)

print(f"Found {len(links)} links:")

for link in links:
    print(link)
