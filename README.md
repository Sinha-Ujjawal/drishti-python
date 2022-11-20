## Flask API ([Drishti Hackerearth Backend Nov - 2022](https://assessment.hackerearth.com/challenges/new/hiring/drishti-backend-engineer-hiring-challenge/))

Flask API to return list of valid words that can be formed using given at-most 5 words.

### Prerequisites

Using [python>=3.7.6](https://www.python.org/downloads/release/python-376/)

### Getting Started

1. Install Requirements

```console
python -m pip install -r requirements.txt
```

2. Run `run.py` to start the server at port `3030`

```console
python run.py
```

3. Then hit the endpoint `/words` as `POST` request, given `json` data as below-

```json
{ "words": ["some-word", "some-other-word"] }
```

4. You can change the default configuration by changing [config.toml](./config.toml) to your needs

### References

[words.txt](./words.txt) taken from [MIT Word List](https://www.mit.edu/~ecprice/wordlist.10000)

### Copyrights

Licensed under [@MIT](./LICENSE)
