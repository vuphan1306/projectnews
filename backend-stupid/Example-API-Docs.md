
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
        "name": "Danh muc thu 100"
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
  Search_article: GET: api_url/article/article_search/?q='abcdef'&limit=5&page=2
    Request params: 
      None
    Response:
      {
        "error": {
          "message": "Sorry, no results on that page.",
          "code": 406
        }
      }
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
  Get top news article: GET: api_url/article/get_top_news_by_category/?id=1&limit=2
    Request params: Need header Authorization: access_token.
    Request params:
      None
    Response:
    {
      "meta": {
        "limit": 1,
        "next": "/api/v1/article/?id=1&offset=1&limit=1",
        "offset": 0,
        "previous": null,
        "total_count": 2
      },
      "objects": [
        {
          "comments": {
            "lastest_comment": {
              "created": "2016-11-13T09:05:34.790648",
              "id": 26,
              "text": "ghiklmn",
              "user": {
                "id": 7,
                "name": "abc xyz",
                "user_avatar": ""
              }
            },
            "total_comments": 15
          },
          "content": "Spectacular new observations of vast pillar-like structures within the Carina Nebula have been made using the MUSE instrument on ESO's Very Large Telescope. The different pillars analysed by an international team seem to be pillars of destruction -- in contrast to the name of the iconic Pillars of Creation in the Eagle Nebula, which are of similar nature.The spires and pillars in the new images of the Carina Nebula are vast clouds of dust and gas within a hub of star formation about 7500 light-years away. The pillars in the nebula were observed by a team led by Anna McLeod, a PhD student at ESO, using the MUSE instrument on ESO's Very Large Telescope.",
          "created": "2016-11-14T08:40:56.492962",
          "date_created": "2016-11-14T08:40:56.493060",
          "date_updated": "2016-11-14T08:40:56.493072",
          "description": "Spectacular new observations of vast pillar-like structures within the Carina Nebula have been made using the MUSE instrument on ESO's Very Large Telescope. The different pillars analysed by an international team seem to be pillars of destruction -- in contrast to the name of the iconic Pillars of Creation in the Eagle Nebula, which are of similar nature.",
          "display_order": 0,
          "id": 5,
          "modified": "2016-11-14T08:40:56.492993",
          "resource_uri": "/api/v1/article/5/",
          "status_code": 1,
          "title": "Pillars of cosmic destruction: Colorful Carina Nebula blasted by brilliant nearby stars",
          "user": 7
        }
      ]
    }
  Get top news article in category: GET: api_url/article/get_top_news/?limit=2&offset=2
    Request params: Need header Authorization: access_token.
    Request params:
      None
    Response:
    {
      "meta": {
        "limit": 2,
        "next": null,
        "offset": 2,
        "previous": "/api/v1/article/?limit=2&offset=0",
        "total_count": 4
      },
      "objects": [
        {
          "comments": {
            "lastest_comment": {
              "created": "2016-11-13T09:05:34.790648",
              "id": 26,
              "text": "ghiklmn",
              "user": {
                "id": 7,
                "name": "abc xyz",
                "user_avatar": ""
              }
            },
            "total_comments": 15
          },
          "content": "Noi dung bai viet moi",
          "created": "2016-11-14T04:26:57.504797",
          "date_created": "2016-11-14T04:26:57.504871",
          "date_updated": "2016-11-14T04:26:57.504882",
          "description": "abc",
          "display_order": 0,
          "id": 3,
          "modified": "2016-11-14T04:26:57.504820",
          "resource_uri": "/api/v1/article/3/",
          "status_code": 1,
          "title": "Day la title2",
          "user": 7
        },
        {
          "comments": {
            "lastest_comment": {
              "created": "2016-11-13T09:05:34.790648",
              "id": 26,
              "text": "ghiklmn",
              "user": {
                "id": 7,
                "name": "abc xyz",
                "user_avatar": ""
              }
            },
            "total_comments": 15
          },
          "content": "Noi dung bai viet update",
          "created": "2016-11-06T06:28:05.909301",
          "date_created": "2016-11-06T06:28:05.909371",
          "date_updated": "2016-11-13T09:05:34.776397",
          "description": "abc",
          "display_order": 0,
          "id": 1,
          "modified": "2016-11-13T09:05:34.776379",
          "resource_uri": "/api/v1/article/1/",
          "status_code": 1,
          "title": "Day la title update",
          "user": 7
        }
      ]
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