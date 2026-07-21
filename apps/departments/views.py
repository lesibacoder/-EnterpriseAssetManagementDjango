from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Department

from django.core.paginator import Paginator

from django.contrib import messages
from django.db.models import ProtectedError
from django.db.models.deletion import ProtectedError

from apps.employees.models import Employee


# ==========================================================
# Department List
# ==========================================================


@login_required
def department_index(request):

    search = request.GET.get("search", "")

    departments = Department.objects.all()

    if search:
        departments = departments.filter(
            name__icontains=search
        )

    total_departments = Department.objects.count()

    total_employees = Employee.objects.count()

    active_departments = Department.objects.filter(
        status="ACTIVE"
    ).count()

    inactive_departments = Department.objects.filter(
        status="INACTIVE"
    ).count()

    paginator = Paginator(departments, 10)

    page = request.GET.get("page")

    departments = paginator.get_page(page)

    return render(
        request,
        "departments/index.html",
        {
            "departments": departments,
            "search": search,

            "total_departments": total_departments,
            "total_employees": total_employees,
            "active_departments": active_departments,
            "inactive_departments": inactive_departments,
        },
    )


# ==========================================================
# Department Detail
# ==========================================================

@login_required
def department_detail(request, pk):

    department = get_object_or_404(

        Department,

        pk=pk,

    )

    return render(

        request,

        "departments/detail.html",

        {

            "department": department,

        },

    )


# ==========================================================
# Create Department
# ==========================================================

from django.shortcuts import redirect
from .forms import DepartmentForm


@login_required
def department_create(request):

    if request.method == "POST":

        form = DepartmentForm(
            request.POST,
        )

        if form.is_valid():

            form.save()

            return redirect("department_index")

    else:

        form = DepartmentForm()

    return render(

        request,

        "departments/form.html",

        {

            "form": form,

            "title": "Add Department",

        },

    )


# ==========================================================
# Update Department
# ==========================================================

@login_required
def department_update(request, pk):

    department = get_object_or_404(
        Department,
        pk=pk,
    )

    if request.method == "POST":

        form = DepartmentForm(
            request.POST,
            instance=department,
        )

        if form.is_valid():

            form.save()

            return redirect("department_detail", pk=department.pk)

    else:

        form = DepartmentForm(
            instance=department,
        )

    return render(

        request,

        "departments/form.html",

        {

            "form": form,

            "title": "Edit Department",

        },

    )


# ==========================================================
# Delete Department
# ==========================================================

@login_required
def department_delete(request, pk):

    department = get_object_or_404(
        Department,
        pk=pk,
    )

    if request.method == "POST":

        try:

            department.delete()

            messages.success(
                request,
                "Department deleted successfully."
            )

        except ProtectedError:

            messages.error(
                request,
                "This department cannot be deleted because it has employees or assets assigned to it."
            )

    return redirect("department_index")

# ==========================================================
#Bulk Delete
# ==========================================================

@login_required
def department_bulk_delete(request):

    if request.method == "POST":

        ids = request.POST.getlist("department_ids")

        deleted = 0
        skipped = 0

        for pk in ids:

            try:

                department = Department.objects.get(pk=pk)

                department.delete()

                deleted += 1

            except ProtectedError:

                skipped += 1

            except Department.DoesNotExist:

                pass

        if deleted:

            messages.success(
                request,
                f"{deleted} department(s) deleted successfully."
            )

        if skipped:

            messages.warning(
                request,
                f"{skipped} department(s) could not be deleted because they have employees or assets."
            )

    return redirect("department_index")