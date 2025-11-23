# SmartRent – Vehicle Rental Management System

## 📌 Project Overview

SmartRent is a full‑stack **vehicle rental management system** that allows customers to browse vehicles, create bookings, make payments, and manage their profile. Admins can manage vehicles, drivers, customers, bookings, payments, and maintenance records.

This project includes a complete **Flask backend**, **HTML/CSS/JavaScript frontend**, and a structured architecture following MVC principles.

---

## 🗂️ Folder Structure

```
vehicle_rental_system/
│
├── backend/
│   ├── app/
│   │   ├── api/                # All API route files
│   │   ├── models/             # Database models (ORM)
│   │   ├── schemas/            # Data validation schemas
│   │   ├── services/           # Business logic layer
│   │   ├── utils/              # Utilities (auth, enums, validators)
│   │   ├── database.py         # DB connection setup
│   │   └── main.py             # App entry point
|   |   |__ _init_.py 
│   ├── venv/                   # Virtual environment
│   ├── requirements.txt
│   └── readme.md
│
└── frontend/
    ├── Admin/                  # Admin UI screens
    ├── customer/               # Customer UI screens
    ├── static/                 # CSS + JS
    ├── index.html
    ├── login.html
    └── register.html
```

---

## 🚀 Features

### **Customer Features**

* Register/Login using secure authentication.
* Browse vehicles (cars + bikes).
* Create bookings.
* View booking history.
* View payments.
* Update profile.
* Logout.

### **Admin Features**

* Dashboard analytics.
* Add/Delete vehicles.
* Add/Delete drivers.
* View customers.
* View and manage bookings.
* View payments.
* Add maintenance records.

---

## 🏗️ Backend Architecture (MVC)

### **Models (Database Tables)**

* User
* Customer
* Vehicle
* Driver
* Booking
* Payment
* Maintenance

### **Schemas (Validation)**

Used to validate incoming request bodies.
Examples:

* `user_schema.py`
* `booking_schema.py`
* `vehicle_schema.py`
* etc.
### **Services (Business Logic)**

* `AuthManager` → Login/Register logic
* `BookingManager` → Booking calculations, validations
* `VehicleManager` → CRUD for vehicles
* `PaymentManager` → Payment tracking
* etc.

### **API Routes**

Organized by entity:

* `/auth` → Login/Logout/Register
* `/vehicles` → Vehicle CRUD
* `/drivers` → Driver CRUD
* `/bookings` → Booking APIs
* `/payments` → Payment APIs
* `/maintenance` → Maintenance APIs

---

## 🛠️ Technology Stack

### **Frontend**

* HTML5, CSS3
* Vanilla JavaScript (Fetch API)
* Responsive design

### **Backend**

* Python Flask
* MySQL / MariaDB
* Mysql-connector-python

### **Other**

* Sessions for authentication
* Clean folder structure

---

## ⚙️ How to Run the Project

### **Backend**

1. Create virtual environment:

```
python -m venv venv
```

2. Activate it:

```
venv\Scripts\activate   # Windows
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run backend:

```
python backend/app/main.py
```

Backend starts on:

```
http://127.0.0.1:5000
```

### **Frontend**

Open another terminal:

```
cd frontend
python -m http.server 8000
```

Open in browser:

```
http://127.0.0.1:8000/index.html
```

---

## 👤 Author

**Yuvicka**
Roll No: **1024240016**
Group: **2X11**

---

## 🔗 LinkedIn Project Post
🚀 Excited to share my project: SmartRent – Online Vehicle Rental System!

🔹 Features: Customer login, Admin dashboard, Vehicle management, Driver management, Booking system, Payments tracking.
🔹 Built with Flask, MySQL, JavaScript.
🔹Backend Based on Python OOPS concept

Proud of completing this full-stack project as part of my coursework.
Feel free to check it out!


---

## 📄 License

This project is for academic use and learning purposes.

