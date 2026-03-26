from django.contrib import admin
from django import forms
from .models import Question, Participant, UserAnswer, Feedback


class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
            'option_a': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
            'option_b': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
            'option_c': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
            'option_d': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
        }


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ('id', 'short_text', 'correct_option')
    search_fields = ('text',)

    def short_text(self, obj):
        return obj.text[:60]
    short_text.short_description = "Savol"


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'started_at')
    search_fields = ('full_name',)
    list_filter = ('started_at',)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant', 'question_short', 'selected_option', 'is_correct', 'answered_at')
    list_filter = ('is_correct', 'selected_option', 'answered_at')
    search_fields = ('participant__full_name', 'question__text')

    def question_short(self, obj):
        return obj.question.text[:50]
    question_short.short_description = "Savol"


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant_name', 'short_message', 'created_at')
    search_fields = ('participant__full_name', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('participant', 'message', 'created_at')

    def participant_name(self, obj):
        return obj.participant.full_name
    participant_name.short_description = "Foydalanuvchi"

    def short_message(self, obj):
        return obj.message[:80]
    short_message.short_description = "Izoh"