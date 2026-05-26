import spacy

nlp = spacy.blank("en")

doc = nlp(
    "Python FastAPI SQL Machine Learning"
)

for token in doc:

    print(token.text)