"""
Main application entry point.
"""
import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create application instance
app = create_app(config_name=os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Run the development server
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_ENV') == 'development'
    )
