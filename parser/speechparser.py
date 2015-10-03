__author__ = 'Jake'

from metamind.api import ClassificationModel, set_api_key
from assets import apikey
import json

set_api_key(apikey)
ClassificationModel(id=155).predict("your text", input_type="text")


def parsestring(alexa):
    sentiment = ClassificationModel(id=155).predict(alexa, input_type="text")
    jsonres = json.loads(json.dumps(sentiment[0]))
    mood = jsonres['label'].lower()

    return mood

def overall_sentiment(alexa):
    totalsentiment = 0
    for sentence in alexa.split("."):
        mood = parsestring(sentence)
        if mood == "positive":
            totalsentiment = totalsentiment + 1
        elif mood == "negative":
            totalsentiment = totalsentiment - 1

    return totalsentiment


def get_grades_sentiment(alexa):

    grade_triggers = set(["grade", "grades", "failed", "passed", "test", "homework", "bombed", "did terrible"])
    thesentence = [x for x in alexa.split(".") if any(words in x for words in grade_triggers)]
    for each in thesentence:
        mood = parsestring(each)
        if mood == "positive":
            return 1
        if mood == "negative":
            return -1
    else:
        return 0


def get_participation_sentiment(alexa):
    participation_triggers = set(["event", "foundation", "lebron", "akron", "university"])
    thesentence = [x for x in alexa.split(".") if any(words in x for words in participation_triggers)]
    for each in thesentence:
        mood = parsestring(each)
        if mood == "positive":
            return 1
        if mood == "negative":
            return -1
    else:
        return 0


def get_attendance_sentiment(alexa):
    attendance_triggers = set(["didn't go", "went to school", "skipped", "attended"])
    thesentence = [x for x in alexa.split(".") if any(words in x for words in attendance_triggers)]
    for each in thesentence:
        mood = parsestring(each)
        if mood == "positive":
            return 1
        if mood == "negative":
            return -1
    else:
        return 0