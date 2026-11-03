"""
Account views: registration (student + instructor), profile, student dashboard,
quality switcher (HD <-> Low bandwidth for Tier-1 / Tier-2/3 support).
"""
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django import forms

from .models import User
from courses.models import Course
from enrollments.models import Enrollment
from progress.models import LessonProgress


class StudentSignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'city', 'state', 'tier')

    def clean_password2(self):
        p1, p2 = self.cleaned_data.get('password1'), self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.role = User.Role.STUDENT
        if commit:
            user.save()
        return user


class InstructorSignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone',
                  'specialization', 'experience_years', 'bio')

    def clean_password2(self):
        p1, p2 = self.cleaned_data.get('password1'), self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.role = User.Role.INSTRUCTOR
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'city', 'state',
                  'tier', 'avatar', 'bio')


def register(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('course_list')
    else:
        form = StudentSignupForm()
    return render(request, 'accounts/register.html', {
        'form': form, 'title': 'Student Registration'
    })


def register_instructor(request):
    if request.method == 'POST':
        form = InstructorSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('instructor_dashboard')
    else:
        form = InstructorSignupForm()
    return render(request, 'accounts/register.html', {
        'form': form, 'title': 'Instructor Registration'
    })


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def student_dashboard(request):
    """Show enrolled courses with progress + billing status."""
    if not request.user.is_student:
        return redirect('home')

    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course').order_by('-enrolled_at')

    # Aggregate progress per enrollment
    dashboard_data = []
    for e in enrollments:
        total_lessons = e.course.total_lessons
        completed = LessonProgress.objects.filter(
            enrollment=e, completed=True
        ).count()
        pct = (completed / total_lessons * 100) if total_lessons else 0
        dashboard_data.append({
            'enrollment': e,
            'completed_lessons': completed,
            'total_lessons': total_lessons,
            'progress_pct': round(pct, 1),
            'next_lesson': e.course.next_lesson_for(e),
        })

    recommended = Course.objects.exclude(
        id__in=[e.course_id for e in enrollments]
    ).filter(is_published=True)[:4]

    return render(request, 'accounts/dashboard.html', {
        'dashboard_data': dashboard_data,
        'recommended': recommended,
    })


@require_POST
@login_required
def switch_quality(request):
    """Toggle between Tier-1 (HD) and Tier-2/3 (Low bandwidth) video defaults."""
    tier = request.POST.get('tier')
    if tier in ('tier1', 'tier2'):
        request.user.tier = tier
        request.user.save(update_fields=['tier'])
    return redirect(request.META.get('HTTP_REFERER', reverse('student_dashboard')))
