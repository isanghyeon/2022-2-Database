class responseObject:
    def __init__(self):
        self.success = {
            "status": 0,
            "message": "Success"
        }
        self.failed = {
            "status": 0,
            "message": "Failed"
        }

    def postMethodResponse(self, state=bool):
        if state is True:
            self.success["status"] = 201
            return self.success, 201

        self.failed["status"] = 400
        return self.failed, 400

    def patchMethodResponse(self, state=bool):
        if state is True:
            self.success["status"] = 200
            return self.success, 200

        self.failed["status"] = 400
        return self.failed, 400

    def deleteMethodResponse(self, state=bool):
        if state is True:
            self.success["status"] = 201
            return self.success, 201

        self.failed["status"] = 400
        return self.failed, 400
