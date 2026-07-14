from django import forms
from course.models import Course, Section, Lesson, LEVEL_CHOICES

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'short_description', 'category', 'skill_level',
            'total_duration', 'price', 'discount_percent', 'image',
            'overview', 'tag',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'عنوان دوره را وارد کنید'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2, 'placeholder': 'کلمات کلیدی را وارد کنید'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select js-choice border-0 z-index-9 bg-transparent'
            }),
            'skill_level': forms.Select(attrs={
                'class': 'form-select js-choice border-0 z-index-9 bg-transparent'
            }),
            'total_duration': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'زمان دوره را وارد کنید'
            }),
            'price': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'قیمت دوره را وارد کنید'
            }),
            'discount_percent': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'درصد تخفیف را وارد کنید'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control stretched-link'
            }),
            'tag': forms.TextInput(attrs={
                'class': 'form-control js-choice mb-0',
                'data-placeholder': 'true',
                'data-max-item-count': '14',
				'data-placeholder-val': "تگ ها را وارد کنید",
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "دسته‌بندی را انتخاب کنید"
        self.fields['skill_level'].choices = [("", "سطح دوره را انتخاب کنید")] + list(LEVEL_CHOICES)
        self.fields['price'].initial = None
        self.fields['discount_percent'].initial = None

    def clean_skill_level(self):
        value = self.cleaned_data.get('skill_level')
        if not value:
            raise forms.ValidationError("لطفاً سطح دوره را انتخاب کنید.")
        return value

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان سرفصل را وارد کنید'
            }),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'video', 'duration']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان درس را وارد کنید'
            }),
            'video': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مدت زمان (به دقیقه)'
            }),
        }