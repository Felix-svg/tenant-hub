
from config import app
from models.apartment import Apartment
from models.building import Building
from models.lease import Lease
from models.payment import Payment
from models.manager import Manager
from models.tenant import Tenant

if __name__ == '__main__':
    app.run(debug=True)

