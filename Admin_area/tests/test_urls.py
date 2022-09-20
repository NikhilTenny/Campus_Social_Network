from django.test import SimpleTestCase
from django.urls import resolve, reverse

from Admin_area import views


class Test_urls(SimpleTestCase):

    def test_adminhome_url(self):
        url = reverse('admin-dashboard')

        self.assertEquals(resolve(url).func.view_class, views.AdminHome)

    def test_NoticeBoard_url(self):
        url = reverse('admin-NB')

        self.assertEquals(resolve(url).func.view_class, views.NoticeBoardView)
    
    def test_TimelineView_url(self):
        url = reverse('admin-TL')

        self.assertEquals(resolve(url).func.view_class, views.TimelineView)

    def test_PlacementView_url(self):
        url = reverse('admin-PM')

        self.assertEquals(resolve(url).func.view_class, views.PlacementView)
    
    def test_PostDetailView_url(self):
        slug = "temp-post"
        url = reverse('adminpostview', args=[slug])

        self.assertEquals(resolve(url).func.view_class, views.PostDetailView)

    def test_PostEditView_url(self):
        slug = "temp-post"
        url = reverse('adminpostedit', args=[slug])

        self.assertEquals(resolve(url).func.view_class, views.PostEditView)
        
    def test_PostDeleteView_url(self):
        slug = "temp-post"
        url = reverse('adminpostdelete', args=[slug])

        self.assertEquals(resolve(url).func.view_class, views.PostDeleteView)
        
    def test_StudentCreateview_url(self):
        url = reverse('sturegister')

        self.assertEquals(resolve(url).func, views.StudentCreateview)   

    def test_TeacherCreateView_url(self):
        url = reverse('teacherregister')

        self.assertEquals(resolve(url).func, views.TeacherCreateView)   
        

    def test_StudentListView_url(self):
        url = reverse('stulist')

        self.assertEquals(resolve(url).func.view_class, views.StudentListView)   

    def test_TeacherListView_url(self):
        url = reverse('teacherlist')

        self.assertEquals(resolve(url).func.view_class, views.TeacherListView)   
        

    def test_UserDeleteView_url(self):
        username = 'tempuser'
        url = reverse('userdelete', args=[username])

        self.assertEquals(resolve(url).func, views.UserDeleteView) 
        
    def test_CreateNoticeView_url(self):
        url = reverse('admincreateNotice')

        self.assertEquals(resolve(url).func.view_class, views.CreateNoticeView)   
        
    def test_CreatePlacementView_url(self):
        url = reverse('admincreatePlacement')

        self.assertEquals(resolve(url).func.view_class, views.CreatePlacementView)  
        
    def test_Dis_roomsView_url(self):
        url = reverse('admin_dis_rooms')

        self.assertEquals(resolve(url).func.view_class, views.Dis_roomsView)  
    
    def test_EditDis_roomView_url(self):
        room_id = '3'
        url = reverse('admin_edit_dis_room', args=[room_id])

        self.assertEquals(resolve(url).func, views.EditDis_roomView) 
        
    def test_RemMemberView_url(self):
        room_id = '3'
        username = 'tempuser'
        url = reverse('rem_member', args=[room_id, username])

        self.assertEquals(resolve(url).func, views.RemMemberView) 

    
    def test_AddMemberlist_url(self):
        room_id = '3'
        url = reverse('memberstoadd', args=[room_id])

        self.assertEquals(resolve(url).func, views.AddMemberlist)
    
    def test_RemoveRoomView_url(self):
        room_id = '3'
        url = reverse('removeroom', args=[room_id])

        self.assertEquals(resolve(url).func, views.RemoveRoomView)   
    
    def test_AdminProfileView_url(self):
        room_id = '3'
        url = reverse('adminprofile', args=[room_id])

        self.assertEquals(resolve(url).func, views.AdminProfileView)  

    def test_EditAdminProfileView_url(self):
        room_id = '3'
        url = reverse('adminprofileedit', args=[room_id])

        self.assertEquals(resolve(url).func, views.EditAdminProfileView)  








