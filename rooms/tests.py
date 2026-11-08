from rest_framework.test import APITestCase
from . import models
from users.models import User

# Create your tests here.

class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESC = "Amenity Descriptions"

    URL = "/api/v1/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):

        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status code is not 200") #응답 상태 코드가 200인지 확인, 200이 오류 메세지 출력
        self.assertIsInstance(data, list,) # 응답 데이터가 리스트인지 확인
        self.assertEqual(len(data), 1,) # 응답 데이터의 길이가 1인지 확인
        self.assertEqual(data[0]["name"], self.NAME,) 
        self.assertEqual(data[0]["description"], self.DESC,)

    def test_create_amenity(self):

        new_amenity_name = "New Amenity"
        new_amenity_desc = "New Amenity Description"

        response = self.client.post(
            self.URL,
            data = {
                "name": new_amenity_name,
                "description": new_amenity_desc,
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status code is not 200")
        self.assertEqual(data["name"], new_amenity_name,)
        self.assertEqual(data["description"], new_amenity_desc,)

        response = self.client.post(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data) # 응답 데이터에 name 필드가 포함되어 있는지 확인


class TestAmenity(APITestCase):

    NAME = "Test Amenity"
    DESC = "Test Description"
    
    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_found(self):
        response = self.client.get("/api/v1/rooms/amenities/2/")
        self.assertEqual(response.status_code, 404)

    def test_get_amenity(self):
        response = self.client.get("/api/v1/rooms/amenities/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], self.NAME)
        self.assertEqual(data["description"], self.DESC)

    def test_put_amenity(self):

        PUT_NAME = "PUT Test Amenity"
        PUT_DESC = "PUT Test Description"

        response = self.client.put(
            "/api/v1/rooms/amenities/1/",
            data={
                "name": PUT_NAME,
                "description": PUT_DESC,
            },
        )
        self.assertEqual(response.status_code, 200, "Not 200 status code")
        data = response.json()
        self.assertEqual(data["name"], PUT_NAME)
        self.assertEqual(data["description"], PUT_DESC)

    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/rooms/amenities/1/")
        self.assertEqual(response.status_code, 204)


class TestRooms(APITestCase):
    def setUp(self):
        user = User.objects.create(
            username="testuser",
        )
        user.set_password("testpassword")
        user.save()
        self.user = user

    def test_create_room(self):
        response = self.client.post("/api/v1/rooms/")
        self.assertEqual(response.status_code, 403) # 인증되지 않은 사용자가 방을 생성하려고 하면 403 상태 코드 반환
        self.client.force_login(self.user) # 테스트 클라이언트에 로그인된 사용자로 설정
