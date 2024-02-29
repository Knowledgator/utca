from transformers import AutoProcessor, AutoModelForQuestionAnswering
import torch

from PIL import Image

processor = AutoProcessor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=False)
model = AutoModelForQuestionAnswering.from_pretrained("microsoft/layoutlmv3-base")

# dataset = load_dataset("nielsr/funsd-layoutlmv3", split="train")
# example = dataset[0]
image = Image.open("programs/image_processing/layout_processing/test.png")
question = "Does Italy has highest governments responsibility?"
# words = example["tokens"]
# boxes = example["bboxes"]

encoding = processor(image, question, return_tensors="pt")
start_positions = torch.tensor([1])
end_positions = torch.tensor([3])

outputs = model(**encoding, start_positions=start_positions, end_positions=end_positions)
print(outputs)