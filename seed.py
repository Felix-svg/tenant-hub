from datetime import date
from config import app, db
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
    manager = Manager(name='John Doe', email='manager@tenanthub.com', phone_number='0712345658')
    manager.set_password('Manager')
    db.session.add(manager)
    db.session.commit()
    building = Building(name='Building 101', address='Kamiti Rd')
    db.session.add(building)
    db.session.commit()
    apartment = Apartment(number='one', building_id=building.id, rent_amount=200000, manager_id=manager.id)
    db.session.add(apartment)
    db.session.commit()
    tenant = Tenant(name='Jane Doe', email='tenant@tenanthub.com', phone_number='0712345678', apartment_id=apartment.id, manager_id=manager.id)
    tenant.set_password('Tenant')
    db.session.add(tenant)
    db.session.commit()
    lease = Lease(tenant_id=tenant.id, apartment_id=apartment.id, start_date=date(2023, 7, 25),
                  end_date=date(2024, 1, 1))
    db.session.add(lease)
    db.session.commit()
    payment = Payment(lease_id=lease.id, amount=20000, payment_date=date(2024, 8, 10))
    db.session.add(payment)
    db.session.commit()

    print('Seeding complete')
