import pickle
import json


class Config:
    def __init__(self):
        self.weight_mutation_chance = 0.05
        self.new_node_mutation_chance = 0.05
        self.new_link_mutation_chance = 0.08

        self.C1 = 1
        self.C2 = 1
        self.C3 = 1

        self.speciation_threshold = 4

    def import_from_json(self, filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.deserialize(data)

    def deserialize(self, data: dict):
        self.weight_mutation_chance = data["weight_mutation_chance"]
        self.new_node_mutation_chance = data["new_node_mutation_chance"]
        self.new_link_mutation_chance = data["new_link_mutation_chance"]
        self.speciation_threshold = data["speciation_threshold"]
        self.C1 = data["C1"]
        self.C2 = data["C2"]
        self.C3 = data["C3"]

    def import_from_pickle(self, filename: str):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            self.deserialize(data)

    def export_to_json(self, filename: str):
        data = self.serialize()

        with open(filename, 'w') as f:
            json.dump(data, f)

        return json.dumps(data)

    def export_to_pickle(self, filename: str):
        data = self.serialize()

        with open(filename, 'wb') as f:
            pickle.dump(data, f)

        return data

    def serialize(self):
        data = {
            "weight_mutation_chance": self.weight_mutation_chance,
            "new_node_mutation_chance": self.new_node_mutation_chance,
            "new_link_mutation_chance": self.new_link_mutation_chance,
            "speciation_threshold": self.speciation_threshold,
            "C1": self.C1,
            "C2": self.C2,
            "C3": self.C3
        }
        return data
