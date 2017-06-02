from django.test import TestCase
from sign.models import Event,Guest
from django.contrib.auth.models import User

# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1,name="oneplus_3_event",status=True,limit=2000,
                             address="中国上海",start_time="2017-4-20 10:30:00")
        Guest.objects.create(id=1,event_id=1,realname="Allen",phone="13232324788",
                             email="Allen@gmail.com",sign=False)

    def test_event_models(self):
        result = Event.objects.get(name="oneplus_3_event")
        self.assertEqual(result.address,"中国上海")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone="13232324788")
        self.assertEqual(result.realname,"Allen")
        self.assertFalse(result.sign)

class IndexPageTest(TestCase):
    """ 测试index登录首页"""
    def test_index_page_renders_index_template(self):
        """ 测试index视图"""
        response = self.client.get('/index/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')

class LoginActionTest(TestCase):
    """ 测试登录动作"""
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123')
    def test_add_admin(self):
        """ 测试添加用户"""
        user = User.objects.get(username = 'admin')
        self.assertEqual(user.username,'admin')
        self.assertEqual(user.email,'admin@mail.com')
    def test_login_action_username_password_null(self):
        """ 用户名密码为空"""
        test_data = {'username':'','password':''}
        response = self.client.post('/login_action/',test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b"username or password error",response.content)
    def test_login_action_success(self):
        """ 登录成功"""
        test_data = {'username':'admin','password':'admin123'}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,302)

class EventManageTest(TestCase):
    """ 发布会管理"""
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123')
        #创建用户
        Event.objects.create(name="Windows10上市发布会",limit=5000,address="美国硅谷",
                             status=1,start_time="2016-1-1 10:00:00")
        #创建发布会事件
        self.login_user = {'username':'admin','password':'admin123'}
        #登录用户信息
    def test_event_manage_success(self):
        """ 测试发布会:Windows10上市发布会"""
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b"Windows10",response.content)
        self.assertIn(b"美国硅谷",response.content)
    def test_event_manage_search_success(self):
        """ 测试发布会搜索"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_name/',{'name':'Windows10'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Windows10", response.content)
        self.assertIn(b"美国硅谷", response.content)

class GuestManageTest(TestCase):
    """ 嘉宾管理"""
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123')
        Event.objects.create(id=1,name="Windows10上市发布会",limit=5000,address="美国硅谷",
                             status=1,start_time="2016-1-1 10:00:00")
        Guest.objects.create(realname='Allen',phone='13323684860',email="Allen@gmail.com",sign=0,event_id=1)
        self.login_user = {'username':'admin','password':'admin123'}
    def test_event_manage_success(self):
        """ 测试嘉宾信息:Allen"""
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b"Allen",response.content)
        self.assertIn(b"13323684860",response.content)

class SignIndexActionTest(TestCase):
    """ 发布会签到"""
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123')
        Event.objects.create(id=1,name="Windows10上市发布会",limit=5000,address="美国硅谷",
                             status=1,start_time="2016-1-1 10:00:00")
        Event.objects.create(id=2, name="iPhone6 Plus", limit=5000, address="China BeiJing",
                             status=1, start_time="2016-9-11 10:00:00")
        Guest.objects.create(realname='小明', phone='10010', email="Ming@gmail.com", sign=1, event_id=1)
        Guest.objects.create(realname='小刚', phone='10000', email="Gang@gmail.com", sign=1, event_id=2)
        self.login_user = {'username': 'admin', 'password': 'admin123'}

    def test_sign_index_action_phone_null(self):
        """ 手机号为空"""
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/1/',{'phone':''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"phone error", response.content)
    def test_sign_index_action_phone_or_event_id_error(self):
        """ 手机号或发布会ID错误"""
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/2/',{'phone':'10000'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"event id or phone error", response.content)
    def test_sign_index_action_user_sign_has(self):
        """用户已签到"""
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/2/',{'phone':'10000'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user has sign in", response.content)
    def test_sign_index_action_sign_success(self):
        """签到成功"""
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/1/',{'phone':'10000'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"sign in success", response.content)
