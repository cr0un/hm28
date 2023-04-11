import json
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from hm28 import settings
from users.models import User, Location


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("username").annotate(total_ads=Count('ad'))

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "location": list(map(str, user.locations.all())),
                "total_ads": user.total_ads,
            })

        response = {
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
        }
        return JsonResponse(response)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except Http404:
            return JsonResponse({"message": "Пользователь не найден"}, status=404)

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "locations": [location.name for location in user.locations.all()],
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'role', 'age', 'locations']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        user_data['password'] = make_password(user_data['password'])

        user = User.objects.create(
            username=user_data["username"],
            password=user_data["password"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            role=user_data["role"],
            age=user_data["age"],
        )

        for location_name in user_data["locations"]:
            location, _ = Location.objects.get_or_create(name=location_name)
            user.locations.add(location)

        user.save()

        response = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "locations": [location.name for location in user.locations.all()],
        }
        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'role', 'age', 'locations']

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_data = json.loads(request.body)

        if 'password' in user_data:
            user_data['password'] = make_password(user_data['password'])

        if 'locations' in user_data:
            locations = user_data.pop('locations')
            self.object.locations.clear()
            for location_name in locations:
                location, _ = Location.objects.get_or_create(name=location_name)
                self.object.locations.add(location)

        for field, value in user_data.items():
            setattr(self.object, field, value)
        self.object.save()

        response = {
            "id": self.object.id,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "locations": [location.name for location in self.object.locations.all()],
        }
        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status": "ok"})


