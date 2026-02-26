# Portfolio Form Integration with Supabase

This project now uses **Supabase** for storing form submissions instead of local JSON files. All form data is stored in a cloud database, making it accessible from anywhere.

## 🚀 Quick Setup

### Step 1: Create Supabase Account and Project

1. Go to [supabase.com](https://supabase.com) and sign up for a free account
2. Create a new project
3. Set a strong database password and choose a region closest to you
4. Wait for the project to initialize (2-3 minutes)

### Step 2: Create the `messages` Table

1. In your Supabase dashboard, go to **SQL Editor**
2. Click **New Query**
3. Paste this SQL:

```sql
CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Create policy to allow anyone to insert
CREATE POLICY "Allow public insert"
ON messages FOR INSERT
WITH CHECK (true);

-- Create policy to allow anyone to select
CREATE POLICY "Allow public select"
ON messages FOR SELECT
WITH CHECK (true);

-- Create policy to allow anyone to delete
CREATE POLICY "Allow public delete"
ON messages FOR DELETE
WITH CHECK (true);
```

4. Click **Run**

### Step 3: Get Your Credentials

1. Go to **Settings** > **API** in your Supabase dashboard
2. Copy your **Project URL** (looks like: `https://your-project.supabase.co`)
3. Copy your **anon public** API key (starts with `eyJhbGc...`)

⚠️ **IMPORTANT**: Only use the **anon public** key, NOT the service role key!

### Step 4: Add Credentials to Your Project

1. Open `static/supabase-config.js`
2. Replace the placeholders:

```javascript
const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGc...(your-key)...';
```

3. Save the file

### Step 5: Test Locally

```bash
python app.py
```

1. Go to `http://localhost:5000`
2. Fill out and submit the form
3. Go to View Report and login with:
   - **Username**: `admin`
   - **Password**: `admin123`
4. You should see your submission in the table!

## 📋 How It Works

### Form Submission Flow

```
User fills form → JavaScript sends to Supabase API → Data stored in 'messages' table
```

**File**: `static/script.js`
- Initializes Supabase client with your credentials
- Sends form data directly to Supabase
- No backend required!

### Report Dashboard

**File**: `templates/report-supabase.html`
- Fetches all messages from Supabase
- Displays in a formatted table
- Allows delete individual messages
- Allows clear all messages

### Authentication

**File**: `templates/login.html`
- Simple demo login (not connected to Supabase)
- Credentials: `admin` / `admin123`
- Session-based (uses Flask backend)

## 🔒 Security Notes

### What's Exposed?
- ✅ Your **anon public key** - Safe to expose, limited access only
- ✅ Your **Supabase URL** - Public information

### What's Protected?
- ❌ Never expose service role key in frontend code
- ❌ Private/sensitive data is protected by Row Level Security policies
- ✅ Users can only read/insert/delete, not modify table structure

### Row Level Security (RLS)

The SQL above creates policies that:
- Allow anyone to **INSERT** new messages
- Allow anyone to **SELECT** (read) all messages
- Allow anyone to **DELETE** messages

For production, you might want to:
- Restrict deletions to authenticated users only
- Add rate limiting to prevent spam
- Add email verification

## 🌐 Deploy to Vercel

1. Push to GitHub:
```bash
git add -A
git commit -m "Integrate Supabase for form storage"
git push origin main
```

2. In Vercel dashboard, redeploy your project (it auto-detects changes)

3. Vercel will automatically read your `supabase-config.js` and use those credentials

## 📁 File Structure

```
portfolio/
├── static/
│   ├── script.js                 # Form submission & Supabase client
│   ├── supabase-config.js        # Supabase credentials (add yours here!)
│   ├── style.css
├── templates/
│   ├── index.html                # Main form page
│   ├── login.html                # Login page
│   ├── report-supabase.html      # Report dashboard (Supabase-powered)
├── app.py                        # Flask backend (minimal)
├── requirements.txt
└── vercel.json
```

## 🐛 Troubleshooting

### Form not submitting?
1. Check browser console (F12 → Console tab)
2. Verify credentials in `supabase-config.js`
3. Check Supabase dashboard for new rows

### Report page shows "Loading..."?
1. Check console for errors
2. Verify you're logged in (`admin`/`admin123`)
3. Make sure credentials are correct
4. Check Supabase table has rows

### Getting 5xx errors?
1. Check if `messages` table exists
2. Verify Row Level Security policies are created
3. Check Supabase dashboard for errors

## 📚 Further Reading

- [Supabase Docs](https://supabase.com/docs)
- [Supabase JavaScript Client](https://supabase.com/docs/reference/javascript/introduction)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)

## ✨ What You Get

✅ Cloud database storage  
✅ No server-side code needed  
✅ Real-time capabilities (optional)  
✅ Free tier: 500 MB storage, unlimited API calls  
✅ Production-ready and scalable  

Enjoy your Supabase-powered portfolio! 🚀
