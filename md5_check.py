import hashlib
from file_name import file_name


def md5_check(file_dir):
    file_list = file_name(file_dir)
    file_list_len = len(file_list)
    print(file_list_len)
    md5_result = hashlib.md5(file_dir.encode('ascii'))
    for num in range(len(file_list)):
        md5_result.update(file_list[num].encode('ascii'))
    print(md5_result.hexdigest())
    return md5_result.hexdigest()
