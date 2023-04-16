import os

from openpyxl import Workbook
from openpyxl.styles import Font

import nlp

DIRECTORY = "scrapedfiles/"
OUTPUT_FILE = "output.xlsx"


def workbook_write(sheet, url_id, text):
    """Write the data to the workbook."""
    positive_score = nlp.positive_score(text)
    negative_score = nlp.negative_score(text)
    polarity_score = nlp.polarity_score()
    subjectivity_score = nlp.subjectivity_score()
    avg_sentence_length = nlp.avg_sentence_length_and_avg_words(text)
    avg_words = nlp.avg_sentence_length_and_avg_words(text)
    avg_word_length = nlp.avg_word_length(text)
    calculate_fog_index = nlp.calculate_fog_index(text)
    complex_words = nlp.complex_words(text)
    word_count = nlp.word_count(text)
    syllables = nlp.syllables(text)
    personal_pronoun_count = nlp.personal_pronoun_count(text)

    row = [
        url_id,
        positive_score,
        negative_score,
        polarity_score,
        subjectivity_score,
        avg_sentence_length,
        avg_words,
        avg_word_length,
        calculate_fog_index,
        complex_words,
        word_count,
        syllables,
        personal_pronoun_count,
    ]
    sheet.append(row)


def process_file(filename, sheet):
    """Process a single input file."""
    url_id = os.path.splitext(filename)[0]
    filepath = os.path.join(DIRECTORY, filename)
    with open(filepath, "r", encoding="ISO-8859-1") as file:
        text = file.read()
        try:
            workbook_write(sheet, url_id, text)
        except Exception as exception:
            print(f"Error processing file {filename}: {exception}")
            raise


def sort_key(filename):
    """Return the numeric value of the filename."""
    try:
        return int(os.path.splitext(filename)[0])
    except ValueError:
        return 0


def main():
    """Process all files in the input directory."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Sheet1"

    sheet.append(
        [
            "URL_ID",
            "POSITIVE SCORE",
            "NEGATIVE SCORE",
            "POLARITY SCORE",
            "SUBJECTIVITY SCORE",
            "AVERAGE SENTENCE LENGTH",
            "AVERAGE NUMBER OF WORDS PER SENTENCE",
            "AVERAGE WORD LENGTH",
            "FOG INDEX",
            "PERCENTAGE OF COMPLEX WORDS",
            "WORD COUNT",
            "SYLLABLE PER WORD",
            "PERSONAL PRONOUN COUNT",
        ]
    )
    sheet["A1"].font = Font(bold=True)
    sheet["B1"].font = Font(bold=True)
    sheet["C1"].font = Font(bold=True)
    sheet["D1"].font = Font(bold=True)
    sheet["E1"].font = Font(bold=True)
    sheet["F1"].font = Font(bold=True)
    sheet["G1"].font = Font(bold=True)
    sheet["H1"].font = Font(bold=True)
    sheet["I1"].font = Font(bold=True)
    sheet["J1"].font = Font(bold=True)
    sheet["K1"].font = Font(bold=True)
    sheet["L1"].font = Font(bold=True)
    sheet["M1"].font = Font(bold=True)

    entries = os.listdir(DIRECTORY)
    entries = sorted(
        entries, key=sort_key
    )  # sort filenames in ascending order based on numeric value
    for filename in entries:
        print(f"Processing file {filename}")
        process_file(filename, sheet)

    workbook.save(OUTPUT_FILE)
    workbook.close()


if __name__ == "__main__":
    main()
