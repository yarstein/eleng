from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.core.cache import cache


from .models import Slider, OurServices, AboutCompany, Vacancy
from .forms import ResumeForm, FeedbackForm
from .utils import get_client_ip



def index(request):
    sliders = cache.get('slide')
    if not sliders:
        sliders = Slider.objects.all()
        cache.set('slide', sliders, timeout=3600)

    sirvices = cache.get('ourservices_part1')
    if not sirvices:
        sirvices = OurServices.objects.only('pk', 'title', 'summary', 'summary_image')
        cache.set('ourservices_part1', sirvices, 3600)
        
    data = {
        'sliders': sliders,
        'title': 'Главная страница',
        'services': sirvices,
    }
    return render(request, 'project/index.html', context=data)


def product(request):
    # попытка получить из кеша:
    sirvices = cache.get('ourservices_part2')
    if not sirvices:
        sirvices = OurServices.objects.only('pk', 'title', 'content', 'content_image')
        cache.set('ourservices_part2', sirvices, timeout=3600)

    data = {
        'sirvices': sirvices,
        'title': 'Наши услуги'
    }
    return render(request, 'project/products.html', context=data)


def aboutcompany(request):
    content = AboutCompany.objects.first()
    data = {
        'content': content,
        'title': 'О компании'
    }
    return render(request, 'project/aboutcompany.html', context=data)


class VacancyView(View):
    form_class = ResumeForm
    template_name = 'project/vacancy.html'

    def get_initial(self):
        """
        Если пользователь авторизован, возвращаем его данные как начальные значения для формы.
        """
        initial = {}
        if self.request.user.is_authenticated:
            user = self.request.user
            initial['first_name'] = user.first_name
            initial['last_name'] = user.last_name
            initial['email'] = user.email
        return initial
    

    def get(self, request, *args, **kwargs):
        # Пытаемся получить кешированный список вакансий
        content = cache.get('vacancies')
        if not content:
            content = Vacancy.objects.all()
            cache.set('vacancies', content, timeout=3600)  # Кешируем на час

        initial = self.get_initial()

        # Передаем объект request в форму
        form = self.form_class(initial=initial, request=request)
        return render(request, self.template_name, {'content': content, 'form': form, 'title': 'Карьера'})
    

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, request=request)
        if form.is_valid():
            resume = form.save(commit=False)
            if request.user.is_authenticated:
                resume.user = request.user
            resume.save()
            messages.success(request, 'Ваше резюме успешно отправлено!')
            return redirect('vacancy')
        else:
            content = Vacancy.objects.all()
            initial = self.get_initial()
            messages.error(request, 'Ошибка заполнения формы. Пожалуйста введите корректные данные!')
            return render(request, self.template_name, {'content': content, 'form': form, 'title': 'Карьера', 'initial': initial})
        

class ContactView(FormView):
    form_class = FeedbackForm
    template_name = 'project/contact.html'
    success_url = reverse_lazy('contact')
    extra_context = {
        'title': 'Контакты',
    }


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.is_authenticated:
            # Если пользователь авторизован, удаляем поле капчи
            del form.fields['captcha']
        return form

    def form_valid(self, form):
        """Если форма валидна, вызывается этот метод для FormView"""

        feedback  = form.save(commit=False)
        feedback.ip_address = get_client_ip(self.request)
        if self.request.user.is_authenticated:
            feedback.user = self.request.user
        feedback.save()
        messages.success(self.request, 'Ваше сообщение успешно отправлено!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Есть ли ошибка в капче?
        if 'captcha' in form.errors:
            messages.error(self.request, 'Неверный ответ капчи. Пожалуйста, попробуйте снова.')
        # Возвращаем пользователя на страницу с формой, передавая ему текущую невалидную форму
        return self.render_to_response(self.get_context_data(form=form))