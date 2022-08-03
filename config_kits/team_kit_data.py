from config_kits.kit import Kit

class TeamKitData:
    def __init__(self,data:bytearray):
        self.data = data
        self.GA = Kit(self.data[:88])
        self.PA = Kit(self.data[88:176])
        self.GB = Kit(self.data[176:264])
        self.PB = Kit(self.data[264:353])

    def update_data(self):
        self.data[:88] = self.GA.data
        self.data[88:176] = self.PA.data
        self.data[176:264] = self.GB.data
        self.data[264:353] = self.PB.data
