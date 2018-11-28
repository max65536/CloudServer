import requests

#res=requests.get("http://www.runoob.com/wp-content/uploads/2013/11/2112205-861c05b2bdbc9c28.png")
#print(res)

#f=open('x.png','wb')
#f.write(res.content)


headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Connection':'Keep-Alive',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

keyword= "abc"

res2=requests.get("https://www.google.de/search",params=keyword)
print(res2)
print(res2.content)

