from config.config import app, db
from models.apartment import Apartment
from models.building import Building
from models.lease import Lease
from models.manager import Manager
from models.payment import Payment
from models.tenant import Tenant

with app.app_context():
    print('Deleting all records')
    Apartment.query.delete()
    Building.query.delete()
    Lease.query.delete()
    Manager.query.delete()
    Payment.query.delete()
    Tenant.query.delete()

    print('Creating apartments, buildings, leases, managers, payments, and tenants')

    print('Seeding complete')
