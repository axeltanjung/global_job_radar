import re

DATA_REGEX = re.compile(
    r"data\s(scientist|engineer|analyst)|machine\slearning|ml\sengineer|analytics|business\sintelligence",
    re.I
)

def is_data_role(title):
    return bool(DATA_REGEX.search(title or ""))
