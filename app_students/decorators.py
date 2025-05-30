from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

class ISStudentUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_student == True
