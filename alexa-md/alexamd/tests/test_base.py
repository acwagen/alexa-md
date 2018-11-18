import unittest
from alexamd import app
from alexamd.ask import get_db, close_db
import os
import sqlite3
import json


class AlexaMDTestBase(unittest.TestCase):
    launch = {
        "version": "1.0",
        "session": {
            "new": True,
            "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
            "application": {
                "applicationId": "fake-application-id"
            },
            "attributes": {},
            "user": {
                "userId": "amzn1.account.AM3B00000000000000000000000"
            }
        },
        "context": {
            "System": {
                "application": {
                    "applicationId": "fake-application-id"
                },
                "user": {
                    "userId": "amzn1.account.AM3B00000000000000000000000"
                },
                "device": {
                    "supportedInterfaces": {
                        "AudioPlayer": {}
                    }
                }
            },
            "AudioPlayer": {
                "offsetInMilliseconds": 0,
                "playerActivity": "IDLE"
            }
        },
        "request": {
            "type": "LaunchRequest",
            "requestId": "string",
            "timestamp": "string",
            "locale": "string",
            "intent": {
                "name": "TestPlay",
                "slots": {
                }
            }
        }
    }

    open_patient = {
        "version": "1.0",
        "session": {
            "new": False,
            "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
            },
            "attributes": {
                "level": "home"
            },
            "user": {
                "userId": "amzn1.account.AM3B00000000000000000000000"
            }
        },
        "context": {
            "Display": {
                "token": ""
            },
            "System": {
                "application": {
                    "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
                },
                "user": {
                    "userId": "amzn1.account.AM3B00000000000000000000000"
                },
                "device": {
                    "supportedInterfaces": {
                        "Display": {
                                "templateVersion": "1.0",
                            "markupVersion": "1.0"
                        }
                    }
                },
                "apiEndpoint": "https://api.amazonalexa.com",
                "apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLjJiOGMxNjQ4LWQ5YjctNDU0Ni04ZTIyLTc3MGQ5NjgxY2JiMCIsImV4cCI6MTU0MjU2MjgzMiwiaWF0IjoxNTQyNTU5MjMyLCJuYmYiOjE1NDI1NTkyMzIsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUY1TVY3N1NUNFlXWlVaQkxFVFE1MkEzSkMzU1lEUldHQUFOSDdEU05GVDVBVVlQQjI0M1hZSldOSjJJUTNMSEdMTzRNRjNSRDVFR1VGRVlHSTRTV0xCWjdEWEg2RlpWTUhEQlRGNTNCT0s0V0NYREVLRkhLUzRXUUhINEdUNE5JT1hVQkZUSzVKUktDTUo3VDVZQTNLMkJRU1NWSDRUS1RPRlJZUURHNlJPS0RNQTNXQjJHUSIsInVzZXJJZCI6ImFtem4xLmFzay5hY2NvdW50LkFGQ05JRDVLQVNXTUpaSURDRjJSWFRETkRIRUpNSzRDTFRaR0JWTTZMTUVPM0FDSTJFS0ZLUEZFWFNFS04zWVlLWU5WQjdJRVdKSUJINFRMRk02SEg0NTRTMlZWQUMyTjdQRFg1V1daWFhRUTNUVUI3VUJKT0RGNkdGS1RHSVYyM05CTE5TRk1STUE0SFRaVjZXNUkzTFRRQlhQSEJLV0IyTlRCNU9QUTZOQVVMTFlCWVhTTlI0U1RaUExIT1dIUFQ0SjdQUExXQVNRNDVVWSJ9fQ.J3JDfpyOqlxoPrsrB3V-TG1hNgY72Q2lzntOX8v4YXAUHBr9Awg1frUfezm2IlH_boFCXc73UXrcrHlDnIXrgujuigiGeW3C6DQeyO41F3Bub_X55LYvWAduK4Pnh91SfmpRGFiUDjmXj-3icetrKvbBd3T9ssfZu1KNN_xzDB48i0q1iLixxu4gbXG6AeQjrgUf1gu4WWOQQSeVEPhuHTX-qZ08s6dxKh0oy1KURUDjhZCggNl8yICx8RcopsXzTlyOxnFsM5hnUVYin35BJ7QOl8lMH-Dq0wWQ4w1hM6k1p-xdcuLjCYyP1NjLVjqglMhiN6evDSGk7-pZUQm6uQ"
            },
            "Viewport": {
                "experiences": [
                        {
                            "arcMinuteWidth": 246,
                            "arcMinuteHeight": 144,
                            "canRotate": False,
                            "canResize": False
                        }
                ],
                "shape": "RECTANGLE",
                "pixelWidth": 1024,
                "pixelHeight": 600,
                "dpi": 160,
                "currentPixelWidth": 1024,
                "currentPixelHeight": 600,
                "touch": [
                    "SINGLE"
                ]
            }
        },
        "request": {
            "type": "IntentRequest",
            "requestId": " amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
            "timestamp": "2018-11-18T16:40:32Z",
            "locale": "en-US",
            "intent": {
                    "name": "OpenIntent",
                    "confirmationStatus": "NONE",
                    "slots": {
                            "imageName": {
                                "name": "imageName",
                                "value": "1",
                                "confirmationStatus": "NONE",
                                "source": "USER"
                            },
                        "imageIndex": {
                                "name": "imageIndex",
                                "confirmationStatus": "NONE"
                        }
                    }
            }
        }
    }

    open_study = {
      "version": "1.0",
      "session": {
        "new": False,
        "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
        "application": {
          "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
        },
        "attributes": {
          "level": "patient",
          "patient": "1"
        },
        "user": {
          "userId": "amzn1.account.AM3B00000000000000000000000"
        }
      },
      "context": {
        "Display": {
          "token": ""
        },
        "System": {
          "application": {
            "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
          },
          "user": {
            "userId": "amzn1.account.AM3B00000000000000000000000"
          },
          "device": {
            "supportedInterfaces": {
              "Display": {
                "templateVersion": "1.0",
                "markupVersion": "1.0"
              }
            }
          },
          "apiEndpoint": "https://api.amazonalexa.com",
          "apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLjJiOGMxNjQ4LWQ5YjctNDU0Ni04ZTIyLTc3MGQ5NjgxY2JiMCIsImV4cCI6MTU0MjU2Mjg5NiwiaWF0IjoxNTQyNTU5Mjk2LCJuYmYiOjE1NDI1NTkyOTYsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUY1TVY3N1NUNFlXWlVaQkxFVFE1MkEzSkMzU1lEUldHQUFOSDdEU05GVDVBVVlQQjI0M1hZSldOSjJJUTNMSEdMTzRNRjNSRDVFR1VGRVlHSTRTV0xCWjdEWEg2RlpWTUhEQlRGNTNCT0s0V0NYREVLRkhLUzRXUUhINEdUNE5JT1hVQkZUSzVKUktDTUo3VDVZQTNLMkJRU1NWSDRUS1RPRlJZUURHNlJPS0RNQTNXQjJHUSIsInVzZXJJZCI6ImFtem4xLmFzay5hY2NvdW50LkFGQ05JRDVLQVNXTUpaSURDRjJSWFRETkRIRUpNSzRDTFRaR0JWTTZMTUVPM0FDSTJFS0ZLUEZFWFNFS04zWVlLWU5WQjdJRVdKSUJINFRMRk02SEg0NTRTMlZWQUMyTjdQRFg1V1daWFhRUTNUVUI3VUJKT0RGNkdGS1RHSVYyM05CTE5TRk1STUE0SFRaVjZXNUkzTFRRQlhQSEJLV0IyTlRCNU9QUTZOQVVMTFlCWVhTTlI0U1RaUExIT1dIUFQ0SjdQUExXQVNRNDVVWSJ9fQ.OUUq020nrajsUbnKsBOABFx5TPY0fpnzV6_iWpt2DPXFguBgvEu8zb0cOJgyuZBJutDidBBOFbKUEIwLAlPH-ht6e3KqBKgJqy-pwZDpXGIKO8jrLAX0BK3gJTQqFAjUv8RgYdLu30zPSaipXlOmHJj3xantCYUetpR5a6Vks9OCSk2qtZa-UYNGuHhVSR42Dlznkbx6iUMCuchR1gzL3u-LuFSC2-RvAEPi8y8fto8nUyhHv8DjgyhL-alJJvQyyy4_e0r51Rp_8APgArvf8BazJ-7Ma9kWxBOQkaTHuR5LI9SDZO7dG776Db_aPL8Gt8dGBqyZG_8Jwl2jRQ1FrQ"
        },
        "Viewport": {
          "experiences": [
            {
              "arcMinuteWidth": 246,
              "arcMinuteHeight": 144,
              "canRotate": False,
              "canResize": False
            }
          ],
          "shape": "RECTANGLE",
          "pixelWidth": 1024,
          "pixelHeight": 600,
          "dpi": 160,
          "currentPixelWidth": 1024,
          "currentPixelHeight": 600,
          "touch": [
            "SINGLE"
          ]
        }
      },
      "request": {
        "type": "IntentRequest",
        "requestId": "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
        "timestamp": "2018-11-18T16:41:36Z",
        "locale": "en-US",
        "intent": {
          "name": "OpenIntent",
          "confirmationStatus": "NONE",
          "slots": {
            "imageName": {
              "name": "imageName",
              "value": "1",
              "confirmationStatus": "NONE",
              "source": "USER"
            },
            "imageIndex": {
              "name": "imageIndex",
              "confirmationStatus": "NONE"
            }
          }
        }
      }
    }

    open_collection = {
      "version": "1.0",
      "session": {
        "new": False,
        "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
        "application": {
          "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
        },
        "attributes": {
          "study": "CT",
          "level": "study",
          "patient": "1"
        },
        "user": {
          "userId": "amzn1.account.AM3B00000000000000000000000"
        }
      },
      "context": {
        "Display": {
          "token": ""
        },
        "System": {
          "application": {
            "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
          },
          "user": {
            "userId": "amzn1.account.AM3B00000000000000000000000"
          },
          "device": {
            "supportedInterfaces": {
              "Display": {
                "templateVersion": "1.0",
                "markupVersion": "1.0"
              }
            }
          },
          "apiEndpoint": "https://api.amazonalexa.com",
          "apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLjJiOGMxNjQ4LWQ5YjctNDU0Ni04ZTIyLTc3MGQ5NjgxY2JiMCIsImV4cCI6MTU0MjU2Mjk0OCwiaWF0IjoxNTQyNTU5MzQ4LCJuYmYiOjE1NDI1NTkzNDgsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUY1TVY3N1NUNFlXWlVaQkxFVFE1MkEzSkMzU1lEUldHQUFOSDdEU05GVDVBVVlQQjI0M1hZSldOSjJJUTNMSEdMTzRNRjNSRDVFR1VGRVlHSTRTV0xCWjdEWEg2RlpWTUhEQlRGNTNCT0s0V0NYREVLRkhLUzRXUUhINEdUNE5JT1hVQkZUSzVKUktDTUo3VDVZQTNLMkJRU1NWSDRUS1RPRlJZUURHNlJPS0RNQTNXQjJHUSIsInVzZXJJZCI6ImFtem4xLmFzay5hY2NvdW50LkFGQ05JRDVLQVNXTUpaSURDRjJSWFRETkRIRUpNSzRDTFRaR0JWTTZMTUVPM0FDSTJFS0ZLUEZFWFNFS04zWVlLWU5WQjdJRVdKSUJINFRMRk02SEg0NTRTMlZWQUMyTjdQRFg1V1daWFhRUTNUVUI3VUJKT0RGNkdGS1RHSVYyM05CTE5TRk1STUE0SFRaVjZXNUkzTFRRQlhQSEJLV0IyTlRCNU9QUTZOQVVMTFlCWVhTTlI0U1RaUExIT1dIUFQ0SjdQUExXQVNRNDVVWSJ9fQ.NJDmAcR8oI-MpTZJwkwaIGst9h3Q3c-nZmW2BMwMLGmqr2VSMd8CNEVL2St1SF0-ev5eDmiKDTpd14rvaXshMPcsPACT5mPnIVKaKWy_TUrN_XKoTLJ358gBtOuFmmyAlsOKjUEawESh6jbT6HHQbK0qsBxunH0VHDqq8xp3xdxutsyuJOMYP4Sg46ptgjUgeJIjMqZzxAMT6X4ph27QdRQpdvXpsKXWbTWYdA6gqaht1bgZI_jxztcOthO1dSo-7_KAnQIPm1nj4xUCjAOgatqnlk3Gkt_vX0oH57-EmIscj0Vfon3FKxAhC8e3GePtLCZnvmiDFOT14-9M1KWeRg"
        },
        "Viewport": {
          "experiences": [
            {
              "arcMinuteWidth": 246,
              "arcMinuteHeight": 144,
              "canRotate": False,
              "canResize": False
            }
          ],
          "shape": "RECTANGLE",
          "pixelWidth": 1024,
          "pixelHeight": 600,
          "dpi": 160,
          "currentPixelWidth": 1024,
          "currentPixelHeight": 600,
          "touch": [
            "SINGLE"
          ]
        }
      },
      "request": {
        "type": "IntentRequest",
        "requestId": "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
        "timestamp": "2018-11-18T16:42:28Z",
        "locale": "en-US",
        "intent": {
          "name": "OpenIntent",
          "confirmationStatus": "NONE",
          "slots": {
            "imageName": {
              "name": "imageName",
              "value": "1",
              "confirmationStatus": "NONE",
              "source": "USER"
            },
            "imageIndex": {
              "name": "imageIndex",
              "confirmationStatus": "NONE"
            }
          }
        }
      }
    }

    RESOURCES_DIR = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'resources')

    @classmethod
    def _execute_sql_script(cls, name):
        with app.app_context():
            cursor = get_db().cursor()

            filename = os.path.join(cls.RESOURCES_DIR, '{}.sql'.format(name))
            with open(filename, 'r') as sql:
                sqlscript = sql.read()
                cursor.executescript(sqlscript)

            cursor.close()
            close_db()

    @classmethod
    def setUpClass(cls):
        try:
            cls._execute_sql_script('drop')
        except sqlite3.OperationalError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            cls._execute_sql_script('drop')
        except sqlite3.OperationalError:
            pass

    def tearDown(self):
        AlexaMDTestBase._execute_sql_script('drop')

    def setUp(self):
        app.config['ASK_VERIFY_REQUESTS'] = False
        self.app = app.test_client()
        AlexaMDTestBase._execute_sql_script('create')
        AlexaMDTestBase._execute_sql_script('data')

    def test_example(self):
        response = self.app.post('/', data=json.dumps(self.launch))
        self.assertEqual(200, response.status_code)

    def test_open_patient(self):
        response = self.app.post('/', data=json.dumps(self.open_patient))
        self.assertEqual(200, response.status_code)

    def test_open_study(self):
        response = self.app.post('/', data=json.dumps(self.open_study))
        self.assertEqual(200, response.status_code)

    def test_open_collection(self):
        response = self.app.post('/', data=json.dumps(self.open_collection))
        self.assertEqual(200, response.status_code)



if __name__ == "__main__":
    unittest.main()
