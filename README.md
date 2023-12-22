# E-Shop Purchase orders

A brief description of your Django project.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

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

## Project Structure

Describe the main components and structure of your Django project.
