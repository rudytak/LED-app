import requests
import math

ip = "192.168.1.49"
port = 3000
url = "http://"+ip+":"+str(port)+"/"

id = input("Write the esp ID: ")  # 1,2
mode = input("Mode number: ")  # 0 - 7
spd = input("Speed: ") # 1 - 100
wave = input("Number of waves: ")  # 1 +
inte = input("Intensity: ") # 0 - 100
hsv = input("HSV mode: ") # 1 - 3
c1 = input("Write your first color (r,g,b): ")  # 0 - 255
c2 = input("Write your second color (r,g,b): ")  # 0 - 255

def post(esp_id,mode,spd,wave,inte,hsv,c1,c2):
    r1 = c1.split(",")[0]
    g1 = c1.split(",")[1]
    b1 = c1.split(",")[2]

    r2 = c2.split(",")[0]
    g2 = c2.split(",")[1]
    b2 = c2.split(",")[2]

    myobj = {
        "mode": esp_id,
        "value": mode,
        "speed": spd,
        "wave": wave,
        "intensity": inte,
        "hsv": hsv,
        "col": [r1, g1, b1],
        "col1": [r2, g2, b2],
    }

    x = requests.post(url, json=myobj)

    print("Posted: " + x.text)

post(id,mode,spd,wave,inte,hsv,c1,c2)