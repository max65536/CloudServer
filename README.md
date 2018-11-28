# CloudServer
*Introduction*

Nowadays people live a information society. They have a large number of data such as working documents, personal photos and favorite musics which may saved in their different devices like laptop, tablet and mobile. It will be very convenient, if users can make their private document be synchronized. As a result, they can use only one device to read all the files saved in all their devices. When they lose their files in accident, they can easily find it back from  the server as their files have been already synchronized. What’s more, sometimes we want to share some files to our partners or friends. But transferring those files may be really troublesome when they need to be continuous uploaded.  So uploading those files synchronously to the specified directory in the server is obviously the best way to achieve the goals.

As what has been mentioned above, we would like to build a cloud file manage system just like Google Drive. The system has some features as follows:
1. User system(login, logout). Every user has an account and a file space. If they forget their password or want to change it, they can set a new one after answering a specified question, which they set before.
2. Using HTTP protocols(maybe use FTP) to transfer small files, such as jpg,  txt , mp3 files.
3. If user has several devices, his devices can synchronize files independently.
4. Users may share their files with a share link.
5. Using checksum to check if the files are synchronized.
6. Using HTML to implement GUI.
