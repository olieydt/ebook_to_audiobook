import argparse
import os
import logging
import re

from epub_extractor import convert_to_nice_path, get_parsed_book
from text_to_speech import TextToAudio, string_to_model_type


def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert an EPUB file to audiobook.")
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="Path to the input EPUB file."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Path to the output directory where the audio files will be saved.",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        required=True,
        help="Either COQUI (coqui-tts) or WHISPER (whisper) are currently accepted.",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    input_epub = args.input
    output_dir = args.output
    model_type = args.model
    if not os.path.isfile(input_epub):
        raise Exception(f"Warning: epub {input_epub} not found")

    book_title, parsed_book = get_parsed_book(input_epub)
    book_title_folder = convert_to_nice_path(book_title)
    output_path = os.path.join(output_dir, book_title_folder)
    os.makedirs(output_path, exist_ok=True)
    text_to_speech = TextToAudio(string_to_model_type(model_type))
    for i in range(len(parsed_book)):
        p = parsed_book[i]
        chapter = p["chapter"]
        content = p["content"]
        text_to_speech.convert_to_audio(chapter, content, output_path)
        logging.debug(f"converting chapter {i} of {len(parsed_book)}")
    logging.debug("Done")


if __name__ == "__main__":
    main()
