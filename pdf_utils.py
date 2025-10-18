import logging
from pypdf import PdfReader


def extractLinks(pdf_path):
    """Extract ordered unique link URIs from a PDF and return as a list.

    Uses pypdf in tolerant mode and suppresses non-critical logging from
    the library. Returns a Python list of URIs in first-seen order.
    """
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    reader = PdfReader(pdf_path, strict=False)

    seen = set()
    ordered = []
    for page in reader.pages:
        annots = page.get("/Annots")
        if not annots:
            continue
        for annot in annots:
            try:
                uri = annot.get_object().get("/A", {}).get("/URI")
            except Exception:
                continue
            if not uri:
                continue
            if uri in seen:
                continue
            seen.add(uri)
            ordered.append(uri)
    return ordered[1:]


if __name__ == "__main__":
    links = extractLinks("./Pitches.pdf")
    print(links)