import io
import sys
from PIL import Image
from pypdf import PdfReader

def dump_images(pdf_filename):
    reader = PdfReader(pdf_filename)
    number_of_pages = len(reader.pages)
    print(f"{pdf_filename}: {number_of_pages} pages")
    for page_number, page in enumerate(reader.pages, start=1):
        print(f"{page_number}/{number_of_pages}")
        for img_num, img_fp in enumerate(page.images, start=1):
            img_filename = f"{page_number:02d}-{img_fp.name}"
            print(f"  {img_filename}")
            with open(img_filename, "wb") as fp:
                fp.write(img_fp.data)

class Band:
    def __init__(self, filename, pagenum, imgnum=0, rotate=0):
        pdf = PdfReader(filename)
        pdfimg = pdf.pages[pagenum].images[imgnum]
        img = Image.open(io.BytesIO(pdfimg.data))
        if rotate != 0:
            img = img.rotate(rotate, expand=True)

def main():
    for pdf_filename in sys.argv[1:]:
        process(pdf_filename)

if __name__ == "__main__":
    main()
