import os, io
from google.cloud import vision
from google.cloud.vision_v1 import types

from dotenv import load_dotenv
load_dotenv() 


client = vision.ImageAnnotatorClient()

folder = r'C:\Users\ljant\Desktop\Ironhack\Projects\Final-Project-Ironhack-2024\Google\VisionApi\images'
img = 'test1.png'
file_path = os.path.join(folder, img)

with io.open(file_path, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content = content)
response = client.document_text_detection(image = image)

docText = response.full_text_annotation.text
print(docText)

block_confidences = []
paragraph_confidences = []

pages = response.full_text_annotation.pages
for page in pages:
    for block in page.blocks:
        block_confidences.append(block.confidence)
        for paragraph in block.paragraphs:
            paragraph_confidences.append(paragraph.confidence)

average_block_confidence = round((sum(block_confidences) / len(block_confidences)) * 100, 2)
average_paragraph_confidence = round((sum(paragraph_confidences) / len(paragraph_confidences)) * 100, 2)

print("Average block confidence:", average_block_confidence, "%")
print("Average paragraph confidence:", average_paragraph_confidence, "%")

with open("docText.txt", "w") as file:
    file.write(docText)

