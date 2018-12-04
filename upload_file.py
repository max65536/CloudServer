import requests


def upload_file(file_list):
    data = {"k1": "v1"}
    file_list_len = len(file_list)

    for num in range(file_list_len):
        filename = file_list[num]
        files = {
        "file": open("./shared_files/"+filename, "rb")
        }
        r = requests.post("http://127.0.0.1:8000/upload", data, files=files)
        print(r.text)
