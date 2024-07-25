from config import app, api
from models.admin import Admin
from routes.index import Index, Favicon
from routes.apartments import Apartments, ApartmentByID
from routes.buildings import Buildings, BuildingByID
from routes.leases import Leases,LeaseByID
from routes.managers import Managers, ManagerByID
from routes.payments import Payments, PaymentByID
from routes.tenants import Tenants, TenantByID

# Routes
api.add_resource(Index, '/')
api.add_resource(Favicon, '/favicon.ico')
api.add_resource(Apartments, "/apartments")
api.add_resource(ApartmentByID, '/apartments/<int:id>')
api.add_resource(Buildings, '/buildings')
api.add_resource(BuildingByID, '/buildings/<int:id>')
api.add_resource(Leases, '/leases')
api.add_resource(LeaseByID, '/leases/<int:id>')
api.add_resource(Managers, '/managers')
api.add_resource(ManagerByID, '/managers/<int:id>')
api.add_resource(Payments, '/payments')
api.add_resource(PaymentByID, '/payments/<int:id>')
api.add_resource(Tenants, '/tenants')
api.add_resource(TenantByID, '/tenants/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)

