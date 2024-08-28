import re
from typing import List


def tokenize(text: str) -> List[str]:
    return re.findall(r'\S+|\s+|[^\w\s]', text)


def levenshtein_distance(s1: List[str], s2: List[str]) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def calculate_word_error_rate(reference: str, hypothesis: str) -> float:
    ref_tokens = tokenize(reference)
    hyp_tokens = tokenize(hypothesis)
    
    distance = levenshtein_distance(ref_tokens, hyp_tokens)
    return distance / len(ref_tokens) if ref_tokens else 0