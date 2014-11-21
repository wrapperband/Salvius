from flask.ext.restful import marshal, request

from humanoid.joints import ArticulatedJoint


class Ankle(ArticulatedJoint):

    def __init__(self):
        super(Ankle, self).__init__()
        self.parent_id = None

        self.data["href"] = "/api/legs/" + str(self.parent_id) + "/ankle/"

    def set_parent_id(self, uuid):
        self.parent_id = uuid
        self.data["href"] = "/api/legs/" + str(uuid) + "/ankle/"

    def get(self, leg_id):
        self.data["href"] = "/api/legs/" + str(leg_id) + "/ankle/"

        return marshal(self.data, self.fields)

    def patch(self, leg_id):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201
