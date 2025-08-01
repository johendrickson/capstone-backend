from app.db import db
from app.models.user_plant import userplant_tags

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    # Many-to-many backref to UserPlant
    user_plants = db.relationship(
        "UserPlant",
        secondary=userplant_tags,
        back_populates="tags"
    )

    def __init__(self, name: str):
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
