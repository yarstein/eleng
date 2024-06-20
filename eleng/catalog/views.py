from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
import random
from django.db.models import Count, Prefetch



from .models import Article, Category, Comment, TagProduct
from .forms import CommentCreateForm
from cart.forms import CartAddProductForm


class ProductListView(ListView):
    """Представление для списка изделий"""
    model = Article
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    # queryset = Article.objects.select_related('category').filter(is_published=True)
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True).select_related('category')

        query = self.request.GET.get('q', None)
        if query:
            # queryset = queryset.filter(name__search=query)
            queryset = queryset.annotate(search=SearchVector("name", "description")).filter(search=query)
            # vector = SearchVector('name', 'description')
            # query = SearchQuery(query)
            # queryset = queryset.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        return context
    

class ProductDetailView(DetailView):
    """Представление для детальной информации об изделий"""
    model = Article
    template_name = 'catalog/catalog_detail.html'
    context_object_name = 'product'
    # Переменная, которая фигурирует в маршруте urls через slug
    slug_url_kwarg = 'arc_slug'


    def get_queryset(self):
        # Prefetch - объект, который предварительно загружает только опубликованные коменты используя queryset=
        comments_prefetch = Prefetch('comments', queryset=Comment.objects.filter(status='published'))
        return Article.objects.prefetch_related('tags', comments_prefetch).all()

    def get_similar_products(self, obj):
        """Список схожих изделий"""
        product_tags_ids = obj.tags.values_list('id', flat=True)
        similar_products = Article.objects.filter(tags__in=product_tags_ids, is_published=True).exclude(id=obj.id)
        similar_products = similar_products.annotate(related_tags=Count('tags')).order_by('-related_tags')
        similar_products_list = list(similar_products.all())
        random.shuffle(similar_products_list)
        return similar_products_list[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        # get_ancestors() - получаем всех предков в иерарх.структуре. Он возвращает QuerySet. include_self=True - включает себя в текуший узел
        context['breadcrumbs'] = self.object.category.get_ancestors(include_self=True)
        context['form'] = CommentCreateForm
        context['total_comments'] = self.object.comments.filter(status='published').count()
        context['similar_products'] = self.get_similar_products(self.object)
        context['cart_product_form'] = CartAddProductForm()
        return context
    

class ProductTagView(ListView):
    """Представление для изделий с одинаковыми тегами"""
    model = Article
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    tag = None
    paginate_by = 5


    def get_queryset(self):
        self.tag = TagProduct.objects.get(slug=self.kwargs['tag_slug'])
        queryset = Article.objects.prefetch_related('tags').filter(tags__slug=self.tag.slug, is_published=True)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Изделия по тегу: {self.tag.tag}'
        context['tag_info'] = self.tag.tag
        return context


class ProductByCategory(ListView):
    model = Article
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    category = None
    paginate_by = 5

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        # Получаем все подкатегории включая текущую категорию
        categories = self.category.get_descendants(include_self=True)   # возвращает QuerySet, включающий все подкатегории текущей категории и саму текущую категорию.
        # Метод distinct() используется для исключения дублирующихся статей,
        queryset = Article.objects.select_related('category').filter(category__in=categories, is_published=True).distinct()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + self.category.title
        context['breadcrumbs'] = self.category.get_ancestors(include_self=True)
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        product_slug = self.kwargs.get('arc_slug')
        form.instance.product = get_object_or_404(Article, slug=product_slug)
        form.instance.author = self.request.user
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog_detail', kwargs={'arc_slug': self.kwargs.get('arc_slug')})
    

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'  # Имя параметра в URL для идентификатора комментария

    def get_queryset(self):
        """Пользователь может удалять только свои комментарии."""
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)
    
    def get_success_url(self):
        """После удаления возвращаем пользователя к статье."""
        product_slug = self.request.POST.get('arc_slug')
        return reverse_lazy('catalog_detail', kwargs={'arc_slug': product_slug})
    
    def dispatch(self, request, *args, **kwargs):
        """Переопределение dispatch для проверки владельца комментария."""
        comment = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if comment.author != request.user:
            raise PermissionDenied("Вы не можете удалить этот комментарий.")
        return super().dispatch(request, *args, **kwargs)
    

