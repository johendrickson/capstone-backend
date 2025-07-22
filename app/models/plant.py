from app.db import db

class Plant(db.Model):
    __tablename__ = "plants"

    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.Text, nullable=False)
    scientific_name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=True)
    preferred_soil_conditions = db.Column(db.Text, nullable=True)
    propagation_methods = db.Column(db.Text, nullable=True)
    edible_parts = db.Column(db.Text, nullable=True)
    is_plant_safe = db.Column(db.Boolean, nullable=True)

    user_plants = db.relationship("UserPlant", back_populates="plant", cascade="all, delete-orphan")

    def __init__(self, common_name, scientific_name, species=None, preferred_soil_conditions=None, propagation_methods=None, edible_parts=None, is_plant_safe=None):
        self.common_name = common_name
        self.scientific_name = scientific_name
        self.species = species
        self.preferred_soil_conditions = preferred_soil_conditions
        self.propagation_methods = propagation_methods
        self.edible_parts = edible_parts
        self.is_plant_safe = is_plant_safe

    def to_dict(self):
        return {
            "id": self.id,
            "common_name": self.common_name,
            "scientific_name": self.scientific_name,
            "species": self.species,
            "preferred_soil_conditions": self.preferred_soil_conditions,
            "propagation_methods": self.propagation_methods,
            "edible_parts": self.edible_parts,
            "is_plant_safe": self.is_plant_safe,
        }
