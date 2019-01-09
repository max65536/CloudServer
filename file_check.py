def file_content_check(last_md5_file_content, current_md5_file_content, current_file_list):
    update_list = []
    print('length is %d' % len(current_md5_file_content))
    num = 0
    while(num < len(current_md5_file_content)):
        if current_md5_file_content[num] != last_md5_file_content[num]:
            update_list.append(current_file_list[num])
        num = num + 1
    return update_list


def file_check(last_md5_file_content, current_md5_file_content, last_md5, current_md5,
               current_file_list, last_file_list, file_dir):

    last_md5_file_content.pop()
    print('last list is %s' % last_md5_file_content)
    print('current list is %s' % current_md5_file_content)
    update_list = []

    if last_md5 == current_md5:
        update_list = file_content_check(last_md5_file_content, current_md5_file_content, current_file_list)
        print('update list is %s' % update_list) #[2]
        print('update list is %d' % len(update_list)) #0
        print('both name md5 are same')
    else:
        file_list_path = [file_dir + '/file_list.txt']
        with open(file_list_path[0], 'w') as f:
            for num in current_file_list:
                print(num, file=f)

        if len(last_file_list) == 0:
            update_list = current_file_list
            print('There is no such client before')
        else:
            current_num = 0
            last_num = 0
            print('current file list %s' % current_file_list)
            print('last file list%s' % last_file_list)
            while current_num < len(current_file_list):
                if current_file_list[current_num] != last_file_list[last_num]:
                    update_list.append(current_file_list[current_num])
                    current_md5_file_content.pop(current_num)
                    current_num += 1
                else:
                    current_num += 1
                    last_num += 1

            content_update_list = file_content_check(last_md5_file_content, current_md5_file_content, current_file_list)
            print('content update is %s' % content_update_list)
            num = 0
            if len(update_list) > 0:
                while num < len(content_update_list):
                    update_list.append(content_update_list[num])
                    num = num + 1
            print('update files are %s\r\n\r\n' % update_list)
    return update_list


