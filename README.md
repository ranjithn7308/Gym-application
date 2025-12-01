# Arnold Gym Django Backend (Minimal Admin UI)

This repository contains a small Django project scaffold for a gym management admin dashboard focused on backend functionality. The templates and CSS are intentionally minimal and match the colors/style in the attached mockups.

Quick start (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` to see the login screen (use the superuser you created).

Files of interest:
- `gymapp/models.py` — core backend models (Member, MembershipPlan, Inventory, Payment)
- `gymapp/views.py` — backend views: login, OTP password reset simulation, dashboard and registration
- `gymapp/forms.py` — forms used for member/plan/payment CRUD
- `templates/` and `static/` — minimal UI to run locally without a frontend framework

Notes:
- This is a development scaffold. Replace SECRET_KEY and DEBUG for production.
- OTP is simulated and printed via Django messages — integrate a real SMS/email provider for production.
