import uuid

from app.web.utils import json_response
from aiohttp.web_exceptions import HTTPNotFound
from app.web.app import View
from app.crm.models import User

from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema
from app.crm.schemas import ListUsersResponseSchema, UserGetRequestSchema, UserGetResponseSchema, UserAddSchema
from app.web.schemas import OkResponseSchema


class AddUserView(View):
    @docs(tags=['crm'], summary='Add user', description='Add new user to the database')
    @request_schema(UserAddSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        # Изначально было так: data = await self.request.json()
        # Но мы добавили валидацию, поэтому можно сократить до:
        data = self.request['data']
        user = User(id_=uuid.uuid4(), email=data['email'])
        await self.request.app.crm_accessor.add_user(user)
        return json_response()


class ListUsersView(View):
    @docs(tags=['crm'], summary='List users', description='List all users in the database')
    @response_schema(ListUsersResponseSchema, 200)
    async def get(self):
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [{'email:': user.email,
                      'id': str(user.id_)} for user in users]
        return json_response(data={'users': raw_users})


class GetUserView(View):
    @docs(tags=['crm'], summary='Get user', description='Get user from the database')
    @querystring_schema(UserGetRequestSchema)
    @response_schema(UserGetResponseSchema, 200)
    async def get(self):
        # Чтобы получить информацию из URL, нужно использовать
        # query параметры.
        user_id = self.request.query['id']
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        if user:
            return json_response(data={'user': {'email': user.email, 'id': str(user.id_)}})
        else:
            raise HTTPNotFound
