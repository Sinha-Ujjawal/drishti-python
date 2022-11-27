from typing import Iterable, List, Set, Optional
import itertools as it
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import logging
import logging.config
from config import LogConfig, DICTIONARY_PATH

DICTIONARY: Optional[Set[str]] = None

logging.config.dictConfig(LogConfig().dict())
logger = logging.getLogger(LogConfig().LOGGER_NAME)

app = FastAPI()


def init_dictionary(file_path: str) -> Set[str]:
    global logger
    ret = set()
    logger.info(f"Initializing Dictionary using file: {file_path}")
    with open(file_path, "r") as fp:
        for word in fp.readlines():
            ret.add(word.strip().lower())
    logger.info(f"Dictionary Initialized, total words: {len(ret)}")
    return ret


def generate_all_prefixes(s: str) -> Iterable[str]:
    for i in range(1, len(s) + 1):
        yield s[:i]


def generate_all_suffixes(s: str) -> Iterable[str]:
    for i in range(len(s)):
        yield s[i:]


def generate_distinct_substrings(s: str) -> Iterable[str]:
    seen_before = set()
    yield ""
    yield from (
        candidate
        for i in range(len(s))
        for j in range(i + 1, len(s) + 1)
        for candidate in [s[i:j]]
        if candidate not in seen_before
        for _ in [seen_before.add(candidate)]
    )


def generate_all_possibilities(words: List[str]) -> Iterable[str]:
    seen_before = set()
    yield from (
        candidate
        for w1, w2, w3 in it.combinations(words, 3)
        for prefix, middle, suffix in it.permutations([w1, w2, w3])
        for p in generate_all_prefixes(prefix)
        for m in generate_distinct_substrings(middle[1:-1])
        for s in generate_all_suffixes(suffix)
        for candidate in [p + m + s]
        if candidate not in seen_before
        for _ in [seen_before.add(candidate)]
    )


class WordsRequest(BaseModel):
    words: List[str]


class WordsResponse(BaseModel):
    words: List[str]


@app.post("/words")
def valid_words_handler(words: WordsRequest) -> WordsResponse:
    global DICTIONARY
    if DICTIONARY is None:
        DICTIONARY = init_dictionary(DICTIONARY_PATH)
    words_lowercased = [word.strip().lower() for word in words.words]
    valid_words = [
        word
        for word in generate_all_possibilities(words_lowercased)
        if word in DICTIONARY
    ]

    if valid_words:
        return WordsResponse(words=valid_words)
    else:
        raise HTTPException(detail="no words found", status_code=404)
