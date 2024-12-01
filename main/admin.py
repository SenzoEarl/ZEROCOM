from django.contrib import admin

from main.models import *


# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]  # Nest Answer inline under Question inline


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'author', 'publish', 'created_at']
    search_fields = ['title', 'body']
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['publish', 'status']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_at', 'active']
    list_filter = ['active', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'body']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer_text', 'is_correct']
    search_fields = ['answer_text']
    list_filter = ['question__quiz', 'is_correct']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['quiz', 'question_text']
    search_fields = ['question_text']
    list_filter = ['quiz']
    ordering = ['quiz']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'author', 'created_at', 'active']
    search_fields = ['title', 'description']

admin.site.register(Lottery)