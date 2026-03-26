from django.db import models


class Question(models.Model):
    text = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()

    CORRECT_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    correct_option = models.CharField(max_length=1, choices=CORRECT_CHOICES)

    def __str__(self):
        return self.text[:70]

class Participant(models.Model):
    full_name = models.CharField(max_length=120)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class UserAnswer(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('participant', 'question')

    def __str__(self):
        return f"{self.participant.full_name} - {self.question.text}"


class Feedback(models.Model):
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE, related_name='feedback')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback - {self.participant.full_name}"