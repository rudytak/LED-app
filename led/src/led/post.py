import requests

ip = "192.168.1.49"
port = 3000
url = "http://"+ip+":"+str(port)+"/"

def post(esp_id,mode,spd,wave,inte,hsv,c1,c2):
    r1 = c1[0]
    g1 = c1[1]
    b1 = c1[2]

    r2 = c2[0]
    g2 = c2[1]
    b2 = c2[2]

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