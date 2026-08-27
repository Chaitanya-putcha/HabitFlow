# HabitFlow - Habit Tracking Application

A modern, production-ready habit tracking web application built with Python Flask, PostgreSQL, Tailwind CSS, and Vanilla JavaScript.

## 🎯 Features

### Core Features
- ✅ **Secure Authentication** - User registration, login, logout with secure password hashing and remember me functionality
- ✅ **Habit Management** - Create, edit, delete, archive, restore, and organize habits
- ✅ **Activity Logging** - Flexible activity logging with support for multiple data types (boolean, count, duration, distance, numeric)
- ✅ **Categories** - Organize habits into custom categories with default category library
- ✅ **Streak System** - Automatic streak calculation based on habit frequency (daily, weekly, monthly)
- ✅ **Dashboard** - Personalized dashboard with quick stats, favorite habits, and recent activities
- ✅ **Calendar View** - Interactive calendar showing activity history with date filtering
- ✅ **Statistics & Analytics** - Comprehensive statistics with charts and trends
- ✅ **User Profile** - Manage profile information, preferences, and account settings
- ✅ **Theme Support** - Light, Dark, and System themes with persistent user preference
- ✅ **Responsive Design** - Fully responsive design optimized for desktop, tablet, and mobile

### Advanced Features
- 📊 Weekly and monthly progress visualization
- 🏆 Top habits by activity
- 📈 Detailed habit statistics and trends
- 🎨 Customizable habit colors and icons
- 🔔 Notes for activity logs
- 🔐 Secure password management
- 📱 Mobile-friendly interface

## 🛠 Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Database**: PostgreSQL (or SQLite for development)
- **Authentication**: Flask-Login with secure password hashing
- **Migrations**: Flask-Migrate
- **API**: RESTful APIs with JSON responses

### Frontend
- **HTML5**: Semantic markup
- **CSS**: Tailwind CSS for utility-first styling
- **JavaScript**: Vanilla ES6+ (no build tools required)
- **Charts**: Chart.js for analytics visualization
- **Icons**: Unicode/Emoji support

### DevOps
- Environment variable configuration with python-dotenv
- CORS support for cross-origin requests
- Production-ready deployment configuration

## 📋 Requirements

- Python 3.8+
- PostgreSQL 12+ (or SQLite for development)
- pip or conda for package management

## 🚀 Setup Instructions

### 1. Clone and Navigate to Project

```bash
cd "c:\Users\Chaitanya Putcha\Desktop\Placement preparation\Projects\HabitFlow"
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
# For development with SQLite, uncomment the SQLite DATABASE_URL line
# For PostgreSQL, configure the DATABASE_URL properly
```

### 5. Database Setup

```bash
# Initialize the database
flask db init

# Create migration scripts
flask db migrate

# Apply migrations
flask db upgrade

# Alternatively, for SQLite development:
# The database will be created automatically
```

### 6. Run the Application

```bash
python run.py

# The app will be available at http://localhost:5000
```

## 📖 API Documentation

### Authentication Endpoints

#### Register User
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "password": "password123"
}
```

#### Login User
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "remember_me": true
}
```

#### Get Current User
```
GET /api/auth/me
```

#### Logout
```
POST /api/auth/logout
```

### Habits Endpoints

#### Get All Habits
```
GET /api/habits?status=active&category_id=1&sort_by=name
```

#### Create Habit
```
POST /api/habits
Content-Type: application/json

{
  "name": "Morning Run",
  "description": "5km running every morning",
  "habit_type": "distance",
  "goal_value": 5,
  "goal_unit": "km",
  "frequency": "daily",
  "category_id": 1,
  "icon": "🏃",
  "color": "#ef4444"
}
```

#### Update Habit
```
PUT /api/habits/<habit_id>
Content-Type: application/json

{
  "name": "Updated Name",
  "status": "active"
}
```

#### Delete Habit
```
DELETE /api/habits/<habit_id>
```

#### Toggle Favorite
```
POST /api/habits/<habit_id>/toggle-favorite
```

#### Archive Habit
```
POST /api/habits/<habit_id>/archive
```

#### Restore Habit
```
POST /api/habits/<habit_id>/restore
```

### Activity Logs Endpoints

#### Get Logs
```
GET /api/logs?habit_id=1&date_from=2024-01-01&date_to=2024-01-31&limit=50&offset=0
```

#### Create Log
```
POST /api/logs
Content-Type: application/json

{
  "habit_id": 1,
  "value": 5,
  "notes": "Felt great today",
  "logged_date": "2024-01-15",
  "logged_time": "06:30:00"
}
```

#### Update Log
```
PUT /api/logs/<log_id>
Content-Type: application/json

{
  "value": 5.5,
  "notes": "Updated note"
}
```

#### Delete Log
```
DELETE /api/logs/<log_id>
```

### Categories Endpoints

#### Get All Categories
```
GET /api/categories
```

#### Create Category
```
POST /api/categories
Content-Type: application/json

{
  "name": "Health",
  "icon": "❤️",
  "color": "#ef4444"
}
```

#### Update Category
```
PUT /api/categories/<category_id>
Content-Type: application/json

{
  "name": "Fitness",
  "icon": "💪"
}
```

#### Delete Category
```
DELETE /api/categories/<category_id>
```

#### Initialize Default Categories
```
POST /api/categories/init-defaults
```

### Dashboard Endpoints

#### Get Dashboard Data
```
GET /api/dashboard
```

#### Get Weekly Progress
```
GET /api/dashboard/weekly-progress
```

#### Get Monthly Progress
```
GET /api/dashboard/monthly-progress
```

### Statistics Endpoints

#### Get Overview Statistics
```
GET /api/statistics/overview?days=30
```

