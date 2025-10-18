from pdf_utils import extractLinks

if __name__ == "__main__":
    links = extractLinks("./Pitches.pdf")
    print(links)