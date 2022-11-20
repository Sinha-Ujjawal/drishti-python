from typing import Iterable, List, Set, Any, Dict
import itertools as it
from dataclasses import dataclass
from flask import Flask, request
import toml

DICTIONARY: Set[str] = set()
CONFIG_PATH: str = "./config.toml"

app = Flask(__name__)


def init_dictionary(file_path: str):
    print(f"Initializing Dictionary using file: {file_path}")
    with open(file_path, "r") as fp:
        for word in fp.readlines():
            DICTIONARY.add(word.strip().lower())
    print("Dictionary Initialized, total words: {}", len(DICTIONARY))


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
    for w1, w2, w3 in it.combinations(words, 3):
        for prefix_word, middle_word, suffix_word in it.permutations([w1, w2, w3]):
            yield from (
                candidate
                for p in generate_all_prefixes(prefix_word)
                for m in generate_distinct_substrings(middle_word[1:-1])
                for s in generate_all_suffixes(suffix_word)
                for candidate in [p + m + s]
                if candidate not in seen_before
                for _ in [seen_before.add(candidate)]
            )


def with_json(handler):
    def _inner():
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            return handler(request.json)
        else:
            return "Json Required", 400

    return _inner


@app.route("/words", methods=["POST"])
@with_json
def valid_words_handler(data: Dict[str, Any]):
    words: List[str] = data.get("words", [])
    words_lowercased = [word.strip().lower() for word in words]
    valid_words = [
        word
        for word in generate_all_possibilities(words_lowercased)
        if word in DICTIONARY
    ]
    if valid_words:
        return {"words": valid_words}, 200
    else:
        return "no words found", 404


@dataclass
class Config:
    host: str
    port: int
    debug: bool
    dictionary_path: str


def load_config(config_path: str) -> Config:
    config = toml.load(config_path)
    return Config(
        host=config.get("host", "127.0.0.1"),
        port=config.get("port", 3030),
        debug=config.get("debug", False),
        dictionary_path=config.get("dictionary_path", "./words.txt"),
    )


if __name__ == "__main__":
    config = load_config(CONFIG_PATH)
    init_dictionary(config.dictionary_path)
    app.run(host=config.host, port=config.port, debug=config.debug)
