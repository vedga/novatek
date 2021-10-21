import requests
import hashlib

class NovatekElectro:
    models = {
        243 : "EM-125",
        293 : "EM-126T",
        255 : "EM-125S",
        285 : "EM-126TS",
        271 : "EM-129"
    }

    def __init__(self,ip,password):
        self._url = 'http://'+ip
        self._password = password

        self.Connect()

    def Connect(self):
        r = requests.get(self._url+'/api/login?device_info').json()
        if "OK" != r["STATUS"]:
            raise ConnectionAbortedError

        prefix = self.models.get(r["device_id"])

        r = requests.get(self._url+'/api/login?salt').json()
        if "OK" != r["STATUS"]:
            raise ConnectionAbortedError

        sha_1 = hashlib.sha1()
        sha_1.update(str(prefix+self._password+r["SALT"]).encode('utf-8'))
        r = requests.get(self._url+'/api/login?login='+sha_1.hexdigest()).json()
        if "OK" != r["STATUS"]:
            raise ConnectionAbortedError

        self._endpoint = self._url + '/' + r["SID"]

    def Voltage(self):
        r = requests.get(self._endpoint+'/api/all/get?volt_msr').json()
        if "OK" != r["STATUS"]:
            raise ConnectionAbortedError
        return float(r["volt_msr"])/10

    def Current(self):
        r = requests.get(self._endpoint+'/api/all/get?cur_msr').json()
        if "OK" != r["STATUS"]:
            raise ConnectionAbortedError
        return float(r["cur_msr"])/100

    def Frequency(self):
        r = requests.get(self._endpoint+'/api/all/get?freq_msr').json()
        if "OK" != r["STATUS"]:
            raise ConnectionAbortedError
        return float(r["freq_msr"])/100

    def ActivePower(self):
        r = requests.get(self._endpoint+'/api/all/get?powa_msr').json()
        if "OK" != r["STATUS"]:
            raise ConnectionAbortedError
        return float(r["powa_msr"])

    def FullPower(self):
        r = requests.get(self._endpoint+'/api/all/get?pows_msr').json()
        if "OK" != r["STATUS"]:
            raise ConnectionAbortedError
        return float(r["pows_msr"])

    def ActiveEnergy(self):
        r = requests.get(self._endpoint+'/api/all/get?enrga_msr').json()
        if "OK" != r["STATUS"]:
            raise ConnectionAbortedError
        return float(r["enrga_msr"])

    def FullEnergy(self):
        r = requests.get(self._endpoint+'/api/all/get?enrgs_msr').json()
        if "OK" != r["STATUS"]:
            raise ConnectionAbortedError
        return float(r["enrgs_msr"])
