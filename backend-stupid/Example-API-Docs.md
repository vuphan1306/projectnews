
APIs:
api_url = "https://docker-machine-ip/api/v1”
############################################################
Authentication:
{
  Sign_up: POST api_url/authentication/sign_up/
    Request params:
    {
      "email": "abc@gmail.com",
      "password": "123456",
      "retype_password": "123456",
      "first_name": "abc",
      "last_name": "xyz"
    }

    Response:
    {
      "user": {
        "api_key": "0c89daddb0e6a3b872f57b40af1241a89bca2c95",
        "email": "abcde@gmail.com",
        "first_name": "abc",
        "id": 4,
        "last_name": "xyz"
      }
    }

  Sign_in: POST api_url/authentication/sign_in/
    Request params:
    {
      "email": "abc@gmail.com",
      "password": "123456"
    }

    Response:
    {
      "user": {
        "access_token": "fff20435-14a9-4f28-92c5-263fa309c2fd",
        "api_key": "f3ef957b7b9c4f22c8797870921284278cf60c10",
        "email": "abc@gmail.com",
        "first_name": "abc",
        "id": 1,
        "last_name": "xyz"
      }
    }

  Get user info: POST: api_urp/authentication/getuserinfo/
    Require Authorization header: access_token
    Response: 
    {
      "user": {
        "first_name": "abc",
        "id": 10,
        "is_seller": false,
        "last_name": "xyz"
      }
    }

  Sign_out: POST api_url/authentication/sign_out/
    Require Authorization header: access_token
    Response: 
    {
      "success”: True
    }

  Login by social account: POST api_url/authentication/loginsocial/
    Request params:
    {
      "email": "nguyenminhlong5@gmail.com",
      "first_name": "nguyen",
      "last_name": "minh long ",
      "image":"",
      "account_id": "",
      "account_key": "",
      "account_secret": "",
      "request_permission": "",
      "login_type": "FACEBOOK",
      "linked_user_id": "rwrd3334tdgsdfw34545gdfwrfsd",
      "access_token": "",
      "granted_permissions": ""
    }
    Response: 
    {
      "user": {
        "access_token": "f8f8314c-3e73-461d-8143-9972062426ba",
        "api_key": "1a973c12e77bf78383913cf5960ec394d95be4f2",
        "email": "nguyenminhlong5@gmail.com",
        "first_name": "nguyen",
        "id": 22,
        "last_name": "minh long"
    }
  
  
}

##########################################################

Category
{
  Create_category: POST: api_url/category/create/
    Request params: Authorization: access_token.
      {
        "name": "Danh muc thu 100",
        "description": "DM 100"
      }
    Response:
      {
        "Success": true
      }

  Update category: POST: api_url/category/update/
    Request params: Authorization: access_token.
      {
        "id": 1,
        name": "Danh muc update"
      }
    Response:
      {
        "Update success": true
      }

  Delete category: DELETE: api_url/category/delete/
   Request params: Authorization: access_token.
      {
        "id": 1
      }
    Response:
      {
        "deleted": 1,
        "success": true
      }

  Get category: GET: api_url/category/get_all/
   Request params:
      None
    Response:
      {
        "objects": [
          {
            "display_order": 0,
            "id": 2,
            "name": "Danh muc thu nhat",
            "status_code": 1
          },
          {
            "display_order": 0,
            "id": 3,
            "name": "Danh muc thu hai",
            "status_code": 1
          },
          {
            "display_order": 0,
            "id": 4,
            "name": "Danh muc thu 10",
            "status_code": 1
          },
          {
            "display_order": 0,
            "id": 9,
            "name": "Danh muc update",
            "status_code": 1
          },
          {
            "display_order": 0,
            "id": 10,
            "name": "Danh muc update",
            "status_code": 1
          },
          {
            "display_order": 0,
            "id": 1,
            "name": "Danh muc update",
            "status_code": 1
          }
        ]
      }
}

#####################################################################3

Article
{
  Create_article: POST: api_url/article/create/
    Request params: Authorization: access_token.
      {
            "title": "Day la title2",
            "content": "Noi dung bai viet 2",
            "description": "abc",
            "category_id": 3
      }
    Response:
      {
        "Success": true
      }

  Update article: POST: api_url/article/update/
    Request params: Authorization: access_token.
      {
        "id": 1,
        "title": "Day la title update",
        "content": "Noi dung bai viet update",
        "description": "abc",
        "category_id": 3
      }
    Response:
      {
        "Update success": true
      }

  Delete article: DELETE: api_url/article/delete/
   Request params: Authorization: access_token.
      {
        "id": 2
      }
    Response:
      {
        "deleted": 1,
        "success": true
      }

  Get article: GET: api_url/article/get_all/
   Request params:
      None
    Response:
      {
        "objects": [
          {
            "category_id": 3,
            "content": "Noi dung bai viet 2",
            "create_by_id": 7,
            "description": "abc",
            "display_order": 0,
            "id": 2,
            "status_code": 1,
            "title": "Day la title2"
          },
          {
            "category_id": 3,
            "content": "Noi dung bai viet update",
            "create_by_id": 7,
            "description": "abc",
            "display_order": 0,
            "id": 1,
            "status_code": 1,
            "title": "Day la title update"
          }
        ]
      }
  Add a comment to a Article: POST: api_url/article/add_comment/
    Request params: Need header Authorization: access_token.
    Request params:
    {
      "article_id": 1,
      "text": "ghiklmn"
    }
    Response:
    {
      "created": "2016-11-13T09:05:34.790648",
      "id": 26,
      "text": "ghiklmn",
      "user": {
        "id": 7,
        "name": "abc xyz",
        "user_avatar": ""
      }
    }
}

#################################################################

Comment
{
  Get all comments of a question: GET: api_url/comment/get_article_comments/?id=1
  or GET: api_url/comment/get_article_comments/?id=1&limit=5&page=1
    Request params: None
    Response:
    {
      {
        "meta": {
          "limit": 20,
          "next": null,
          "offset": 0,
          "previous": null,
          "total_count": 15
        },
        "objects": [
          {
            "created": "2016-11-13T09:05:34.790648",
            "id": 26,
            "text": "ghiklmn",
            "user": {
              "id": 7,
              "name": "abc xyz",
              "user_avatar": ""
            }
          },
          {
            "created": "2016-11-12T22:19:31.073149",
            "id": 19,
            "text": "ban choi game hay quassssssssssssssssssssssssssssssss!!!",
            "user": {
              "id": 7,
              "name": "abc xyz",
              "user_avatar": ""
            }
          },
          {
            "created": "2016-11-12T22:17:39.011095",
            "id": 17,
            "text": "ban choi game hay quassssssssssssssssssssssssssssssss!!!",
            "user": {
              "id": 7,
              "name": "abc xyz",
              "user_avatar": ""
            }
          },
          {
            "created": "2016-11-12T21:38:19.140257",
            "id": 11,
            "text": "Noi dung comment",
            "user": {
              "id": 7,
              "name": "abc xyz",
              "user_avatar": ""
            }
          }
        ]
      }
    }

  Update comment: POST: api_url/comment/update_comment/
    Request params: Authorization: access_token.
      {
        "comment_id": 14,
        "text": "1234424234"
      }
    Response:
    {
      "created": "2016-11-12T21:56:19.284972",
      "id": 14,
      "text": "1234424234",
      "user": {
        "id": 7,
        "name": "abc xyz",
        "user_avatar": ""
      }
    }

  Delete comment: DELETE: api_url/comment/delete_comment/
   Request params: Authorization: access_token.
      {
        "comment_id": 14
      }
    Response:
      {
        "Success": true
      }


}