# 🧠 KazReddit — Reddit-style Forum Built with Django
KazReddit is a monolithic Reddit-style forum application built with Django. It allows users to register, log in, create subreddits, make posts, and leave threaded comments in a structured and minimalist environment. Designed as a full-stack educational project, it’s built with maintainability and extensibility in mind.

# 🚀 Features
✅ User Authentication

Built-in Django User model

Login & registration with session-based auth

Protected comment posting and subreddit/post creation

# 🧵 Reddit-style Subreddit System

Create and browse named subreddits

Posts are scoped by subreddit context

# 📝 Post Management

Post title and body creation via web forms

Per-subreddit post listing

Author tracking per post

# 💬 Threaded Comments

Fully nested comment system using self-referencing Comment model

Tree structure rendered recursively (like Reddit threads)

Reply forms per comment (with/without JS)

Only authenticated users can post or reply

# 🧹 Clean Django Architecture

Class-based views (ListView, DetailView, CreateView)

Static file management for CSS/JS

CSRF protection & security best practices

🛠 Tech Stack
Python 3.11+

Django 5.2

SQLite (default) — can be swapped with PostgreSQL

HTML5 + CSS3 + minimal JS (for inline reply toggling)

Bootstrap-free, custom styling

# 📂 Project Structure (Simplified)
bash
Копировать
Редактировать
KazReddit/
│
├── core/                    # Main Django app
│   ├── models.py            # Post, Comment, Subreddit
│   ├── views.py             # All views (class-based)
│   ├── templates/core/      # HTML templates
│   └── static/core/         # CSS and JS
│
├── kazreddit/              # Project configuration
│   ├── urls.py
│   └── settings.py
│
├── db.sqlite3              # Default DB (add to .gitignore)
├── manage.py
└── README.md

# Clone the repo
git clone https://github.com/<your-username>/KazReddit-Django-Monolith-.git
cd KazReddit-Django-Monolith-

# Create a virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
python manage.py migrate
python manage.py runserver
✍️ Example Use Cases
Educational projects in Django

Reddit clone for small communities

Forum prototype with minimal stack

Sandbox for exploring threaded comments & nested models

🔒 Security Notes
Commenting and posting are restricted to logged-in users

CSRF protection enabled on all forms

Safe redirect on login/registration
