import json

from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy

from hm28 import settings
from users.models import User
from .models import Ad, Category


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    def get(self, request, **kwargs):
        # ads = Ad.objects.all().order_by("-price")
        ads = Ad.objects.all().order_by("-price").select_related('author')

        paginator = Paginator(ads, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        ads_page = paginator.get_page(page_number)

        ads_list = []
        for ad in ads_page:
            ads_list.append({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "author": ad.author.username,
                "price": float(ad.price),
                "description": ad.description,
                "is_published": ad.is_published,
                "category_id": ad.category_id,
                "image": ad.image.url if ad.image else None,
            })
        average_price = ads.aggregate(Avg('price'))
        response = {
            "items": ads_list,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
            "average_price": round(float(average_price.get('price__avg', 0)), 1)
        }
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Http404:
            return JsonResponse({"message": "Данного товара не существует"}, status=404)

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.username,
            "price": float(ad.price),
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category', 'image']

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        ad = Ad.objects.create(
            name=ad_data["name"],
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            category_id=ad_data["category"]
        )

        ad.author = get_object_or_404(User, pk=ad_data["author"])

        if "image" in ad_data:
            ad.image = ad_data["image"]
        ad.save()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.username,
            "price": float(ad.price),
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'price', 'description', 'is_published', 'image', 'category']

    def patch(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        self.object.name = ad_data["name"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.is_published = ad_data["is_published"]
        self.object.category_id = ad_data["category"]

        if "image" in ad_data:
            self.object.image = ad_data["image"]

        self.object.save()

        data = {
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.username,
            "price": float(self.object.price),
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        }
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = reverse_lazy('ads')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, request, **kwargs):
        categories = Category.objects.all().order_by("name")
        response = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name,
            })
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data["name"]
        )

        data = {
            "id": category.id,
            "name": category.name,
        }
        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    model = Ad
    fields = ["name", "image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "image": self.object.image.url if self.object.image else None
        })

