from multiprocessing import context
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import College, Organization, OrgMember, Program, Student
from studentorg.forms import CollegeForm, OrganizationForm, OrgMemberForm, StudentForm, ProgramForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone

class HomePageView (ListView) :
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_students"] = Student.objects.count()
        context["total_organizations"] = Organization.objects.count()
        context["total_programs"] = Program.objects.count()

        today = timezone.now().date()
        count = (
            OrgMember.objects.filter(
                date_joined__year=today.year
            )
            .values("student")
            .distinct()
            .count()
        )

        context["students_joined_this_year"] = count
        return context

# Program Views

class ProgramList (ListView) :
    model = Program
    context_object_name = 'program'
    template_name = 'program_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')       
        if query:
            qs = qs.filter(
                Q(prog_name__icontains=query) |
                Q(college__college_name__icontains=query)
            )
        return qs

    def get_ordering(self):
        allowed = ["prog_name", "college__college_name"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "prog_name"
    
class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_form.html'
    success_url = reverse_lazy('program_list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_form.html'
    success_url = reverse_lazy('program_list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program_list')



# College Views

class CollegeList (ListView) :
    model = College
    context_object_name = 'college'
    template_name = 'college_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')       
        if query:
            qs = qs.filter(
                Q(college_name__icontains=query)
            )
        return qs

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_form.html'
    success_url = reverse_lazy('college_list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_form.html'
    success_url = reverse_lazy('college_list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college_list')


# Student Views

class StudentList(ListView):
    model = Student
    context_object_name = 'student'
    template_name = 'student_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')       
        if query:
            qs = qs.filter(
                Q(lastname__icontains=query) |
                Q(firstname__icontains=query) |
                Q(middlename__icontains=query) |
                Q(program__prog_name__icontains=query) |
                Q(program__college__college_name__icontains=query)
            )
        return qs
    
    def get_ordering(self):
        allowed = ["student_id","lastname", "firstname", "middlename", "program__prog_name", "program__college__college_name"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "lastname"

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('student_list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('student_list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_del.html'
    success_url = reverse_lazy('student_list')


# OrgMember Views

class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'org_members'
    template_name = 'org_members.html'
    paginate_by = 5

    def get_queryset(self): 
        qs = super().get_queryset()
        query = self.request.GET.get('q')       
        if query:
            qs = qs.filter(
                Q(student__lastname__icontains=query) |
                Q(student__firstname__icontains=query) |
                Q(organization__name__icontains=query) |
                Q(date_joined__icontains=query)
            )
        return qs
    
    def get_ordering(self):
        allowed = ["student__lastname", "student__firstname", "organization__name", "date_joined"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "date_joined"

class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'org_member_form.html'
    success_url = reverse_lazy('org_member_list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'org_member_form.html'
    success_url = reverse_lazy('org_member_list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'org_member_del.html'
    success_url = reverse_lazy('org_member_list')


# Organization Views

class OrganizationList (ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5
    ordering = ["college__college_name","name"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')       
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        return qs
    
    def get_ordering(self):
        allowed = ["name", "college__college_name", "description"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "name"

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_form.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_form.html'
    success_url = reverse_lazy('organization-list') 

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

