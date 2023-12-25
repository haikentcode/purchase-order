# E-Shop Purchase orders

A brief description of your Django project.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Testing](#testing)
- [Project Structure](#project-structure)
- [API-Endpoints](#API-Endpoints)
- [API-Documentation](#API-Documentation)

## Getting Started

### Prerequisites

- Python 3.x
- Pipenv (optional but recommended for managing dependencies)

### Installation

1. Clone the repository:

   ```bash
   $ git clone https://github.com/haikentcode/purchase-order.git
   $ cd purchase-order
   ```

2. Create a virtual environment to install dependencies in and activate it:

   ```sh
   #using venv ( Note: python --> python3 )
   $ python -m venv sumtracker
   $ source sumtracker/bin/activate
   ```

   ```sh
   #using pyenv( creating env with python version 3.11.5)
   $ pyenv virtualenv 3.11.5 sumtracker
   $ pyenv activate sumtracker
   ```

3. Install dependencies:

   ```sh
   (sumtracker)../purchase-order $ pip install -r requirements.txt
   ```

4. Apply migrations:

   ```sh
   (sumtracker)../purchase-order $ cd eshop
   (sumtracker)../purchase-order/eshop $ python manage.py migrate
   ```

5. Run the development server:

   ```sh
   (sumtracker)../purchase-order/eshop $ python manage.py runserver
   ```

6. Creating a Superuser 
   ```sh
   (sumtracker)../purchase-order/eshop $ python manage.py createsuperuser
   ```

### Testing
```
(sumtracker)../purchase-order $ python manage.py test  



Found 18 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..................
----------------------------------------------------------------------
Ran 18 tests in 21.744s

OK
Destroying test database for alias 'default'...
```

## Project Structure

```
── LICENSE
├── README.md
├── eshop
│   ├── eshop
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── purchase
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── filters.py
│       ├── management
│       │   └── commands
│       │       └── populate_data.py
│       ├── migrations
│       │   ├── 0001_initial.py
│       │   └── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── test.py
│       ├── urls.py
│       └── views.py
└── requirements.txt
```


# API Endpoints
## The project includes the following API endpoints:
```
Suppliers: /purchase/suppliers// - 
Orders: /purchase/orders/ - 
Line Items: /purchase/line_items/ - 

```


## API-Documentation
### You can explore the API documentation using the following tools:
```
Swagger UI: To view the API documentation using Swagger UI, 
navigate to http://127.0.0.1:8000/api/swagger-ui/ in your web browser.

ReDoc: For a more interactive documentation experience, 
you can visit http://127.0.0.1:8000/docs/.

```

