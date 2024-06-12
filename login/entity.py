import spacy
from spacy.matcher import Matcher
# Load the English model (adjust model name as needed)
nlp = spacy.load("en_core_web_sm")

def extract_entities_ner(text):
  """Extracts named entities using spaCy's pre-trained model.

  Args:
      text: The text to process for entity extraction.

  Returns:
      A list of dictionaries, where each dictionary represents an entity
      with its text, label (category), and start and end indices in the text.
  """

  doc = nlp(text)
  entities = []
  for entity in doc.ents:
    entities.append({
      "text": entity.text,
      "label": entity.label_,
      "start": entity.start_char,
      "end": entity.end_char,
    })
  return entities


# def extract_facility_name(text):
#     # Load spaCy model
#     nlp = spacy.load('en_core_web_sm')
    
#     # Add Entity Ruler
#     ruler = nlp.add_pipe("entity_ruler")
#     pattern = {
#         "label": "FACILITY",
#         "pattern": [{"LOWER": {"FUZZY": "name"}},{"LOWER": {"FUZZY": "of"}}, {"LOWER": {"FUZZY": "facility"}}]
#     }
#     ruler.add_patterns([pattern])
    
#     # Process text
#     doc = nlp(text)
    
#     # Extract the first facility name match
#     facility_name = None
#     for ent in doc.ents:
#         if ent.label_ == "FACILITY":
#             facility_name = ent.text
#             break
    
#     return facility_name

# # Example usage
def extract_facility_name(text):
    # Load spaCy model
    nlp = spacy.load('en_core_web_sm')
    
    # Initialize the Matcher with the shared vocab
    matcher = Matcher(nlp.vocab)
    
    # Define the pattern
    pattern = [
        # {"LOWER": "name"},
        # {"LOWER": "of"},
        {"LOWER": "facility"},
        {"IS_PUNCT": True, "OP": "?"},
        {"IS_ALPHA": True, "OP": "+"}
    ]
    
    matcher.add("FACILITY_NAME", [pattern])
    
    # Process the text
    doc = nlp(text)
    
    # Find matches
    matches = matcher(doc)
    
    # Extract the first match if available
    facility_name = None
    if matches:
        match_id, start, end = matches[0]
        facility_name = doc[start:end].text.strip()  # Extract and strip matched text

    return facility_name
        # span = doc[start:end]
        # facility_name = span.text
        # # facility_name = span.text.split(':')[-1].strip()  # Extract text after the colon
    


# pattern = [{"LOWER": "owner", "FUZZY": True}]  # Create a list containing the pattern dictionary
                    # print(pattern)
                    # matcher = Matcher(nlp.vocab)
                    # matcher.add("ExamplePattern", pattern)  # Add the pattern list

                    # matches = matcher(doc)
                    # for match_id, start, end, ratio in matches:
                    #     span = doc[start:end]
                    #     print(f"Match found: {span.text}, Ratio: {ratio}")
                                        