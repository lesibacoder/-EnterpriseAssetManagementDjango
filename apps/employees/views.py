from django.contrib.auth.decorators import login_required
from django.db.models import Count
# from django.shortcuts import render
from django.shortcuts import (
    render,
    get_object_or_404,
)

from .models import Employee
from .forms import EmployeeForm
from apps.departments.models import Department

from django.http import HttpResponse


# ============================================================
# Employee Index
#
# Displays all employees.
# ============================================================

@login_required
def employee_index(request):

    employees = (
        Employee.objects
        .select_related("department")
        .order_by("employee_number")
    )

    context = {

        # Employee Statistics

        "total_employees": Employee.objects.count(),

        "active_employees": Employee.objects.filter(
            status="ACTIVE"
        ).count(),

        "inactive_employees": Employee.objects.filter(
            status="INACTIVE"
        ).count(),

        "total_departments": Department.objects.count(),

        # Search Filters

        "departments": Department.objects.order_by("name"),

        # Employee Table

        "employees": employees,

    }

    return render(

        request,

        "employees/index.html",

        context,

    )



@login_required
def employee_create(request):

    if request.method == "POST":

        form = EmployeeForm(

            request.POST,

            request.FILES,

        )

        if form.is_valid():

            form.save()

            return redirect("employees")

    else:

        form = EmployeeForm()

    context = {

        "form": form,

        "title": "Add Employee",

    }

    return render(

        request,

        "employees/form.html",

        context,

    )


@login_required
def employee_detail(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk,
    )

    context = {

        "employee": employee,

    }

    return render(
        request,
        "employees/detail.html",
        context,
    )


@login_required
def employee_update(request, pk):

    return HttpResponse(f"Employee Update {pk}")


@login_required
def employee_delete(request, pk):

    return HttpResponse(f"Employee Delete {pk}")