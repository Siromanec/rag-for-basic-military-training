import pathlib

import fitz


def extract_images_from_pdf(pdf_path: pathlib.Path):
    pdf_document = fitz.open(pdf_path)

    output_folder = pdf_path.parent / "extracted_images" / pdf_path.stem
    output_folder.mkdir(parents=True, exist_ok=True)

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = output_folder / f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
    pdf_document.close()


if __name__ == "__main__":
    for pdf_path in (pathlib.Path(__file__).absolute().parent.parent.parent.parent / "data").glob("*.pdf"):
        extract_images_from_pdf(pdf_path)
