import argparse
from enum import Enum
import io

from google.cloud import vision
from google.cloud.vision import types
import argparse
from enum import Enum
import io

from google.cloud import vision
from google.cloud.vision import types
#from PIL import Image, ImageDraw

print("program running")
pic_path = '/Users/karlsmith/PycharmProjects/typewriter-functionality/test_pics/20180224_084729.jpg'


def detect_document(path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    for page in document.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)

            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)

            block_text = ''
            for symbol in block_symbols:
                block_text = block_text + symbol.text

            print('Block Content: {}'.format(block_text))
            print('Block Bounds:\n {}'.format(block.bounding_box))


detect_document(pic_path)