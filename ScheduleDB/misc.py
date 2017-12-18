
def get_list(item):
    if not isinstance(item, list):
        item = (item, )
    return item


def is_correct_fields(records):
    for item in records:
        if not item:
            return False
    return len(records) > 0
