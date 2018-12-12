import requests

data = {"name" : "user5"}
filename='robot.png'
files = {
  "file" : open("./ClientFiles/"+filename, "rb")
}
# r = requests.post("http://127.0.0.1:8000/upload", data, files=files)

# r = requests.get('https://www.google.com')
print(r.text)
