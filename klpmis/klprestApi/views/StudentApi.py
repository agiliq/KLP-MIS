"""
StudentApi is used
1) To view Individual Student details.
2) To create new Student
3) To update existing Student
4) To call bulk create/edit students form
5) To delete selected students
"""
from django.http import HttpResponse
from django.shortcuts import render

from schools.models import Student, StudentGroup, Institution, Child
from schools.forms import Child_Form
from vendor.django_restapi.model_resource import Collection
from vendor.django_restapi.responder import TemplateResponder
from vendor.django_restapi.receiver import XMLReceiver
from klprestApi.views.BoundaryApi import ChoiceEntry
from schools.receivers import KLP_user_Perm


class KLP_Student(Collection):

    def get_entry(self, student_id):
        # Query For Selected Student based on student_id
        Students = Student.objects.get(id=student_id)
        return ChoiceEntry(self, Students)


def KLP_Student_Create(request, studentgroup_id, counter=0):
    """ To Create New Student
        boundary/(?P<bounday>\d+)/schools/(?P<school>\d+)/class/creator/"""
    # Checking user Permissions for Student add

    KLP_user_Perm(request.user, "Student", "Add")

    buttonType = request.POST.get('form-buttonType')
    model = StudentGroup.objects.get(id=studentgroup_id)
    mapStudent = request.GET.get(
        'map_Student') or request.POST.get('mapStudent') or 0
    assessment_id = request.GET.get(
        'assessment_id') or request.POST.get('assessment_id') or 0
    referKey = Institution.objects.get(id=model.institution.id).boundary.id
    # before Child.objects.all()
    queryset = Child.objects.filter(pk=0)

    KLP_Create_Student = KLP_Student(
        queryset,
        permitted_methods=('GET', 'POST'),
        responder = TemplateResponder(
            template_dir='viewtemplates',
            template_object_name='child',
            extra_context={
                'buttonType': buttonType,
                'referKey': referKey,
                "studentgroup_id": studentgroup_id,
                'studentgroup': model,
                'modelName': "student",
                "mapStudent": mapStudent,
                'assessment_id': assessment_id,
                'counter': counter}),
        receiver = XMLReceiver(
        ),
    )
    response = KLP_Create_Student.responder.create_form(
        request,
        form_class=Child_Form)
    return HttpResponse(response)


def KLP_Student_Call(request, studentgroup_id):
    """ To show Bulk Students to create"""
    context = {'studentgroup_id': studentgroup_id, 'totStudents': range(10)}
    return (
        render(request,
            'viewtemplates/student_form.html', context)
    )


def KLP_Student_Edit_Call(request, studentgroup_id):
    """ To show Bulk Students to update """
    studentList = request.GET.getlist("students")
    context = {'studentgroup_id': studentgroup_id,
               'studentList': studentList}
    return (
        render(request,
               'edittemplates/student_form.html', context)
    )


def KLP_Student_View(request, student_id):
    """ To View Selected Student
            studentsroup/(?P<studentsroup_id>\d+)/view/?$"""
    kwrg = {'is_entry': True}
    # before Student.objects.all()
    resp = KLP_Student(
        queryset=Student.objects.filter(pk=student_id),
        permitted_methods=('GET',
                           'POST'),
        responder = TemplateResponder(template_dir='viewtemplates',
                                      template_object_name=
                                      'student', ), )(request, student_id,
                                                      **kwrg)
    return HttpResponse(resp)


def KLP_Student_Update(request, student_id, counter=0):
    """ To update Selected student student/(?P<student_id>\d+)/update/"""
    # Checking user Permissions for Student update
    KLP_user_Perm(request.user, "Student", "Update")
    buttonType = request.POST.get('form-buttonType')
    # before Child.objects.all()
    KLP_Edit_Student = KLP_Student(
        queryset=Child.objects.filter(pk=student_id),
        permitted_methods=('GET',
                           'POST'),
        responder = TemplateResponder(template_dir='edittemplates',
                                      template_object_name='child',
                                      extra_context={
                                          'buttonType': buttonType,
                                          'modelName': "student",
                                          'counter': counter}),
        receiver = XMLReceiver(), )
    response = KLP_Edit_Student.responder.update_form(
        request,
        pk=student_id,
        form_class=Child_Form)

    return HttpResponse(response)


def KLP_DeleteStudnet(request, id):
    """ To delete selected Students"""
    # get all selected students
    students_list = request.POST.getlist("students")
    respStr = {}
    count = 0
    delFailed = ''
    if len(students_list) > 0:
        for stud_id in students_list:
            # get Student Object to delete
            obj = Student.objects.get(child__id=stud_id)
            sgobj = StudentGroup.objects.filter(
                id=id, group_type='Class').count()
            if 1:
                from django.db import connection
                cursor = connection.cursor()
                q1 = """ insert into schools_student_0(id,
                    child_id, other_student_id, active)
                    select id, child_id, other_student_id, 0
                    from schools_student_2 where id = %d """ % (obj.id)

                q2 = """insert into schools_student_studentgrouprelation_0(
                        id,student_id, student_group_id, academic_id, active)
                        select id,
                        student_id, student_group_id, academic_id, 0
                        from schools_student_studentgrouprelation_2
                        where student_id = %d
                        and student_group_id = %d """ % (obj.id, int(id))

                q3 = """ delete from schools_student_studentgrouprelation_2
                    where student_id = %d and student_group_id = %d """ % (
                    obj.id, int(id))

                q4 = """ delete from schools_student_2 where id = %d """ % (
                    obj.id)
                if sgobj >= 1:
                    cursor.execute(q1)
                cursor.execute(q2)
                cursor.execute(q3)
                if sgobj >= 1:
                    cursor.execute(q4)

                delFailed += obj.child.first_name + " " + obj.child.last_name
            else:
                return (
                    HttpResponse("Students " + delFailed +
                                 " Deletion Failed")
                )

        return (
            HttpResponse(
                "All Selected Students has been deleted successfully")
        )
    else:
        return HttpResponse("Please select students to delete")
