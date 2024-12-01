from itertools import chain
from lib2to3.fixes.fix_input import context

from django.core.mail import send_mail
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.views.generic import ListView, View, DetailView, TemplateView

from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from main.forms import CommentForm, EmailPostForm
from main.models import Quiz, Question, Post, QuizResult, Comment, Answer, Lottery


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        # Calling the base implementation too get the default context
        context = super().get_context_data(**kwargs)

        blogs = Post.published.all()
        quizzes = Quiz.objects.all()

        combined = list(chain(blogs, quizzes))

        #add queryset to context
        context['combined_list'] = combined

        return context

class PostListView(ListView):
    queryset = Post.published.annotate(comment_count=Count('comments'))
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    comments = post.comments.filter(active=True)
    form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)


        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends that you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
            
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


class QuizListView(ListView):
    model = Quiz
    queryset = Quiz.objects.annotate(question_count=Count('questions'))
    template_name = 'quiz/post/list.html'
    context_object_name = 'quizzes'


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/post/detail.html'  # Replace with your template
    context_object_name = 'quiz'


class QuizSubmitView(View):
    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        score = 0
        total_questions = quiz.questions.count()
        results = []  # To store question, selected answer, and correct answer

        # Iterate over all the questions in the quiz
        for question in quiz.questions.all():
            selected_answer_id = request.POST.get(str(question.id))
            selected_answer = None
            correct_answer = None

            # Get the selected answer if provided
            if selected_answer_id:
                selected_answer = Answer.objects.get(id=selected_answer_id)

            # Find the correct answer for this question
            correct_answer = question.answers.filter(is_correct=True).first()

            # Check if the selected answer is correct
            if selected_answer and selected_answer.is_correct:
                score += 1

            # Append result data for this question
            results.append({
                'question': question,
                'selected_answer': selected_answer,
                'correct_answer': correct_answer
            })

        # Save the result
        QuizResult.objects.create(
            contestant=request.user.username,  # Assuming logged-in user
            quiz=quiz,
            score=score
        )

        # Pass results and other details to the template
        context = {
            'quiz': quiz,
            'score': score,
            'total': total_questions,
            'results': results
        }
        return render(request, 'quiz/post/quiz_result.html', context)


class QuizResultView(View):
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        result = QuizResult.objects.filter(contestant=request.user.username, quiz=quiz).last()
        context = {
            'quiz': quiz,
            'score': result.score,
            'total': quiz.questions.count(),
        }
        return render(request, 'quiz/post/quiz_result.html', context)


class QuizResultsListView(ListView):
    model = QuizResult
    template_name = 'quiz/post/quiz_results_list.html'
    context_object_name = 'results'

    def get_queryset(self):
        quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        return QuizResult.objects.filter(quiz=quiz).order_by('-completed_at')

    def get_context_data(self, **kwargs):
        # Call the base implementation to get the default context
        context = super().get_context_data(**kwargs)

        # Get the quiz object
        quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])

        # Add the total number of questions to the context
        total_questions = quiz.questions.count()
        context['total_questions'] = total_questions

        return context


class LotteryList(ListView):
    model = Lottery
    template_name = 'lottery/list.html'
    context_object_name = 'lottery'
