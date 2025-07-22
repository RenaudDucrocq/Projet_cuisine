from document_text_annotations import main
from parse_methods import parse

if __name__ == "__main__":
    main.render_full_text("images/IMG_3061.jpg", "document_text_annotations/outputs/output.txt")
    parse.parse("document_text_annotations/outputs/output.txt", )
