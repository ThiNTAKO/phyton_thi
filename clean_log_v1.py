# Step 1: Convert the PNG image into a PDF using ReportLab
image_pdf = "image_as_pdf.pdf"
canvas_obj = canvas.Canvas(image_pdf, pagesize=letter)

# Add the image to the PDF, adjust width and height as needed
image_path = "Graph.png"
canvas_obj.drawImage(image_path, 0, 0, width=letter[0], height=letter[1], preserveAspectRatio=True)
canvas_obj.showPage()
canvas_obj.save()

print(f"Image PDF saved to: {image_pdf}")


def merge_pdfs(input_pdfs, output_pdf):
    merger = PyPDF2.PdfMerger()

    try:
        # Iterate over each input PDF in the list and append it
        for pdf in input_pdfs:
            merger.append(pdf)

        # Write the merged PDF to the output file
        with open(output_pdf, 'wb') as merged_pdf:
            merger.write(merged_pdf)
        print(f'Merged PDFs successfully. Output saved to: {output_pdf}')
    except Exception as e:
        print(f'Error merging PDFs: {e}')

# Example usage

input_pdfs = [image_pdf, "rapport_vulnerabilites_ThiNTA.pdf"]  # List of PDFs to merge
output_pdf = 'merged_output.pdf'

merge_pdfs(input_pdfs, output_pdf)
