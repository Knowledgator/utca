from typing import Dict, Any, Type, get_origin
# import pprint
# import uuid

from core.executable_level_1.actions import (
    Action,
    OneToOne,
    OneToMany,
    ManyToMany,
    ManyToOne,
    ExecuteFunction
)

def one_to_one(a: Dict[str, Any]) -> Dict[str, Any]:
    return a

a = ExecuteFunction(one_to_one)

print(type(a))
# print(type(a) is Action[Dict[str, Any], Dict[str, Any]])

# from implementation.datasources.pdf.actions import (
#     PDFRead, PDFExtractTexts, PDFExtractTables,
#     PDFExtractImages
# )
# from implementation.datasources.image.actions import (
#     ImageWrite
# )

# pages = PDFRead().execute({
#     "path_to_file": "programs/test/pfizer-report.pdf",
#     "pages": [91]
# })

# # for page_id, images in PDFExtractImages().execute(pages).items():
# #     for image in images:
# #         ImageWrite().execute({
# #             "path_to_file": str(uuid.uuid4()) + ".png",
# #             "image": image
# #         })

# with open('test.txt', 'w') as f:
#     f.write(PDFExtractTexts().execute(pages)["pdf_texts"][91])