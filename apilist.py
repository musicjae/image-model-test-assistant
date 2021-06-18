import requests


def loadapi(imgpath,port):

  with open(imgpath, "rb") as image:
    f = image.read()

  if port == 30009:
    data = {"file":f}
    response = requests.post(f'http://175.106.96.83:{str(port)}/animal-classification/predict', files=data)
    print(list(eval(str(response.text).encode().decode('UTF-8')).values())[0])
    return list(eval(str(response.text).encode().decode('UTF-8')).values())[0]

  elif port == 30010:
    data = {"file":f}
    response = requests.post(f'http://175.106.96.83:{str(port)}/plant-classification/predict', files=data)
    print(list(eval(str(response.text).encode().decode('UTF-8')).values())[0])
    return list(eval(str(response.text).encode().decode('UTF-8')).values())[0]

  elif port == 30015:
    data = {"file":f}
    response = requests.post(f'http://175.106.96.83:{str(port)}/dogclf/predict', files=data)
    print(list(eval(str(response.text).encode().decode('UTF-8')).values())[0])
    return list(eval(str(response.text).encode().decode('UTF-8')).values())[0]

  elif port == 30016:
    data = {"file":f}
    response = requests.post(f'http://175.106.96.83:{str(port)}/catclf/predict', files=data)
    print(list(eval(str(response.text).encode().decode('UTF-8')).values())[0])
    return list(eval(str(response.text).encode().decode('UTF-8')).values())[0]

  elif port == 30017:
    data = {"file":f}
    response = requests.post(f'http://175.106.96.83:{str(port)}/animal-plant-classification/predict', files=data)
    print(list(eval(str(response.text).encode().decode('UTF-8')).values())[0])
    return list(eval(str(response.text).encode().decode('UTF-8')).values())[0]

  elif port == 30018:
    data = {"file":f}
    response = requests.post(f'http://175.106.96.83:{str(port)}/dogornot/predict', files=data)
    print(list(eval(str(response.text).encode().decode('UTF-8')).values())[0])
    return list(eval(str(response.text).encode().decode('UTF-8')).values())[0]