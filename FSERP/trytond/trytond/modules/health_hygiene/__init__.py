from trytond.pool import Pool

from hygiene_report import *
from health_report import *
from messages import *

def register():
    Pool.register(
    PestControlTest,
    WaterControlTest,
    HealthReport,
    Messages,
    module='health_hygiene', type_ ='model'
    )
