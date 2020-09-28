class BracketIndex(object):
    def __init__(self, start_index, end_index):
        self.start_index = start_index
        self.end_index = end_index

    def __str__(self):
        return '{"start_index": ' + str(self.start_index) + ', "end_index": ' + str(self.end_index) + '}'


def get_bracket_index(content: str, pre_index: int):
    if content is None or content.__len__() == 0:
        raise Exception('content is None')
    if pre_index is None:
        raise Exception('pre_index is None')
    right_count = 0
    left_count = 0
    index = 0
    start_index = None
    end_index = None
    while (right_count == 0 or right_count != left_count) and index < content.__len__():
        if content[index] == '{':
            right_count = right_count + 1
            if start_index is None:
                start_index = index
        if content[index] == '}':
            left_count = left_count + 1
            end_index = index
        index = index + 1
    if end_index is not None:
        return BracketIndex(pre_index + start_index, pre_index + end_index)
