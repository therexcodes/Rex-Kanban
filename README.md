# Rex-Kanban App

## Overview
Rex-Kanban is a task management API that enables users to create and manage boards, columns, and tasks efficiently. It provides authentication, role-based access, and a structured RESTful API to help users organize their workflow.

## Features
- User authentication & authorization (JWT-based)
- CRUD operations for Boards, Columns, and Tasks
- Role-based access (users can only modify their own data)
- Token-based authentication
- API endpoints for task organization
- Deployed backend for easy integration with frontend

---

## Installation Steps

### **1. Clone the Repository**
```sh
  git clone https://github.com/your-username/rex-kanban.git
  cd rex-kanban
```

### **2. Create a Virtual Environment & Activate**
```sh
  python -m venv env
  source env/bin/activate  # On Mac/Linux
  env\Scripts\activate  # On Windows
```

### **3. Install Dependencies**
```sh
  pip install -r requirements.txt
```

### **4. Set Up Environment Variables**
Create a `.env` file in the project root and add:
```sh
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
ALLOWED_HOSTS=*
```

### **5. Apply Migrations & Run Server**
```sh
  python manage.py migrate
  python manage.py runserver
```

---

## API Documentation

### **Authentication**
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/accounts/register/` | Register a new user |
| POST | `/api/accounts/login/` | Login & get access token |
| POST | `/api/accounts/logout/` | Logout & invalidate token |
| POST | `/api/accounts/token/refresh/` | Refresh JWT token |

### **Boards**
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/kanban/boards/` | Get all boards for the authenticated user |
| POST | `/api/kaban/boards/` | Create a new board |
| DELETE | `/api/kanban/boards/<id>/` | Delete a board |

### **Columns**
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/kanban/columns/` | Get all columns in a board |
| POST | `/api/kanban/columns/` | Create a new column in a board |
| DELETE | `/api/kanban/columns/<id>/` | Delete a column |

### **Tasks**
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/kanban/tasks/` | Get all tasks for the authenticated user |
| POST | `/api/kanban/tasks/` | Create a new task under a column |
| PUT | `/api/kanban/tasks/<id>/` | Update a task |
| DELETE | `/api/kanban/tasks/<id>/` | Delete a task |

---

## **Postman Collection**
To test API endpoints easily, import the Postman collection:
[Download Collection](https://www.postman.com/) (replace with actual link once available)

---

## **Deployment**
To deploy the project on **Render/Railway**, follow these steps:
1. Push your code to GitHub.
2. Link your GitHub repo to Render/Railway.
3. Configure environment variables.
4. Deploy and test API accessibility.

---

## Contributing
Pull requests are welcome! Ensure your code follows the project structure and best practices.