#### Get Habit Statistics
```
GET /api/statistics/habit/<habit_id>?days=90
```

#### Get Top Habits
```
GET /api/statistics/top-habits?days=30&limit=10
```

#### Get Monthly Statistics
```
GET /api/statistics/monthly?month=1&year=2024
```

#### Get Yearly Statistics
```
GET /api/statistics/yearly?year=2024
```

#### Get Streak Data
```
GET /api/statistics/streak-data
```

### Calendar Endpoints

#### Get Calendar Month
```
GET /api/calendar/<year>/<month>
```

#### Get Date Details
```
GET /api/calendar/date/<YYYY-MM-DD>
```

#### Get Heatmap Data
```
GET /api/calendar/heatmap
```

#### Get Week View
```
GET /api/calendar/week/<year>/<week_number>
```

### Profile Endpoints

#### Get Profile
```
GET /api/profile
```

#### Update Profile
```
PUT /api/profile
Content-Type: application/json

{
  "full_name": "New Name",
  "profile_picture": "https://example.com/pic.jpg",
  "timezone": "America/New_York",
  "theme": "dark"
}
```

#### Get Preferences
```
GET /api/profile/preferences
```

#### Update Preferences
```
PUT /api/profile/preferences
Content-Type: application/json

{
  "timezone": "UTC",
  "theme": "system"
}
```

#### Change Password
```
POST /api/auth/change-password
Content-Type: application/json

{
  "current_password": "old_password",
  "new_password": "new_password"
}
```

## 📁 Project Structure

```
HabitFlow/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models.py                # Database models (User, Habit, Category, Log)
│   ├── views.py                 # Frontend views
│   └── routes/
│       ├── auth.py              # Authentication endpoints
│       ├── dashboard.py         # Dashboard data endpoints
│       ├── habits.py            # Habit management endpoints
│       ├── categories.py        # Category management endpoints
│       ├── logs.py              # Activity log endpoints
│       ├── statistics.py        # Statistics and analytics endpoints
│       ├── profile.py           # User profile endpoints
│       └── calendar.py          # Calendar view endpoints
├── static/
│   ├── index.html               # Landing page
│   ├── dashboard.html           # Dashboard page
│   ├── css/
│   │   └── main.css             # Main stylesheet
│   └── js/
│       ├── main.js              # Core functionality and API helpers
│       └── dashboard.js         # Dashboard interactions
├── config.py                    # Configuration management
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment configuration template
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## 🗄️ Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- full_name
- profile_picture
- timezone
- theme
- created_at
- updated_at

### Categories Table
- id (Primary Key)
- user_id (Foreign Key)
- name
- description
- icon
- color
- is_default
- created_at
- updated_at

### Habits Table
- id (Primary Key)
- user_id (Foreign Key)
- category_id (Foreign Key, nullable)
- name
- description
- icon
- color
- habit_type (boolean, count, duration, distance, numeric)
- goal_value
- goal_unit
- frequency (daily, weekly, monthly)
- status (active, archived, disabled)
- is_favorite
- display_order
- created_at
- updated_at

### Habit Logs Table
- id (Primary Key)
- user_id (Foreign Key)
- habit_id (Foreign Key)
- value (nullable)
- notes
- logged_date
- logged_time (nullable)
- created_at
- updated_at

## 🎨 UI/UX Highlights

- **Clean Design**: Minimalist, modern interface inspired by Notion, GitHub, and Linear
- **Responsive Layout**: Works seamlessly on all devices
- **Dark Mode Support**: Easy on the eyes with customizable themes
- **Smooth Animations**: Subtle transitions and hover effects
- **Accessible**: Semantic HTML and keyboard navigation support
- **Performance**: Optimized frontend with lazy loading and efficient API calls

## 🔐 Security Features

- ✅ Secure password hashing with Werkzeug
- ✅ CSRF protection with Flask
- ✅ SQL injection prevention with SQLAlchemy ORM
- ✅ Secure session management with Flask-Login
- ✅ HTTPOnly and Secure cookie flags
- ✅ Input validation and sanitization
- ✅ Protected routes with login requirements

## 📦 Deployment

### Preparing for Production

1. Set environment variables in `.env`:
   ```
   FLASK_ENV=production
   SECRET_KEY=<strong-random-key>
   DATABASE_URL=postgresql://user:password@host:port/db_name
   ```

2. Configure a production WSGI server (Gunicorn, uWSGI)

3. Set up a reverse proxy (Nginx, Apache)

4. Enable HTTPS/SSL

5. Configure database backups

### Deployment Platforms

This application can be deployed on:
- **Render** (built-in support)
- **Railway** (built-in support)
- **Heroku** (with Procfile configuration)
- **AWS** (EC2, ECS, Elastic Beanstalk)
- **DigitalOcean** (App Platform, Droplets)
- **Azure** (App Service, Container Instances)

## 🚀 Future Enhancements

- [ ] Email notifications and reminders
- [ ] Push notifications
- [ ] Habit sharing and social features
- [ ] AI-powered habit insights
- [ ] CSV/PDF export
- [ ] Cloud backup and restore
- [ ] OAuth authentication (Google, GitHub)
- [ ] Progressive Web App (PWA) support
- [ ] Offline functionality
- [ ] Multilingual support
- [ ] Achievement badges and gamification
- [ ] Leaderboards
- [ ] Intelligent habit recommendations

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 💬 Support

For support, please:
- Check the documentation in this README
- Review the API documentation section
- Check the application logs for errors
- Create an issue if you find a bug

## 👨‍💻 Author

Built with ❤️ for productivity and habit tracking.

---

**Happy Tracking! 🎯**

Start building your best habits with HabitFlow today!
