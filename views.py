from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, Job
from datetime import date, datetime

# --- 1. HOME / LOGIN PAGE ---
# app/views.py

def index(request):
    # FORCE LOGOUT: Clear session when visiting the home page
    request.session.flush() 
    return render(request, 'index.html')
# --- 2. REGISTER LOGIC ---
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        dob_str = request.POST['dob']
        role = request.POST['role']
        category = request.POST['category']

        # 18+ Check
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age < 18:
            return render(request, 'index.html', {'error': 'You must be 18+'})

        # Create User
        user = UserProfile.objects.create(name=name, phone=phone, dob=dob, role=role, category=category)
        
        # Save to Session (Login)
        request.session['user_id'] = user.id
        return redirect('dashboard')

    return redirect('index')

# --- 3. DASHBOARD ---
def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id: return redirect('index') # Security check

    user = UserProfile.objects.get(id=user_id)
    today = date.today()
    
    # Get all future jobs
    jobs = Job.objects.filter(date__gte=today)

    return render(request, 'dashboard.html', {'user': user, 'jobs': jobs})

# --- 4. POST JOB ---
def post_job(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        employer = UserProfile.objects.get(id=user_id)
        
        Job.objects.create(
            title=request.POST['title'],
            location=request.POST['location'],
            date=request.POST['date'],
            pay=request.POST['pay'],
            pay_type=request.POST['type'],
            category=request.POST['category'],
            required_workers=request.POST['required'],
            employer=employer
        )
    return redirect('dashboard')

# --- 5. APPLY FOR JOB ---
def apply_job(request, job_id):
    user_id = request.session.get('user_id')
    worker = UserProfile.objects.get(id=user_id)
    job = get_object_or_404(Job, id=job_id)

    # Check Logic
    if not job.is_full() and worker not in job.applicants.all():
        job.applicants.add(worker)
    
    return redirect('dashboard')

# --- 6. LOGOUT ---
def logout(request):
    request.session.flush()
    return redirect('index')