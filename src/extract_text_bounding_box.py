import pickle
import json
from google.protobuf.json_format import MessageToJson

def getBoundingBox(response, num_sentences=1):
#with open('../test_pics/meta_729.pkl', 'rb') as f:
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
    minX= False
    minY= False
    maxX= False
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
    return(minX, minY, maxX, maxY)

#filepath = '/Users/karlsmith/PycharmProjects/typewriter-ocr-tweet/test_pics/20180224_090209.jpg'
#response = ocr_picture_from_path(filepath)
