"""A library for parsing words from the raw text file."""
import json


def main():
    with open("./data/ielts/raw.txt", "r", encoding="utf-8") as f:
        raw_txt = f.readlines()

    i = 0
    results = []

    for line in raw_txt:
        if len(line) < 2:
            # Skip empty line.
            continue

        if "Word List" in line:
            if i > 0:
                with open(f"./data/ielts/word-list-{i}.json", "w") as f:
                    f.write(json.dumps(results, ensure_ascii=False))

            i += 1
            results.clear()

            continue

        if not any(c in line for c in ("/", "[", "]", "{", "}")):
            # Skip phrases.
            continue

        result = {"word": "", "ipa": "", "explain": [{"cn": ""}]}
        state = 0
        for c in line:

            if (state == 0 or state == 1) and (c in ("/", "[", "]", "{", "}")):
                if state == 0:
                    state = 1
                else:
                    state = 3

            if state == 0:
                if c != " ":
                    result["word"] += c

            if state == 2:
                result["explain"][0]["cn"] += c

            if state == 1 or state == 3:
                result["ipa"] += c

                if state == 3:
                    state = 2

        result["word"] = result["word"].replace("*", "")
        result["explain"][0]["cn"] = result["explain"][0]["cn"].strip()

        results.append(result)

    # Dump the last one.
    with open(f"./data/ielts/word-list-{i}.json", "w") as f:
        f.write(json.dumps(results, ensure_ascii=False))

    # return 12


if __name__ == "__main__":
    main()
