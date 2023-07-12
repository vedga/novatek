class NovatekRegistry:
    devices = {}

    def Add(self, name, device):
        if not name in self.devices:
            self.devices[str(name)] = device

    def Get(self, name):
        return self.devices.get(str(name))
