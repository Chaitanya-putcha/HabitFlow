# HabitFlow Development Guide

This guide will help you set up your development environment and contribute to HabitFlow.

## Getting Started

### System Requirements

- Python 3.8 or higher
- pip or conda
- Git
- Code editor (VS Code, PyCharm, Sublime Text, etc.)

### Initial Setup

1. **Clone or download the repository**

```bash
git clone https://github.com/username/habitflow.git
cd habitflow
```

2. **Create virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
pip install flask-shell-ipython  # Optional: enhanced Flask shell
```

4. **Configure environment**

```bash
cp .env.example .env
# Edit .env for your local setup
```

5. **Initialize database**

```bash
# For SQLite (development)
python -c "from app import create_app; app = create_app(); app.app_context().push()"

# For PostgreSQL (optional)
flask db init
flask db migrate
flask db upgrade
```

6. **Run development server**

```bash
python run.py
# or
flask run
```

Visit `http://localhost:5000` in your browser.

## Project Structure

```
habitflow/
├── app/
│   ├── __init__.py              # App factory and setup
│   ├── models.py                # Database models
│   ├── views.py                 # Frontend routes
│   └── routes/
│       ├── __init__.py
│       ├── auth.py              # Authentication
│       ├── dashboard.py         # Dashboard data
│       ├── habits.py            # Habit CRUD
│       ├── categories.py        # Category management
│       ├── logs.py              # Activity logging
│       ├── statistics.py        # Analytics
│       ├── profile.py           # User profile
│       └── calendar.py          # Calendar views
├── static/
│   ├── index.html               # Landing page
│   ├── dashboard.html           # Main app interface
│   ├── css/
│   │   └── main.css             # Styling
│   └── js/
│       ├── main.js              # Core functionality
│       └── dashboard.js         # Dashboard logic
├── config.py                    # Configuration
├── run.py                       # Entry point
└── requirements.txt             # Dependencies
```

## Development Workflow

### Creating a Feature

1. **Create a feature branch**

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**

3. **Test your changes**

```bash
# Run application
python run.py

# Test in browser
# http://localhost:5000
```

4. **Commit your work**

```bash
git add .
git commit -m "Add your feature description"
```

5. **Push and create Pull Request**

```bash
git push origin feature/your-feature-name
```

### Code Style Guide

#### Python

- Follow PEP 8 style guide
- Use type hints where applicable
- Write docstrings for functions and classes
- Use meaningful variable names

Example:

```python
def calculate_current_streak(habit: Habit) -> int:
    """
    Calculate the current streak for a habit.
    
    Args:
        habit: The habit object to calculate streak for
        
    Returns:
        The number of consecutive days/weeks/months the habit was completed
    """
    # Implementation
    pass
```

#### JavaScript

- Use ES6+ features
- Use meaningful variable names
- Write comments for complex logic
- Use async/await for promises

Example:

```javascript
/**
 * Load habits from the API
 * @returns {Promise<Array>} Array of habit objects
 */
async function loadHabits() {
    const response = await HabitFlow.api.fetchAPI('/habits');
    if (response?.ok) {
        const habits = await response.json();
        return habits;
    }
    return [];
}
```

#### HTML/CSS

- Use semantic HTML
- Use Tailwind classes for styling
- Keep IDs and classes meaningful
- Comment complex sections

### Testing

#### Manual Testing

1. **Test authentication**
   - Register new user
   - Login/logout
   - Password change

2. **Test habit management**
   - Create habit
   - Edit habit
   - Delete/archive habit
   - Toggle favorite

3. **Test activity logging**
   - Log activities
   - Edit/delete logs
   - Filter logs

4. **Test UI/UX**
   - Try dark mode
   - Test on mobile
   - Test all pages

#### Running Tests

```bash
# Create tests directory if not exists
mkdir tests

# Run tests
python -m pytest tests/

# With coverage
python -m pytest --cov=app tests/
```

### Database Changes

When making database changes:

1. **Update model in `app/models.py`**

2. **Create migration**

```bash
flask db migrate -m "Description of change"
```

3. **Review the migration** in `migrations/versions/`

