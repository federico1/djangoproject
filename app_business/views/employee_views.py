from django.views import generic, View
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from app_business.decorators import business_role_required
from app_business.models import BusinessEmployee, BusinessCourses
from students.models import User, Student
from courses.models import Enrollments

import json
import datetime

decorators = [never_cache, login_required, business_role_required]

@method_decorator(decorators, name='dispatch')
class EmployeesTemplateView(generic.TemplateView):
    template_name = 'business_employees/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EmployeesTemplateView, self).get_context_data(
            *args, **kwargs)

        return context

@method_decorator(decorators, name='dispatch')
class EmployeesManageView(View):
    def get(self, request):
        fs = ['id', 'owner', 'student', 'student__first_name', 'student__email',
              'student__last_name', 'student__image', 'student__company_name', 'student__designation', 'created']
        qs = BusinessEmployee.objects.filter(owner=request.user)
        qs = qs.filter(is_deleted=False).values(*fs)
            #Q(is_deleted=False) & Q(owner=request.user)).values(*fs)
        return JsonResponse({"data": list(qs), 'owner':request.user.id}, safe=False)

    def post(self, request, *args, **kwargs):
        try:

            if 'op_delete' in request.POST and 'id' in request.POST:
                employee = BusinessEmployee.objects.get(
                    pk=int(request.POST['id']))
                employee.is_deleted = True
                employee.save()
                return JsonResponse({'result': True, 'error': False})

            if 'op_password' in request.POST and 'user_id' in request.POST:
                user = User.objects.get(pk=int(request.POST['user_id']))
                # user.password = make_password(request.POST['password'])
                user.set_password(request.POST['password'])
                print(user)
                user.save()
                return JsonResponse({'result': True, 'error': False})

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            company_name = request.POST['company_name']
            id = request.POST['id']
            user_id = request.POST['user_id']
            image = request.POST['image']
            designation = request.POST['designation']
            password = request.POST['password'] if 'password' in request.POST else None

            result = False
            user = None

            if user_id and int(user_id) > 0:
                user = User.objects.get(pk=user_id)
                user.is_student = True
                user.is_teacher = False
                user.is_super = False
                user.is_business = False
                user.first_name = first_name
                user.last_name = last_name
                user.company_name = company_name
                user.image = image
                user.designation = designation
                user.email = email
                user.username = email
                user.save()
                result = True
            else:
                user = User.objects.create_user(username=email,
                                                email=email,
                                                password=password)
                user.is_student = True
                user.is_teacher = False
                user.is_super = False
                user.is_business = False
                user.first_name = first_name
                user.last_name = last_name
                user.company_name = company_name
                user.image = image
                user.designation = designation
                user.save()
                student = Student.objects.create(user=user)

            if user and id and int(id) > 0:
                pass
            elif user:
                bs = BusinessEmployee(owner=request.user,
                                      student=user, is_deleted=False)
                bs.save()
                result = True

            return JsonResponse({'result': result, 'error': False})
        except Exception as ex:
            return JsonResponse({'result': None, 'error': True, 'ex': ex})

@method_decorator(decorators, name='dispatch')
class SingleEmployeeManageView(View):
    def get(self, request, id):
        template_name = 'business_employees/details.html'
        business_employee = BusinessEmployee.objects.get(pk=id)
        if business_employee.owner.id != request.user.id:
            return redirect(reverse_lazy('business_employees'))

        context = {'business_employee': business_employee}
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            if 'op_name' in request.POST and request.POST['op_name'] == 'get_student_courses':
                fs = ['id', 'course', 'course__title', 'course__slug',
                      'is_completed', 'completed_date', 'created']
                enrollments = Enrollments.objects.filter(
                    user_id=request.POST['student_id']).values(*fs)
                return JsonResponse({"data": list(enrollments), 'result': True, 'error': False}, safe=False)
            elif 'op_name' in request.POST and request.POST['op_name'] == 'assign_course':

                student_id = request.POST['student_id']
                business_course_id = request.POST['business_course_id']
                course_id = request.POST['course_id']

                Enrollments.objects.create(
                    user_id=student_id, course_id=course_id)

                business_course = BusinessCourses.objects.get(
                    id=business_course_id)
                business_course.is_assigned = True

                history = []

                is_history_valid = bool(
                    business_course.assign_history and business_course.assign_history.strip())

                if is_history_valid:
                    history = json.loads(business_course.assign_history)

                time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                history.append({'employee_id': student_id,
                               'date_created': time_stamp})

                business_course.assign_history = json.dumps(history)
                business_course.save()

                return JsonResponse({'result': True, 'error': False}, safe=False)

        except Exception as ex:
            return JsonResponse({'result': None, 'error': True, 'ex': ex})
