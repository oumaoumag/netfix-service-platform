# NetFix Service Platform

![NetFix Logo](static/css/logo.png)

NetFix is a Django-based service marketplace that connects companies offering home services with customers seeking them. The platform allows companies to list their services and customers to request them, providing a seamless interaction between service providers and consumers.

## Features

- **User Management**
  - Dual registration for companies and customers
  - Email-based authentication
  - Profile management with role-based access control

- **Service Management**
  - Companies can create and list services
  - Customers can request services
  - Dynamic pricing and service categorization
  - Service history tracking

- **User Interface**
  - Responsive design with a modern look
  - Dynamic navigation based on user roles
  - Interactive elements for better user experience

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://learn.zone01kisumu.ke/git/oumouma/netfix.git
   cd netfix
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   python manage.py migrate
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

- **main**: Core application with templates and base views.
- **services**: Manages service-related functionalities.
- **users**: Custom user system with registration and authentication.
- **static**: Contains CSS and other static assets.
- **templates**: HTML templates for rendering views.

## Models Overview

### Users (users/models.py)
- **User**: Custom user model extending `AbstractUser` with roles for company and customer.
- **Company**: Represents service providers with fields for specialization and rating.
- **Customer**: Represents service consumers with a date of birth for age calculation.

### Services (services/models.py)
- **Service**: Represents services offered by companies, with fields for pricing, category, and company association.
- **RequestService**: Tracks service requests by customers, including duration and location.

## Templates

- **Base Template**: `main/templates/main/base.html` - Provides the basic structure for all pages.
- **Home Page**: `main/templates/main/home.html` - Displays the most requested services.
- **Profile Page**: `users/templates/users/profile.html` - Shows user-specific information and services.

## Static Files

- **CSS**: Located in `static/css/style.css`, providing styling for the entire application.
- **Images**: Stored in the static directory for use in templates.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a detailed description.
4. Follow PEP8 guidelines for code style.

## Authors

- **Sheilla Juma** - [GitHub Profile](https://learn.zone01kisumu.ke/git/sjuma)
- **Ouma Ouma** - [GitHub Profile](https://github.com/oumaoumag)

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

