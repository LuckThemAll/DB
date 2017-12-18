
def get_list(item):
    if not isinstance(item, list):
        item = (item, )
    return item
