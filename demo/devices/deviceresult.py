import json

class DeviceResult:
    def __init__(self, name, duration=0.0, valid = True):
        self.__name = name
        self.Duration = duration
        self.IsValid = valid
        self.__readings = []

    def add_reading(self, name, type, value):
        found = next((x for x in self.__readings if x["name"] == name), None)
        if found is None:
            self.__readings.append({
                "name": name,
                "type": type,
                "value": value
            })
        else:
            found["type"] = type
            found["value"] = value

    def to_json(self, pretty = False):
        data = {}
        for key in self.__dict__:
            newKey = key.replace("_", "").replace(self.__class__.__name__, "")
            if newKey == "readings":
                data["readings"] = self.__readings
                continue
            data[newKey] = self.__dict__[key]
        if pretty:
            return json.dumps(data, indent=4, sort_keys=True)

        return json.dumps(data, separators=(',', ':'))

    @property
    def IsValid(self):
        return self.__isvalid
 
    @IsValid.setter
    def IsValid(self, value):
        self.__isvalid = value
    
    @property
    def Duration(self):
        return self.__duration

    @Duration.setter
    def Duration(self, value):
        self.__duration = round(value,4)