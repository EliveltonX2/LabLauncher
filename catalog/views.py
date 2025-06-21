# catalog/views.py (VERSÃO FINAL E CORRIGIDA COM COMENTÁRIOS)

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType

# Imports dos nossos modelos e formulários
from .models import Part, Project, Category
from .forms import PartForm, ProjectForm
from comments.models import Comment
from comments.forms import CommentForm

# --- VIEWS DE PEÇAS ---

class PartCreateView(LoginRequiredMixin, CreateView):
    model = Part
    form_class = PartForm
    template_name = 'catalog/part_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'in_review'
        return super().form_valid(form)

class PartListView(ListView):
    model = Part
    template_name = 'catalog/part_list.html'
    context_object_name = 'parts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(status='approved')
        search_query = self.request.GET.get('q')
        category_query = self.request.GET.get('category')
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if category_query:
            queryset = queryset.filter(category__id=category_query)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PartUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Part
    form_class = PartForm
    template_name = 'catalog/part_form.html'
    success_url = reverse_lazy('dashboard')
    def test_func(self):
        part = self.get_object()
        return self.request.user == part.author

class PartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Part
    template_name = 'catalog/part_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    def test_func(self):
        part = self.get_object()
        return self.request.user == part.author

class PartDetailView(FormMixin, DetailView):
    model = Part
    template_name = 'catalog/part_detail.html'
    context_object_name = 'part'
    form_class = CommentForm

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part = self.get_object()
        content_type = ContentType.objects.get_for_model(part)
        context['comments'] = Comment.objects.filter(content_type=content_type, object_id=part.pk)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.content_object = self.get_object()
        comment.save()
        return super().form_valid(form)

# --- VIEWS DE PROJETOS ---
# (A lógica é idêntica à das Peças, apenas trocando os modelos e forms)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'catalog/project_form.html'
    success_url = reverse_lazy('dashboard')
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'in_review'
        return super().form_valid(form)

class ProjectListView(ListView):
    model = Project
    template_name = 'catalog/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10
    def get_queryset(self):
        queryset = super().get_queryset().filter(status='approved')
        search_query = self.request.GET.get('q')
        category_query = self.request.GET.get('category')
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        if category_query:
            queryset = queryset.filter(category__id=category_query)
        return queryset.order_by('-created_at')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'catalog/project_form.html'
    success_url = reverse_lazy('dashboard')
    def test_func(self):
        project = self.get_object()
        return self.request.user == project.author

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'catalog/project_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    def test_func(self):
        project = self.get_object()
        return self.request.user == project.author

class ProjectDetailView(FormMixin, DetailView):
    model = Project
    template_name = 'catalog/project_detail.html'
    context_object_name = 'project'
    form_class = CommentForm

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        content_type = ContentType.objects.get_for_model(project)
        context['comments'] = Comment.objects.filter(content_type=content_type, object_id=project.pk)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.content_object = self.get_object()
        comment.save()
        return super().form_valid(form)