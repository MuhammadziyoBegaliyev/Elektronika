from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Question, Participant, UserAnswer, Feedback


@require_http_methods(["GET", "POST"])
def start_quiz(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()

        if not full_name:
            return render(request, 'quiz/start.html', {
                'error': "Iltimos, ismingizni kiriting."
            })

        participant = Participant.objects.create(full_name=full_name)

        question_ids = list(
            Question.objects.order_by('id').values_list('id', flat=True)[:10]
        )

        request.session['participant_id'] = participant.id
        request.session['question_order'] = question_ids

        return redirect('question_view', index=0)

    return render(request, 'quiz/start.html')


@require_http_methods(["GET", "POST"])
def question_view(request, index):
    participant_id = request.session.get('participant_id')
    question_order = request.session.get('question_order', [])

    if not participant_id or not question_order:
        return redirect('start_quiz')

    participant = get_object_or_404(Participant, id=participant_id)

    if index >= len(question_order):
        return redirect('result_view')

    question_id = question_order[index]
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        selected_option = request.POST.get('selected_option', '').strip().upper()

        if selected_option not in ['A', 'B', 'C', 'D']:
            selected_option = ''

        UserAnswer.objects.update_or_create(
            participant=participant,
            question=question,
            defaults={
                'selected_option': selected_option if selected_option else None,
                'is_correct': selected_option == question.correct_option
            }
        )

        return redirect('question_view', index=index + 1)

    current_question_number = index + 1
    total = len(question_order)
    progress = int((current_question_number / total) * 100) if total > 0 else 0

    context = {
        'question': question,
        'index': index,
        'total': total,
        'current_question_number': current_question_number,
        'progress': progress,
        'time_limit': 40,
    }

    return render(request, 'quiz/question.html', context)


@require_http_methods(["GET"])
def result_view(request):
    participant_id = request.session.get('participant_id')
    question_order = request.session.get('question_order', [])

    if not participant_id or not question_order:
        return redirect('start_quiz')

    participant = get_object_or_404(Participant, id=participant_id)
    answers = UserAnswer.objects.filter(participant=participant).select_related('question')

    answer_map = {answer.question.id: answer for answer in answers}

    result_data = []
    correct_count = 0
    incorrect_count = 0
    unanswered_count = 0

    questions = Question.objects.filter(id__in=question_order)

    for question in questions:
        user_answer = answer_map.get(question.id)

        if user_answer is None or not user_answer.selected_option:
            status = 'unanswered'
            unanswered_count += 1
            selected_option = None
        elif user_answer.is_correct:
            status = 'correct'
            correct_count += 1
            selected_option = user_answer.selected_option
        else:
            status = 'incorrect'
            incorrect_count += 1
            selected_option = user_answer.selected_option

        result_data.append({
            'question': question,
            'selected_option': selected_option,
            'correct_option': question.correct_option,
            'status': status,
        })

    total_questions = len(question_order)
    score_percent = int((correct_count / total_questions) * 100) if total_questions > 0 else 0

    existing_feedback = Feedback.objects.filter(participant=participant).first()

    context = {
        'participant': participant,
        'result_data': result_data,
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'unanswered_count': unanswered_count,
        'score_percent': score_percent,
        'existing_feedback': existing_feedback,
    }

    return render(request, 'quiz/result.html', context)


@require_http_methods(["POST"])
def save_feedback(request):
    participant_id = request.session.get('participant_id')

    if not participant_id:
        return redirect('start_quiz')

    participant = get_object_or_404(Participant, id=participant_id)
    message = request.POST.get('message', '').strip()

    if message:
        Feedback.objects.update_or_create(
            participant=participant,
            defaults={'message': message}
        )

    return redirect('result_view')