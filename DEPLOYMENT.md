# HabitFlow Deployment Guide

This guide covers deploying HabitFlow to various platforms.

## Prerequisites

- Python 3.8+
- PostgreSQL database access
- Git repository (optional but recommended)

## Environment Setup

Before deploying, ensure your `.env` file contains all required variables:

```env
FLASK_ENV=production
FLASK_APP=run.py
SECRET_KEY=<strong-random-key-change-this>
DATABASE_URL=postgresql://user:password@host:port/database_name
PORT=5000
DEBUG=False
```

Generate a strong SECRET_KEY:

```bash
python -c 'import os; print(os.urandom(24).hex())'
```

## Deployment Platforms

### 1. Render (Recommended for Easy Setup)

#### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/habitflow.git
git push -u origin main
```

#### Step 2: Connect to Render

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the HabitFlow repository
5. Set up the following:
   - **Name**: habitflow
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && flask db upgrade`
   - **Start Command**: `gunicorn run:app`
   - **Plan**: Free or Pro

#### Step 3: Add Environment Variables

In Render dashboard:
1. Go to "Environment" tab
2. Add variables:
   - `FLASK_ENV=production`
   - `SECRET_KEY=<your-generated-key>`
   - `DATABASE_URL=<render-postgres-url>`
   - `DEBUG=False`

#### Step 4: Add Database

1. In Render dashboard, click "New +" → "PostgreSQL"
2. Set up PostgreSQL database
3. Copy the connection string to `DATABASE_URL` environment variable

#### Step 5: Deploy

The deployment should start automatically when you push to GitHub.

### 2. Railway

#### Step 1: Install Railway CLI

```bash
npm i -g @railway/cli
```

#### Step 2: Login

```bash
railway login
```

#### Step 3: Initialize Project

```bash
railway init
```

#### Step 4: Add Environment Variables

```bash
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=<your-generated-key>
railway variables set DEBUG=False
```

#### Step 5: Add PostgreSQL

```bash
railway add --service postgres
```

The DATABASE_URL will be automatically set.

#### Step 6: Deploy

```bash
railway up
```

Or push to GitHub and enable GitHub integration.

### 3. Heroku

#### Step 1: Install Heroku CLI

[Download Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

#### Step 2: Login

```bash
heroku login
```

#### Step 3: Create App

```bash
heroku create habitflow-app
```

#### Step 4: Add PostgreSQL

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

#### Step 5: Set Environment Variables

```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=<your-generated-key>
heroku config:set DEBUG=False
```

#### Step 6: Deploy

```bash
git push heroku main
```

Run migrations:

```bash
heroku run flask db upgrade
```

### 4. AWS Elastic Beanstalk

#### Step 1: Install EB CLI

```bash
pip install awsebcli
```

#### Step 2: Initialize

```bash
eb init -p python-3.11 habitflow
```

#### Step 3: Create Environment

```bash
eb create habitflow-env
```

#### Step 4: Set Environment Variables

```bash
eb setenv FLASK_ENV=production SECRET_KEY=<key> DEBUG=False
```

#### Step 5: Deploy

```bash
eb deploy
```

### 5. DigitalOcean App Platform

#### Step 1: Connect GitHub

1. Go to DigitalOcean App Platform
2. Click "Create App"
3. Connect GitHub account
4. Select the HabitFlow repository

#### Step 2: Configure

1. Set up the web service:
   - **Build Command**: `pip install -r requirements.txt && flask db upgrade`
   - **Run Command**: `gunicorn run:app`

2. Add PostgreSQL database

3. Set environment variables

#### Step 3: Deploy

Click "Deploy" to start deployment.

### 6. Docker Deployment

#### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

#### Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:password@db:5432/habitflow
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=habitflow
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### Deploy with Docker

```bash
docker-compose up -d
```

## Post-Deployment Checks

After deployment, verify:

1. **Application is running**
   ```bash
   curl https://your-app-url.com
   ```

2. **Database connection**
   - Check application logs
   - Verify migrations have run

3. **SSL/TLS**
   - Ensure HTTPS is enabled
   - Check certificate validity

4. **Environment variables**
   - Verify all required variables are set
   - Don't expose sensitive values in logs

5. **Database backups**
   - Set up automated backups
   - Test backup restoration

## Monitoring and Maintenance

### Enable Logging

Check application logs regularly for errors:

```bash
# On render.com
# View in dashboard under "Logs"

# On Railway
railway logs

# On Heroku
heroku logs --tail
```

### Database Backups

Set up automatic backups through your platform:

- **Render**: Automatic daily backups
- **Railway**: Configure backup snapshots
- **Heroku**: Use Heroku PG Backups
- **AWS**: Use AWS RDS automated backups
- **DigitalOcean**: Enable automated backups

### Performance Optimization

1. Enable caching headers
2. Use CDN for static files
3. Optimize database queries
4. Monitor application performance

### Security Updates

Regularly update dependencies:

```bash
pip list --outdated
pip install --upgrade <package>
```

Update requirements.txt and redeploy.

## Troubleshooting

### Application Won't Start

1. Check environment variables are set
2. Verify database connection string
3. Check logs for specific errors
4. Ensure Python version is correct

### Database Connection Issues

1. Verify DATABASE_URL format
2. Check database user/password credentials
3. Ensure firewall allows connections
4. Test connection locally first

### Static Files Not Loading

1. Ensure Flask is serving static files correctly
2. Check static folder is included in deployment
3. For production, use a web server like Nginx

### Migration Errors

1. Ensure Flask-Migrate is installed
2. Check database permissions
3. Verify migration files are included

## Performance Tips

1. Use connection pooling
2. Enable query caching
3. Optimize database indexes
4. Use gzip compression
5. Minify static assets
6. Implement API rate limiting

## Security Checklist

- [ ] Change SECRET_KEY to strong random value
- [ ] Set DEBUG=False in production
- [ ] Use HTTPS/SSL
- [ ] Secure database connection
- [ ] Set secure session cookies
- [ ] Enable CORS only for trusted origins
- [ ] Implement rate limiting
- [ ] Regular security audits
- [ ] Keep dependencies updated
- [ ] Monitor for suspicious activity

## Scaling

As your application grows:

1. Upgrade database plan
2. Add caching layer (Redis)
3. Implement load balancing
4. Separate API and web servers
5. Use CDN for static assets
6. Implement monitoring and alerting

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://railway.app/docs)
- [Heroku Docs](https://devcenter.heroku.com/)

---

For more help, check the main README.md or create an issue in the repository.
