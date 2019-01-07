from upload_file import upload_file


def file_content_check(last_md5_file_content, current_md5_file_content):
    update_list = []
    print('length is %d' % len(current_md5_file_content))
    num = 0
    while(num < len(current_md5_file_content)):
        if current_md5_file_content[num] != last_md5_file_content[num]:
            update_list.append(num)
        num = num + 1
    return update_list


def file_check(last_md5_file_content, current_md5_file_content, last_md5, current_md5,
               current_file_list, last_file_list, file_dir):

    upload_list = []
    last_md5_file_content.pop()
    print('last list is %s' % last_md5_file_content)
    print('current list is %s' % current_md5_file_content)

    if last_md5 == current_md5:
        update_list = file_content_check(last_md5_file_content, current_md5_file_content)
        print('update list is %s' % update_list) #[2]
        print('update list is %d' % len(upload_list)) #0
        num = 0
        while (num < len(update_list)):
            upload_list.append(current_file_list[update_list[num]])
            print('current update is %s' % current_file_list[update_list[num]])
            num = num + 1
        upload_list.append('md5_client01_file_content.txt')
        upload_file(upload_list)
        print('upload files are %s\r\n\r\n' % upload_list)
        print('both md5 are same')
    else:
        file_list_path = [file_dir + '/file_list.txt']
        with open(file_list_path[0], 'w') as f:
            for num in current_file_list:
                print(num, file=f)

        if len(last_file_list) == 0:
            upload_list = current_file_list
            print('There is no such client before')
            upload_list.append('md5_client01.txt')
            upload_list.append('file_list.txt')
            upload_list.append('md5_client01_file_content.txt')
            upload_file(upload_list)
        else:
            current_num = 0
            last_num = 0
            print('current %s' % current_file_list)
            print('last %s' % last_file_list)
            while current_num < len(current_file_list):
                if current_file_list[current_num] != last_file_list[last_num]:
                    upload_list.append(current_file_list[current_num])
                    current_md5_file_content.pop(current_num)
                    current_num += 1
                else:
                    current_num += 1
                    last_num += 1
            upload_list.append('md5_client01.txt')
            upload_list.append('file_list.txt')

            update_list = file_content_check(last_md5_file_content, current_md5_file_content)
            print('update is %s' % update_list)
            num = 0
            if len(update_list) > 0:
                while num < len(update_list):
                    upload_list.append(current_file_list[update_list[num]])
                    print('update11 is %s' % current_file_list[update_list[num]])
                    num = num + 1
            upload_list.append('md5_client01_file_content.txt')
            upload_file(upload_list)
            print('upload files are %s\r\n\r\n' % upload_list)



