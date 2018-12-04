import hashlib


def md5_check(file_list, file_dir):
    file_list_len = len(file_list)
    print('The number of files are is: %d' % file_list_len)
    md5_result = hashlib.md5(file_dir.encode('ascii'))
    for num in range(file_list_len):
        md5_result.update(file_list[num].encode('ascii'))
    print('MD5 is: %s' % (md5_result.hexdigest()))
    return md5_result.hexdigest()
