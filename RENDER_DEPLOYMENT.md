# Deploy Backend Portfolio API to Render

## 🚀 Deployment Instructions

### Prerequisites

- GitHub repository with your code
- Render account (free tier available)
- Database (PostgreSQL) - can use Supabase or Render's PostgreSQL

### Step 1: Prepare Your Code

1. **Make sure these files exist:**
   - `wsgi.py` - Production WSGI entry point (✅ Created)
   - `render.yaml` - Render configuration (✅ Created)
   - `requirements.txt` - Python dependencies (✅ Exists)

2. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

### Step 2: Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:

   **Basic Settings:**
   - Name: `be-portfolio` (or your preferred name)
   - Environment: `Python 3`
   - Region: `Singapore` (or nearest to your users)
   - Branch: `main`

   **Build & Deploy:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`

### Step 3: Configure Environment Variables

Add these environment variables in Render dashboard:

1. **SECRET_KEY** (Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

   ```
   Value: lxi0MIK_rJhKtyTMqLt95CXfHHWf7cFep7vKUR5LWSA
   ```

2. **JWT_SECRET_KEY** (Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

   ```
   Value: z47ZYdcZoJ1ppSd8LqiIpuRDqwXPl_sIbumb5DIK3G8
   ```

3. **FLASK_DB_URI** (Your database connection string)

   ```
   # If using Supabase:
   postgresql://postgres:[YOUR-PASSWORD]@[HOST]:5432/postgres

   # If using Render PostgreSQL:
   Use the "Internal Database URL" from Render PostgreSQL dashboard
   ```

4. **FLASK_ENV**
   ```
   Value: production
   ```

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Build your application
   - Install dependencies
   - Start the server with Gunicorn
3. Wait for deployment to complete (usually 2-5 minutes)

### Step 5: Test Your API

Once deployed, your API will be available at:

```
https://be-portfolio-xxx.onrender.com/api/v1/about
```

Test endpoints:

- Swagger Docs: `https://your-app.onrender.com/apidocs`
- About endpoint: `https://your-app.onrender.com/api/v1/about`

## 🔧 Common Issues & Solutions

### Issue 1: "Application failed to respond"

**Cause:** Port binding issue or app crash
**Solution:**

- Check logs in Render dashboard
- Ensure `wsgi.py` uses the PORT environment variable
- Verify all environment variables are set

### Issue 2: "Failed to fetch" / CORS errors

**Cause:** CORS not configured properly
**Solution:**

- ✅ Already fixed in `src/__init__.py` with proper CORS configuration
- If needed, update CORS origins to specific domains:
  ```python
  "origins": ["https://your-frontend.com", "http://localhost:3000"]
  ```

### Issue 3: Database connection errors

**Cause:** Wrong database URL or network issue
**Solution:**

- Use **Internal Database URL** if using Render PostgreSQL
- For Supabase, ensure IP is allowed
- Test connection string format: `postgresql://user:password@host:port/database`

### Issue 4: "Module not found" errors

**Cause:** Missing dependencies
**Solution:**

- Ensure all packages are in `requirements.txt`
- Add any missing packages:
  ```bash
  pip freeze > requirements.txt
  ```

### Issue 5: "SECRET_KEY not found"

**Cause:** Environment variables not set
**Solution:**

- Double-check all environment variables in Render dashboard
- Click "Deploy latest commit" after adding variables

## 📊 Monitoring

- **Logs:** Render Dashboard → Your Service → Logs tab
- **Metrics:** Monitor response times and errors in Events tab
- **Health Check:** Render will ping `/` endpoint every few minutes

## 🔄 Updating Your Deployment

1. Make code changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```
3. Render will automatically detect the push and redeploy

## 💡 Tips

1. **Free Tier Limits:**
   - Apps spin down after 15 minutes of inactivity
   - First request after spin-down may take 30-60 seconds
   - Upgrade to paid plan for always-on service

2. **Database:**
   - Use Supabase for free PostgreSQL with better uptime
   - Or use Render's PostgreSQL (free tier available but limited)

3. **Security:**
   - Never commit `.env` file to GitHub
   - Always use environment variables for secrets
   - Regenerate SECRET_KEY and JWT_SECRET_KEY for production

4. **Performance:**
   - Use Gunicorn workers: `gunicorn -w 4 wsgi:app`
   - Enable connection pooling for database
   - Cache static responses

## 📝 Checklist Before Deploy

- [ ] All environment variables set in Render
- [ ] Database is accessible from Render servers
- [ ] `requirements.txt` includes all dependencies (including `gunicorn`)
- [ ] Code pushed to GitHub main branch
- [ ] CORS configured for your frontend domain
- [ ] Health check endpoint (`/`) returns 200 OK

## 🆘 Need Help?

If you encounter issues:

1. Check Render logs first
2. Test locally with: `gunicorn wsgi:app`
3. Verify environment variables
4. Check database connectivity

Good luck with your deployment! 🚀
