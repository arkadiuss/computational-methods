def read_file(file_name):
    with open(file_name, 'r') as f:
        res = f.read()
    return res


def write_to_file(file_name, content):
    with open(file_name, 'w') as f:
        f.write(content)