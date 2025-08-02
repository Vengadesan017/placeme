

from django.db.models import Q
from pyparsing import infixNotation, opAssoc, Word, alphanums, CaselessKeyword, ParserElement
"""
For keyword search in using logical operator ( AND, OR, NOT, () )
"""
# Set default whitespace characters
ParserElement.setDefaultWhitespaceChars(' \t')

# Define grammar
AND = CaselessKeyword("and")
OR = CaselessKeyword("or")
NOT = CaselessKeyword("not")
word = Word(alphanums + "-_+.#")
bool_expr = infixNotation(word, [
    (NOT, 1, opAssoc.RIGHT),
    (AND, 2, opAssoc.LEFT),
    (OR, 2, opAssoc.LEFT),
])

def parse_to_q(parsed):
    if isinstance(parsed, str):
        return (
            Q(professional_summary__icontains=parsed) |
            Q(skill__icontains=parsed) |
            Q(resume_text__icontains=parsed)
        )

    if len(parsed) == 1:
        return parse_to_q(parsed[0])

    if parsed[0] == "not":
        return ~parse_to_q(parsed[1])

    # Binary operators
    left = parse_to_q(parsed[0])
    for op, right in zip(parsed[1::2], parsed[2::2]):
        if op.lower() == "and":
            left = left & parse_to_q(right)
        elif op.lower() == "or":
            left = left | parse_to_q(right)
    return left

def build_candidate_query(search_text: str):
    try:
        parsed = bool_expr.parseString(search_text, parseAll=True)
        return parse_to_q(parsed[0])
    except Exception as e:
        print(f"[Boolean Parser Error] {e}")
        return Q()  # Return empty filter on parse failure
