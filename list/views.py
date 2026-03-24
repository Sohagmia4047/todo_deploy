from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone

from list.models import Category, Todo


def todo_view(request):
    if request.method == "POST":
        todo_id = request.POST.get("todo_id")
        title = (request.POST.get("title") or "").strip()
        image = request.FILES.get("image")
        end_time_str = request.POST.get("end_time")
        category_name = (request.POST.get("category_name") or "").strip()

        if not title or not end_time_str:
            messages.error(request, "Title and End time are required.")
            return redirect("todo_view")

        try:
            naive_dt = datetime.fromisoformat(end_time_str)
            end_time = timezone.make_aware(naive_dt)
        except ValueError:
            messages.error(request, "Invalid end time format.")
            return redirect("todo_view")

        if todo_id:
            try:
                todo = Todo.objects.get(id=todo_id)
            except Todo.DoesNotExist:
                messages.error(request, "Todo not found.")
                return redirect("todo_view")

            todo.title = title
            todo.end_time = end_time
            if image:
                todo.image = image
            todo.save()

            # পুরানো category delete করে নতুনটা set
            todo.categories.all().delete()
            if category_name:
                Category.objects.create(todo=todo, category_name=category_name)

            messages.success(request, "Todo updated successfully.")
        else:
            todo = Todo.objects.create(
                title=title,
                end_time=end_time,
                image=image
            )

            if category_name:
                Category.objects.create(todo=todo, category_name=category_name)

            messages.success(request, "Todo added successfully.")

        return redirect("todo_view")

    query = (request.GET.get("q") or "").strip()
    category = (request.GET.get("category") or "").strip()

    qs = Todo.objects.all().prefetch_related("categories").order_by("-created_at")
    all_categories = Category.objects.values_list("category_name", flat=True).distinct()

    if query:
        qs = qs.filter(title__icontains=query)

    if category:
        qs = qs.filter(categories__category_name__icontains=category).distinct()

    paginator = Paginator(qs, 6)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "todo.html", {
        "all_todo": page_obj,
        "query": query,
        "category": category,
        "all_categories": all_categories,
    })


def done_view(request, task_id):
    try:
        todo = Todo.objects.get(id=task_id)
        todo.done = True
        todo.save()
        messages.success(request, "Task completed successfully.")
        return redirect("todo_view")
    except Todo.DoesNotExist:
        return HttpResponse("Undefined Task")


def delete_view(request, task_id):
    try:
        todo = Todo.objects.get(pk=task_id)
    except Todo.DoesNotExist:
        messages.error(request, "Task not found.")
        return redirect("todo_view")

    todo.delete()
    messages.success(request, "Task deleted successfully.")
    return redirect("todo_view")