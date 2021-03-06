from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles import finders
from django import template
from django.test import Client
from django.contrib.auth.models import User
from django.contrib import auth

class GeneralTests(TestCase):
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	def test_index_page_exists(self):
		response = self.client.get(reverse('main:index'))
		if(response.content == b""):
			self.fail("index page contains no content!")
	
	def test_templates_are_served(self):
		try:
			template.loader.get_template("main/test.html")	
		except:
			self.fail("could not find templates/main/test.html template, are you sure templates are being served?, maybe someone deleted the file...")

	def test_static_files_are_served(self):
		result = finders.find('images/test.jpg')
		if(result == None):
			self.fail("could not get images/test.jpg static file, are you they are served, or someone deleted the file?")

class ViewsTests(TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass


	def test_index_page_exists(self):
		response = self.client.get(reverse('main:index'))


	def test_hotrestaurants_page_exists(self):
		response = self.client.get(reverse('main:hotrestaurants'))

	def test_registersignin_page_exists(self):
		response = self.client.get(reverse('main:registersignin'))

	def test_randomrecipes_page_exists(self):
		response = self.client.get(reverse('main:randomrecipes'))

	def test_myrecipes_page_exists(self):
		response = self.client.get(reverse('main:myrecipes'))

	def test_myplaces_page_exists(self):
		response = self.client.get(reverse('main:myplaces'))


class LoginRegisterTests(TestCase):
	def setUp(self):
		#Create a test account if it doesn't exist
		try:
			u = User.objects.get(username="test")
			#This code breaks if the user doesn't exist 
			u.set_password('test')
			u.save()
		except:	
			u=User(username="test")
			u.save()
			u.set_password('test')
			u.save()
	
	def tearDown(self):
		try:
			u = User.objects.get(username = "test")
			u.delete()
		except:
			pass
	
	def test_registersignin_page_normal_login_redirects_to_index_view(self):
		#if you've logged in correctly ie used correct details, the page should take you back to index page
		c = Client()
		response = c.post("/registersignin/",{"signinusername":"test","signinpassword":"test"})
		self.assertEqual(response.url,"/")	
		
	def test_registersignin_page_succesfully_logs_you_in(self):
		c = Client()
		user = auth.get_user(c)
		assert (not user.is_authenticated)
		response = c.post("/registersignin/",{"signinusername":"test","signinpassword":"test"})
		user = auth.get_user(c)
		assert user.is_authenticated
	
	def test_registersignin_page_doesnt_log_you_in_with_incorrect_details(self):
		c = Client()
		user = auth.get_user(c)
		assert (not user.is_authenticated)
		response = c.post("/registersignin/",{"signinusername":"test","signinpassword":"wrongpassword"})
		user = auth.get_user(c)
		assert (not user.is_authenticated)

	def test_registersignin_page_register_only_works_on_new_username(self):
		c = Client()
		user = auth.get_user(c)
		assert (not user.is_authenticated)
		response = c.post("/registersignin/",{"signinusername":"test","signinpassword":"new_password"})
		user = auth.get_user(c)
		assert (not user.is_authenticated)

	def test_registersignin_page_register_creates_new_user_and_sign_you_in(self):
		c = Client()
		user = auth.get_user(c)
		a = (not user.is_authenticated)
		response = c.post("/registersignin/",{"registerusername":"test2","registerpassword":"test"})
		user = auth.get_user(c)
		b = user.is_authenticated
		c = (user.username == "test2")
		u = User.objects.get(username = "test2")
		u.delete()
		assert a
		assert b
		assert c
		
	def test_signout_page_succesfully_logs_out(self):
		c = Client()
		user = auth.get_user(c)
		assert (not user.is_authenticated)
		response = c.post("/registersignin/",{"signinusername":"test","signinpassword":"test"})
		user = auth.get_user(c)
		assert user.is_authenticated
		c.get("/signout/")
		user = auth.get_user(c)
		assert not user.is_authenticated	

	def test_registersignin_page_has_empty_string_as_default_location(self):
		c = Client()
		response = c.post("/registersignin/",{"registerusername":"test2","registerpassword":"test"})
		user = auth.get_user(c)
		a = (user.userinfo.location == "")	
		u = User.objects.get(username = "test2")
		u.delete()
		assert a


class RandomRecipeTests(TestCase):
        
        def setUp(self):
                pass

        def tearDown(self):
                pass

        def test_user_loggedin_url_saving_works(self):
                #add click on recipes to saved ones of user
                pass

        def test_url_dont_repeat(self):
                response1 = self.client.get('/randomrecipes/')
                response2 = self.client.get('/randomrecipes/')
                assert(response1 != response2)

        def test_url_redirect_to_recipe(self):
                #c = Client()
                #response = c.post('/randomrecipes/')
                #self.assertEqual(response.url,fetch_redirect_response=True)
                pass


def CreateUser(username = "test",password = "test"):
	try:
		u = User.objects.get(username=username)
		#This code breaks if the user doesn't exist 
		u.set_password(password)
		u.save()
		
	except:	
		u=User(username=username)
		u.save()
		u.set_password(password)
		u.save()
	finally:
		return u
	
def DeleteUser(user):
	user.delete()

from main.models import UserInfo
class HotRestaurantTests(TestCase):
	def setUp(self):
		#Create a test account if it doesn't exist
		try:
			u = User.objects.get(username="test")
			#This code breaks if the user doesn't exist 
			u.set_password('test')
			u.save()
			
		except:	
			u=User(username="test")
			u.save()
			u.set_password('test')
			u.save()
		finally:
			info = UserInfo(user = u,location = "test")
			info.save()
	
	def tearDown(self):
		try:
			u = User.objects.get(username = "test")
			u.delete()
		except:
			pass
	
	def test_hotrestaurants_returns_restaurant_information_always(self):
		c = Client()
		c.login(username="test",password="test")
		response = c.get("/hotrestaurants/")
		assert (len(response.context["restaurants"]) > 1)
		u = CreateUser(username = "test2",password="test")		
		info = UserInfo(user = u, location = "G128NU")
		c.login(username="test2",password="test")
		response = c.get("/hotrestaurants/")
		assert (len(response.context["restaurants"]) > 1)
		c.logout()	
		response = c.get("/hotrestaurants/")
		assert (len(response.context["restaurants"]) > 1)
		












