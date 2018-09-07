import io
import os
from google.cloud import vision
from google.cloud.vision import types
from textblob import TextBlob
import json
from google.protobuf.json_format import MessageToJson
from utils import time_it
from tweet import max_tweet_length

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../auth/image-annotation-5ce604dffdbc.json"
FLAG_DO_SPELLCHECK = False
period = '.'
x_margin = 10  # px
y_margin = 10  # px



@time_it
def ocr_picture_from_path(path):
    """
    Detects document features in an image.
    :param path: str - the location of the picture to send
    :returns: str - the text value of the raw api response
    """
    print("calling GCV API")
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)

    return response


def interpretResponse(full_text, num_sentences=1):
    """
    Extracts the last [num_sentences] sentences in full_text
    :param full_text: str - the text to pull sentences from
    :param num_sentences: int - the number of sentences
    :returns: text if successful or False if a tweet can't be extracted
    """

    full_text = full_text.full_text_annotation.text

    if (FLAG_DO_SPELLCHECK):
        full_text_blob = TextBlob(full_text)
        full_text_blob = full_text_blob.correct()
        full_text = str(full_text_blob)

    periods = [pos for pos, char in enumerate(full_text) if char == '.' or char==","]
    if len(periods) < num_sentences+1:
        if len(full_text) > max_tweet_length:
            return False
        return full_text

    #  negative index, skipping first period, going back as many periods as requested sentences
    startpos = periods[(-1)-num_sentences] + 1

    if full_text[startpos] == " ":
        startpos+=1

    return full_text[startpos:]

def getBoundingBox(response, num_sentences=1):
    """
    gets the coordinates of the box that bounds the text to tweet
    :param response: textAnnotation - the textAnnotation object to pull sentences from
    :param num_sentences: int - the number of sentences in the tweet
    :returns: the tuple (minX, maxX, minY, maxY) of the bounding box
    """
    response = response.full_text_annotation
    currentSentence = 0
    serialized = MessageToJson(response)
    jsonDoc = json.loads(serialized)

    stop = False
    minX = False
    minY = False
    maxX = False
    maxY = False

    for page in reversed(jsonDoc['pages']):
        for block in reversed(page['blocks']):
            block_words = []
            for paragraph in reversed(block['paragraphs']):
                block_words.extend(reversed(paragraph['words']))

            block_symbols = []
            for word in block_words:
                block_symbols.extend(reversed(word['symbols']))

            block_text = ''
            block_text = block_text + block_symbols[0]['text']
            boundingBoxVertices = block_symbols[0]['boundingBox']['vertices']
            if stop == False:
                if minX == False:
                    minX = boundingBoxVertices[0]['x']
                    maxX = boundingBoxVertices[0]['x']
                    minY = boundingBoxVertices[0]['y']
                    maxY = boundingBoxVertices[0]['y']
                for coord in boundingBoxVertices[1:]:
                    if coord['x'] > maxX:
                        maxX = coord['x']
                    if coord['y'] > maxY:
                        maxY = coord['y']
                    if coord['x'] < minX:
                        minX = coord['x']
                    if coord['y'] < minY:
                        minY = coord['y']

            for symbol in block_symbols[1:]:
                if symbol['text'] == '.':
                    currentSentence += 1
                    if currentSentence == num_sentences:
                        stop = True
                else:
                    if stop == False:
                        boundingBoxVertices = symbol['boundingBox']['vertices']
                        for coord in boundingBoxVertices[1:]:
                            if coord['x'] > maxX:
                                maxX = coord['x']
                            if coord['y'] > maxY:
                                maxY = coord['y']
                            if coord['x'] < minX:
                                minX = coord['x']
                            if coord['y'] < minY:
                                minY = coord['y']
                        block_text = block_text + symbol['text']
    return(minX - x_margin, minY - y_margin, maxX + x_margin, maxY + y_margin)


# Test:
# print(interpretResponse("Breed cats as big as elephants and elephants as big as cats. Rebuild the Berlin wall. Break California into 3 separate states.",3))
