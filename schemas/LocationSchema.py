from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema


# __tablename__ = 'locations'

# id = Column(Integer, primary_key=True)
# lat = Column(String(20), unique=False)
# lng = Column(String(20), unique=True)
# device = Column(Integer, ForeignKey("devices.id"))
# date_registered = Column(Date, default=datetime.datetime.utcnow)
class LocationSchema(ModelSchema):
    class Meta:
        # Fields to expose
        fields = ('lat', 'lng', 'date_registered')
location_schema = LocationSchema()
oficios_schema = OficioSchema(many=True)