4. **Apply migration**

```bash
flask db upgrade
```

### API Changes

When adding/modifying API endpoints:

1. **Update route file** in `app/routes/`

2. **Add documentation** in the route file

3. **Update README.md** API section

4. **Test endpoint** with curl or Postman

Example:

```bash
curl -X POST http://localhost:5000/api/habits \
  -H "Content-Type: application/json" \
  -d '{"name":"New Habit","frequency":"daily"}'
```

## Debugging

### Flask Shell

```bash
flask shell

>>> from app import db
>>> from app.models import User, Habit
>>> users = User.query.all()
>>> habit = Habit.query.first()
```

### Print Debugging

```python
# In Python
print(f"Variable: {variable}")
app.logger.info(f"Debug info: {debug_info}")

# In JavaScript
console.log('Debug:', variable);
```

### Browser DevTools

1. Open Developer Tools (F12)
2. Use Network tab to inspect API calls
3. Use Console for JavaScript errors
4. Use Application tab to check storage

### Logging

Configure logging in Flask:

```python
import logging

# In run.py or app/__init__.py
if app.debug:
    logging.basicConfig(level=logging.DEBUG)
```

## Common Tasks

### Add a New Database Model

1. Edit `app/models.py`
2. Create migration: `flask db migrate -m "Add new model"`
3. Apply: `flask db upgrade`

### Add a New API Endpoint

1. Create file in `app/routes/` or add to existing file
2. Create blueprint and register in `app/__init__.py`
3. Add documentation in README.md
4. Test endpoint

### Add Frontend Feature

1. Edit relevant HTML file in `static/`
2. Add CSS to `static/css/main.css`
3. Add JavaScript to `static/js/`
4. Test in browser

### Update Dependencies

```bash
# Check outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package_name

# Update all packages
pip install --upgrade -r requirements.txt

# Update requirements.txt
pip freeze > requirements.txt
```

## Performance Tips

### Backend

- Use database indexes on frequently queried columns
- Implement query caching with Redis
- Use pagination for large datasets
- Profile slow queries with Flask-SQLAlchemy echo

### Frontend

- Lazy load images
- Debounce API calls
- Use local storage for caching
- Minify production assets

## Security Best Practices

1. **Never commit secrets** to repository
2. **Validate all user input** on backend
3. **Use HTTPS** in production
4. **Implement rate limiting** for APIs
5. **Keep dependencies updated**
6. **Use security headers** (HSTS, CSP, etc.)

## Documentation

When adding features, update:

1. **README.md** - Add to features/API sections
2. **Code comments** - Explain complex logic
3. **Docstrings** - Document functions and classes
4. **CHANGELOG.md** - Log version changes

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
flask run --port 5001
```

### Database Issues

```bash
# Reset database (WARNING: Deletes all data)
rm instance/habitflow.db

# Or with PostgreSQL
dropdb habitflow
createdb habitflow
flask db upgrade
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

## Performance Profiling

### CPU Profiling

```python
from werkzeug.middleware.profiler import ProfilerMiddleware

app = ProfilerMiddleware(app)
app.run()
```

### Query Profiling

```python
# In config.py
SQLALCHEMY_ECHO = True  # Logs all SQL queries
```

## Contributing Guidelines

1. Fork the repository
2. Create feature branch
3. Follow code style
4. Test your changes
5. Write clear commit messages
6. Submit pull request
7. Address review feedback

## Useful Commands

```bash
# Run app
python run.py

# Flask shell
flask shell

# Database migrations
flask db init          # Initialize migrations
flask db migrate       # Create migration
flask db upgrade       # Apply migration
flask db downgrade     # Rollback migration

# Format code
autopep8 --in-place app/*.py app/routes/*.py

# Run tests
python -m pytest

# Check for errors
flake8 app/ static/js/
```

## Getting Help

1. Check existing issues on GitHub
2. Read error messages carefully
3. Check application logs
4. Search Stack Overflow
5. Ask in project discussions

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/)
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [Tailwind CSS](https://tailwindcss.com/docs)

---

Happy coding! 🚀

If you have questions, feel free to open an issue or discussion.
