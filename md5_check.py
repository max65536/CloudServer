import hashlib


def md5_check(file_list, file_dir):
    file_list_len = len(file_list)
    print('The number of files are is: %d' % file_list_len)
    md5_result = hashlib.md5(file_dir.encode('ascii'))
    for num in range(file_list_len):
        md5_result.update(file_list[num].encode('ascii'))
    print('MD5 is: %s' % (md5_result.hexdigest()))
    return md5_result.hexdigest()


def md5_file_content_check(file_list, file_dir):
    md5_file_content = []
    file_list_len = len(file_list)

    for num in range(file_list_len):        #read all files content and calculate their own md5
        with open(file_dir+'/'+file_list[num], 'rb') as f:
            content = f.read()
            md5_file_content.append(hashlib.md5(content).hexdigest())

    with open(file_dir + '/md5_client01_file_content.txt', 'w') as f:
        for num in md5_file_content:
            print(num, file=f)

    return md5_file_content
