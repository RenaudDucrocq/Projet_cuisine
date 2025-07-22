import json

from google.cloud import vision
from google.protobuf.json_format import MessageToJson

client = vision.ImageAnnotatorClient(
    #client_options={"api_key": "AIzaSyCBBmP6xXD7sgU3lQ0dtxMbKEakKb2w_gA"}
)

with open("../../images/IMG_3061.jpg", "rb") as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations
print("Texts:")

with open("../outputs/output.json", "w") as output_file:
    json_obj = MessageToJson((response._pb))
    json.dump(json_obj, output_file, indent=2)


# for text in texts:
#     print(f'\n"{text.description}"')
#
#     vertices = [
#         f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
#     ]
#
#     print("bounds: {}".format(",".join(vertices)))

if response.error.message:
    raise Exception(
        "{}\nFor more info on error messages, check: "
        "https://cloud.google.com/apis/design/errors".format(response.error.message)
    )
