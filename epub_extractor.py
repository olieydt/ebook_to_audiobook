import logging
from ebooklib import epub
from bs4 import BeautifulSoup
import re
from typing import List, Dict
from urllib.parse import urlparse


def convert_to_nice_path(s: str) -> str:
    return re.sub(r"['\\\/\- `\n’:]+", "_", s)


def load_epub(file_path):
    try:
        book = epub.read_epub(file_path)
        print(f"Successfully loaded '{file_path}'")
        return book
    except Exception as e:
        print(f"Error loading EPUB file: {e}")
        return None


def get_toc(book: epub.EpubBook):
    chapters = []

    for item in book.toc:
        if isinstance(item, epub.Link):
            # Simple chapter
            chapters.append({"title": item.title, "href": item.href})
        elif isinstance(item, tuple) and isinstance(item[0], epub.Section):
            # Section with possible subsections
            chapters.append({"title": item[0].title, "href": item[0].href})
            chapters.extend(extract_section(item[1]))
    return chapters


def extract_section(sections):
    chapters = []

    for sub_item in sections:
        if isinstance(sub_item, epub.Link):
            chapters.append({"title": sub_item.title, "href": sub_item.href})
        elif isinstance(sub_item, tuple) and isinstance(sub_item[0], epub.Section):
            chapters.append({"title": sub_item[0].title, "href": sub_item[0].href})
            chapters.extend(extract_section(sub_item[1]))
    return chapters


def extract_chapter_content(book: epub.EpubBook, href: str):
    try:
        # Get the document by href
        doc = book.get_item_with_href(urlparse(href).path)
        if doc is None:
            print(f"Document not found: {href}")
            return ""

        # Parse the HTML content
        soup = BeautifulSoup(doc.get_content(), "html.parser")

        # Remove scripts, styles, and other unwanted elements
        for tag in soup(["script", "style", "nav"]):
            tag.decompose()

        # Get text and clean it
        text = soup.get_text(separator="\n")
        text = clean_text(text)
        return text
    except Exception as e:
        print(f"Error extracting content from {href}: {e}")
        return ""


def clean_text(text):
    # Normalize line endings to '\n'
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    def replacer(match):
        matched_text = match.group()
        if len(matched_text) >= 2:
            return "\n"
        else:
            return " "

    return re.sub(r"\n+", replacer, text)


def get_parsed_book(epub_path) -> tuple[str, List[Dict[str, str]]]:
    book = load_epub(epub_path)
    if not book:
        raise Exception("could not parse book")

    chapters = get_toc(book)
    logging.debug(f"Found {len(chapters)} chapters/sections.")

    parsed_book = []
    for _, chapter in enumerate(chapters, 1):
        title = chapter["title"]
        href = chapter["href"]
        content = extract_chapter_content(book, href)
        if len(content.replace("\n", "")) < 1:
            continue
        parsed_book.append({"chapter": title, "content": content})
    return book.title, parsed_book
