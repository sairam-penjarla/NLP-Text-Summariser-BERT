import pandas as pd

from summarizer import Summarizer

import warnings
warnings.filterwarnings('ignore')

class TextSummarizer:
  """
  This class performs text summarization using pre-trained models.
  """

  def __init__(self, max_length=400, min_length_text=40):
    """
    Initializes the TextSummarizer object with default parameters.

    Args:
      max_length: Maximum characters allowed in each text block (default: 400).
      min_length_text: Minimum characters required for summarization (default: 40).
    """
    self.MAX_LENGTH = max_length
    self.MIN_LENGTH_TEXT = min_length_text
    self.summarizer = Summarizer()  # Assuming Summarizer is an available library

  def summarize_text(self, text):
    """
    Summarizes a given text block using the pre-trained model.

    Args:
      text: The text block to be summarized.

    Returns:
      The summarized text.
    """
    summary = self.summarizer(text, min_length=self.MIN_LENGTH_TEXT)
    return ''.join(summary)

  def process_data(self, data_path, num_blocks=5):
    """
    Reads data from a CSV file, creates text blocks, and performs summarization.

    Args:
      data_path: Path to the CSV file containing text data.
      num_blocks: Number of text blocks to process (default: 5).
    """
    # Assuming pandas and other libraries are imported elsewhere

    DATA_COLUMNS = {'TEXT': str, 'ENV_PROBLEMS': int, 'POLLUTION': int, 'TREATMENT': int, 'CLIMATE': int, 'BIOMONITORING': int}
    warnings.filterwarnings('ignore')

    df = pd.read_csv(data_path, delimiter=';', header=0)
    df = df.astype(DATA_COLUMNS)
    df = df[:num_blocks]

    bodies = []
    i = 0
    while i < len(df):
      body = ""
      body_empty = True
      while (len(body) < self.MAX_LENGTH) and (i < len(df)):
        if body_empty:
          body = df.loc[i, 'TEXT']
          body_empty = False
        else:
          body += " " + df.loc[i, 'TEXT']
        i += 1
      bodies.append(body)

    bert_summary = []
    for body in bodies:
      bert_summary.append(self.summarize_text(body))

    print(f"\nNumber of text blocks = {len(bodies)}\n")
    print("Text blocks:\n", bodies)

    for i in range(len(bodies)):
      print("ORIGINAL TEXT:")
      print(bodies[i])
      print("\nBERT Summarizing Result:")
      print(bert_summary[i])


# Usage example
text_summarizer = TextSummarizer()
text_summarizer.process_data('water_problem_nlp_en_for_Kaggle_100.csv')

body = "Despite the similar volumes of discharged wastewater major part of pollutants comes with communal WWTPs. They bring 84% of organic pollution 86% of phosphate ions and 84% of mineral nitrogen 91% of ammonia nitrogen 87% nitrate nitrogen and 79% nitrite nitrogen. The input of the industry is between 7-21% and agriculture has the lowest impact on water bodies - 0-6%. Of the 92 urban areas only 51 localities (55%) have centralized collection of communal waste waters and their monitoring. Among the 2878 villages 6 of them (0.2%) have such a monitoring."
summary = text_summarizer.summarizer(body)
print(summary)