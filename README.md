# 🚗 Car Rental API - 1Now.io Case Study

A comprehensive Django REST API backend for Lahore Car Rental, built as a case study for 1Now.io. This project demonstrates building a production-ready car rental management system with modern Django practices.

## 📋 Project Overview

**Company**: 1Now.io - Software for independent car rental companies  
**Target**: Backend API for LahoreCarRental.com  
**Tech Stack**: Django + Django REST Framework + JWT Authentication

### What 1Now Does
1Now.io builds specialized software solutions for independent car rental companies, enabling small to medium operators to digitize their operations. They provide:
- **Online booking systems** with real-time availability
- **Fleet management** with vehicle tracking
- **Rental agreement management** with digital contracts
- **Calendar & scheduling** with conflict prevention
- **Payment processing** with deposit handling

### Who It Serves
- **Primary**: Independent car rental companies
- **Example**: LahoreCarRental.com (small operator running their fleet)
- **Size**: Small to medium-sized car rental businesses
- **Location**: Global, with focus on local/regional operators

### How This Backend Connects to Frontend
This API serves as the backend for LahoreCarRental.com's frontend, providing:
- **RESTful endpoints** for all car rental operations
- **JWT authentication** for secure user sessions
- **Real-time data** for vehicle availability and bookings
- **Payment integration** for deposits and full payments
- **Scalable architecture** to support business growth

## 🚀 Features

### ✅ Core Features
- **User Authentication**: JWT-based registration, login, and profile management
- **Vehicle Management**: CRUD operations for fleet management with ownership validation
- **Booking System**: Complete booking lifecycle with overlap prevention
- **Payment Processing**: Mock Stripe integration for deposits and payments
- **Advanced Filtering**: Search and filter capabilities for vehicles and bookings

### ✅ Advanced Features (Bonus)
- **Booking Overlap Prevention**: Prevents double-booking of vehicles
- **Mock Stripe Integration**: Simulates payment processing with 95% success rate
- **Custom Validators**: Comprehensive input validation and error handling
- **Query Filters**: Advanced filtering for bookings by date, status, etc.
- **User Permissions**: Scoped access control for all operations

## 🛠 Technology Stack

- **Backend**: Django 4.2.7 + Django REST Framework 3.14.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **API Documentation**: Swagger/OpenAPI (drf-yasg)
- **Testing**: pytest + pytest-django
- **Code Quality**: Black, flake8, isort
- **Image Processing**: Pillow

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CarRental
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the API**
   - API Base URL: `http://localhost:8000/api/v1/`
   - Admin Interface: `http://localhost:8000/admin/`
   - API Documentation: `http://localhost:8000/swagger/`

## 📚 API Endpoints

### Authentication
- `POST /api/v1/register/` - User registration
- `POST /api/v1/login/` - User login
- `POST /api/v1/logout/` - User logout
- `GET /api/v1/profile/` - Get user profile
- `PUT /api/v1/profile/` - Update user profile
- `POST /api/v1/change-password/` - Change password
- `POST /api/v1/refresh-token/` - Refresh JWT token

### Vehicle Management
- `GET /api/v1/vehicles/` - List user's vehicles
- `POST /api/v1/vehicles/` - Create new vehicle
- `GET /api/v1/vehicles/{id}/` - Get vehicle details
- `PUT /api/v1/vehicles/{id}/` - Update vehicle
- `DELETE /api/v1/vehicles/{id}/` - Delete vehicle
- `GET /api/v1/vehicles/search/` - Search available vehicles

### Booking Management
- `GET /api/v1/bookings/` - List user's bookings
- `POST /api/v1/bookings/` - Create new booking
- `GET /api/v1/bookings/{id}/` - Get booking details
- `PUT /api/v1/bookings/{id}/` - Update booking
- `POST /api/v1/bookings/{id}/confirm/` - Confirm booking
- `POST /api/v1/bookings/{id}/cancel/` - Cancel booking
- `GET /api/v1/bookings/search/` - Search bookings with filters

## 🔧 Sample API Requests

### User Registration
```bash
curl -X POST http://localhost:8000/api/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password2": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890"
  }'
```

### User Login
```bash
curl -X POST http://localhost:8000/api/v1/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

### Create Vehicle
```bash
curl -X POST http://localhost:8000/api/v1/vehicles/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "make": "Toyota",
    "model": "Camry",
    "year": 2022,
    "license_plate": "ABC123",
    "vehicle_type": "sedan",
    "fuel_type": "petrol",
    "transmission": "automatic",
    "daily_rate": 50.00,
    "color": "Silver",
    "seats": 5
  }'
```

### Create Booking
```bash
curl -X POST http://localhost:8000/api/v1/bookings/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": 1,
    "start_date": "2024-01-15T10:00:00Z",
    "end_date": "2024-01-17T10:00:00Z",
    "pickup_location": "Lahore Airport",
    "return_location": "Lahore Airport",
    "notes": "Airport pickup and return"
  }'
```

## 🧪 Testing

### Run All Tests
```bash
python manage.py test
```

### Run Specific Test Files
```bash
python manage.py test users.tests
python manage.py test vehicles.tests
python manage.py test bookings.tests
```

### Manual Testing Scripts
```bash
# Test authentication
python test_auth.py

# Test vehicle management
python test_vehicles.py

# Test booking management
python test_bookings.py
```

## 📊 Database Schema

### Users
- Custom User model with additional fields (phone, address, etc.)
- JWT authentication support
- Profile management

### Vehicles
- Complete vehicle information (make, model, year, plate)
- Rental rates (daily, weekly, monthly)
- Status tracking (available, rented, maintenance)
- Owner relationship

### Bookings
- Booking lifecycle management
- Date validation and overlap prevention
- Payment status tracking
- Customer and vehicle relationships

### Payments
- Payment processing with mock Stripe integration
- Multiple payment types (deposit, full payment, refund)
- Payment status tracking
- Stripe-specific fields for real integration

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **User Permissions**: Scoped access control for all operations
- **Input Validation**: Comprehensive validation for all inputs
- **Error Handling**: Graceful error responses without exposing internals
- **CORS Configuration**: Proper cross-origin resource sharing setup

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up static file serving
- [ ] Configure logging
- [ ] Set up SSL/TLS certificates
- [ ] Configure environment variables

### Environment Variables
```bash
export SECRET_KEY="your-secret-key"
export DATABASE_URL="postgresql://user:pass@localhost/dbname"
export STRIPE_SECRET_KEY="sk_test_..."
export STRIPE_PUBLISHABLE_KEY="pk_test_..."
```

## 📈 Performance & Scalability

- **Database Optimization**: Proper indexing and query optimization
- **Pagination**: Efficient data pagination for large datasets
- **Caching Ready**: Structure supports Redis/Memcached integration
- **API Rate Limiting**: Ready for rate limiting implementation
- **Monitoring**: Logging configuration for production monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **1Now.io** for the case study opportunity
- **Django REST Framework** for the excellent API framework
- **Django community** for the robust ecosystem

## 📞 Support

For support or questions about this project:
- Create an issue in the repository
- Contact: [Your Email]
- Project URL: [Repository URL]

---

**Built with ❤️ for 1Now.io Case Study** 