"""
StudentApi is used 
1) To view Individual Student details.
2) To create new Student
3) To update existing Student
4) To call bulk create/edit students form
5) To delete selected students
"""
from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry
from django.contrib.contenttypes.models import ContentType

from schools.signals import check_user_perm
from schools.receivers import KLP_user_Perm

class KLP_Student(Collection):    
    def get_entry(self, student_id):        
    	# Query For Selected Student based on student_id
        Students = Student.objects.get(id=student_id)          
        return ChoiceEntry(self,Students )

def KLP_Student_Create(request, studentgroup_id, counter=0):
	""" To Create New Student boundary/(?P<bounday>\d+)/schools/(?P<school>\d+)/class/creator/"""
	# Checking user Permissions for Student add
	check_user_perm.send(sender=None, user=request.user, model='Student', operation='Add')
        check_user_perm.connect(KLP_user_Perm)
	buttonType = request.POST.get('form-buttonType')
	model = StudentGroup.objects.get(id=studentgroup_id)
	mapStudent = request.GET.get('map_Student') or request.POST.get('mapStudent') or 0
	assessment_id = request.GET.get('assessment_id') or request.POST.get('assessment_id') or 0
	referKey = Institution.objects.get(id = model.institution.id).boundary.id
        queryset = Child.objects.all() 
        KLP_Create_Student = KLP_Student(queryset , permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'child', extra_context={'buttonType':buttonType, 'referKey':referKey,"studentgroup_id":studentgroup_id, 'studentgroup':model, 'modelName':"student", "mapStudent":mapStudent, 'assessment_id':assessment_id, 'counter':counter}), receiver = XMLReceiver(),)
        response = KLP_Create_Student.responder.create_form(request,form_class=Child_Form)
        return HttpResponse(response)

def KLP_Student_Call(request, studentgroup_id):
	""" To show Bulk Students to create"""
	return render_to_response('viewtemplates/student_form.html',{'studentgroup_id':studentgroup_id, 'totStudents':range(10)})        
	

def KLP_Student_Edit_Call(request, studentgroup_id):
	""" To show Bulk Students to update """
	studentList = request.GET.getlist("students")
	return render_to_response('edittemplates/student_form.html',{'studentgroup_id':studentgroup_id, 'studentList':studentList})	
	
def KLP_Student_View(request, student_id):
	""" To View Selected Student studentsroup/(?P<studentsroup_id>\d+)/view/?$"""
	kwrg = {'is_entry':True}
	resp=KLP_Student(queryset = Student.objects.all(), permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'student',),)(request, student_id, **kwrg)
        return HttpResponse(resp)

def KLP_Student_Update(request, student_id, counter=0):
	""" To update Selected student student/(?P<student_id>\d+)/update/"""
	# Checking user Permissions for Student update
	check_user_perm.send(sender=None, user=request.user, model='Student', operation='Update')
        check_user_perm.connect(KLP_user_Perm)
	buttonType = request.POST.get('form-buttonType')
	KLP_Edit_Student =KLP_Student(queryset = Child.objects.all(), permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'edittemplates', template_object_name = 'child',extra_context={'buttonType':buttonType,'modelName':"student", 'counter':counter} ), receiver = XMLReceiver(),)
	response = KLP_Edit_Student.responder.update_form(request, pk=student_id, form_class=Child_Form)
	
	return HttpResponse(response)
	
def KLP_DeleteStudnet(request, id):
	""" To delete selected Students"""
	students_list = request.POST.getlist("students")  # get all selected students
	respStr = {}
	count = 0 
	delFailed = '' 
	if len(students_list) > 0:
		for stud_id in students_list:
			# get Student Object to delete
			obj = Student.objects.get(child__id=stud_id)  
			try:	
				relObjects = Student_StudentGroupRelation.objects.filter(student = obj, academic=current_academic, active=2)
				if relObjects.count() <= 1:
					obj.active = 0
					obj.save()
				sgRelObj = Student_StudentGroupRelation.objects.get(student = obj, student_group__id=id, academic=current_academic, active=2)
				sgRelObj.active = 0
				sgRelObj.save()
				
			except:
				count = count + 1
				delFailed += '%s %s ,'(obj.child.firstName, obj.child.lastName)
				
			
	if count == 0:	 
		return HttpResponse("All Selected Students has been deleted successfully")
	else:	
		return HttpResponse("Studens"+ delFailed+" Deletion Failed")	

urlpatterns = patterns('',    
   url(r'^studentgroup/(?P<studentgroup_id>.*)/student/creator/$', KLP_Student_Create),
   url(r'^studentgroup/(?P<studentgroup_id>.*)/student/creator/(?P<counter>\d+)/$', KLP_Student_Create),
   url(r'^student/(?P<student_id>\d+)/view/?$', KLP_Student_View),
   url(r'^student/(?P<student_id>\d+)/update/?$', KLP_Student_Update),
   url(r'^student/(?P<student_id>\d+)/update/(?P<counter>\d+)/$', KLP_Student_Update),
   url(r'^studentgroup/(?P<studentgroup_id>.*)/student/call/$', KLP_Student_Call), 
   url(r'^deletestudents/(?P<id>\d+)/$', KLP_DeleteStudnet),  
   url(r'^studentgroup/(?P<studentgroup_id>.*)/student/editCall/$', KLP_Student_Edit_Call), 
)
