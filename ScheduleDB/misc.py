
def get_list(item):
    if not isinstance(item, list):
        item = (item, )
    return item


def is_correct_fields(records):
    return len(records) > 0
