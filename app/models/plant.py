from app.db import db

class Plant(db.Model):
    __tablename__ = "plants"

    id = db.Column(db.Integer, primary_key=True)
    scientific_name = db.Column(db.Text, nullable=False)
    common_name = db.Column(db.Text, nullable=True)
    species = db.Column(db.Text, nullable=True)
    preferred_soil_conditions = db.Column(db.Text, nullable=True)
    propagation_methods = db.Column(db.Text, nullable=True)
    edible_parts = db.Column(db.Text, nullable=True)
    is_pet_safe = db.Column(db.Boolean, nullable=True)
    image_url = db.Column(db.Text, nullable=True)

    user_plants = db.relationship("UserPlant", back_populates="plant", cascade="all, delete-orphan")

    def __init__(
        self,
        scientific_name,
        common_name=None,
        species=None,
        preferred_soil_conditions=None,
        propagation_methods=None,
        edible_parts=None,
        is_pet_safe=None,
        image_url=None
    ):
        self.scientific_name = scientific_name
        self.common_name = common_name
        self.species = species
        self.preferred_soil_conditions = preferred_soil_conditions
        self.propagation_methods = propagation_methods
        self.edible_parts = edible_parts
        self.is_pet_safe = is_pet_safe
        self.image_url = image_url

    def to_dict(self):
        return {
            "id": self.id,
            "scientific_name": self.scientific_name,
            "common_name": self.common_name,
            "species": self.species,
            "preferred_soil_conditions": self.preferred_soil_conditions,
            "propagation_methods": self.propagation_methods,
            "edible_parts": self.edible_parts,
            "is_pet_safe": self.is_pet_safe,
            "image_url": self.image_url,
        }
