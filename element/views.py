# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import json
import sqlite3
from datetime import *
from dateutil.relativedelta import *

import logging
logger = logging.getLogger(__name__)

# GET ~/keyboard/ 요청에 반응
def keyboard(request):
    return JsonResponse({
        'type': 'buttons',
        'buttons': ['식단표', '3학년 시간표', '학사일정', '오늘의 날씨', '홈페이지 공지사항']
    })

# csrf 토큰 에러 방지, POST 요청에 message response
@csrf_exempt
def message(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    responder = received_json_data['content']

    daystring = ["월", "화", "수", "목", "금", "토", "일"]
    nextdaystring = ["화", "수", "목", "금", "토", "일", "월"]

    today = date.today().weekday()
    today_date = date.today()
    tomorrow_date = today_date+relativedelta(days=+1)
    if responder in daystring:
        if today == 6:
            days = today_date + relativedelta(weekday=daystring.index(responder))
        else:
            days = today_date + relativedelta(days=-today, weekday=daystring.index(responder))

    if responder == '식단표':
        return JsonResponse({
            'message': {
                'text': '식단표를 열람하기 위해 항목을 선택해 주세요.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['오늘 식단표', '내일 식단표', '이번주의 다른 요일 식단표', '초기화면으로']
            }
        })
    elif responder == '오늘 식단표':
        return JsonResponse({
            'message': {
                'text': '[' + responder + '] \n' + today_date.strftime("%m월 %d일 ") + daystring[today] + '요일 식단표입니다. \n \n' + data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['오늘 식단표', '내일 식단표', '이번주의 다른 요일 식단표', '초기화면으로']
            }
        })
    elif responder == '내일 식단표':
        return JsonResponse({
            'message': {
                'text': '[' + responder + '] \n' + tomorrow_date.strftime("%m월 %d일 ") + nextdaystring[today] + '요일 식단표입니다. \n \n' + data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['오늘 식단표', '내일 식단표', '이번주의 다른 요일 식단표', '초기화면으로']
            }
        })
    elif responder == '이번주의 다른 요일 식단표':
        return JsonResponse({
            'message': {
                'text': '식단 정보가 필요한 요일을 입력해주세요\n입력 가능 요일 : 월 화 수 목 금 토'
            },
            'keyboard': {
                'type': 'text'
            }
        })
    elif responder in daystring and responder != "일":
        return JsonResponse({
            'message': {
                'text': days.strftime("%m월 %d일 ") + responder + '요일 식단표입니다. \n \n' + data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['오늘 식단표', '내일 식단표', '이번주의 다른 요일 식단표', '초기화면으로']
            }
        })
    elif responder == '3학년 시간표':
        return JsonResponse({
            'message': {
                'text': '항목을 선택해 주세요.\n이과반만 조회가 가능합니다.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면으로', '3-5 오늘 시간표', '3-5 내일 시간표', '3-6 오늘 시간표', '3-6 내일 시간표', '3-7 오늘 시간표', '3-7 내일 시간표', '3-8 오늘 시간표', '3-8 내일 시간표']
            }
        })
    elif responder == '3-5 오늘 시간표':
        return JsonResponse({
            'message': {
                'text': today_date.strftime("3-5반의 %m월 %d일 ") + daystring[today] + '요일 시간표입니다. \n \n' + data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면으로', '3-5 오늘 시간표', '3-5 내일 시간표', '3-6 오늘 시간표', '3-6 내일 시간표', '3-7 오늘 시간표', '3-7 내일 시간표', '3-8 오늘 시간표', '3-8 내일 시간표']
            }
        })
    elif responder == '3-5 내일 시간표':
        return JsonResponse({
            'message': {
                'text': tomorrow_date.strftime("3-5반의 %m월 %d일 ") + nextdaystring[today] + '요일 시간표입니다. \n \n' + data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면으로', '3-5 오늘 시간표', '3-5 내일 시간표', '3-6 오늘 시간표', '3-6 내일 시간표', '3-7 오늘 시간표', '3-7 내일 시간표', '3-8 오늘 시간표', '3-8 내일 시간표']
            }
        })
    elif responder == '3-6 오늘 시간표':
        return JsonResponse({
            'message': {
                'text': today_date.strftime("3-6반의 %m월 %d일 ") + daystring[today] + '요일 시간표입니다. \n \n' + data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면으로', '3-5 오늘 시간표', '3-5 내일 시간표', '3-6 오늘 시간표', '3-6 내일 시간표', '3-7 오늘 시간표', '3-7 내일 시간표', '3-8 오늘 시간표', '3-8 내일 시간표']
            }
        })
    elif responder == '3-6 내일 시간표':
        return JsonResponse({
            'message': {
                'text': tomorrow_date.strftime("3-6반의 %m월 %d일 ") + nextdaystring[today] + '요일 시간표입니다. \n \n' + data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면으로', '3-5 오늘 시간표', '3-5 내일 시간표', '3-6 오늘 시간표', '3-6 내일 시간표', '3-7 오늘 시간표', '3-7 내일 시간표', '3-8 오늘 시간표', '3-8 내일 시간표']
            }
        })
    elif responder == '3-7 오늘 시간표':
        return JsonResponse({
            'message': {
                'text': today_date.strftime("3-7반의 %m월 %d일 ") + daystring[today] + '요일 시간표입니다. \n \n' + data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면으로', '3-5 오늘 시간표', '3-5 내일 시간표', '3-6 오늘 시간표', '3-6 내일 시간표', '3-7 오늘 시간표', '3-7 내일 시간표', '3-8 오늘 시간표', '3-8 내일 시간표']
            }
        })
    elif responder == '3-7 내일 시간표':
        return JsonResponse({
            'message': {
                'text': tomorrow_date.strftime("3-7반의 %m월 %d일 ") + nextdaystring[today] + '요일 시간표입니다. \n \n' + data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면으로', '3-5 오늘 시간표', '3-5 내일 시간표', '3-6 오늘 시간표', '3-6 내일 시간표', '3-7 오늘 시간표', '3-7 내일 시간표', '3-8 오늘 시간표', '3-8 내일 시간표']
            }
        })
    elif responder == '3-8 오늘 시간표':
        return JsonResponse({
            'message': {
                'text': today_date.strftime("3-8반의 %m월 %d일 ") + daystring[today] + '요일 시간표입니다. \n \n' + data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면으로', '3-5 오늘 시간표', '3-5 내일 시간표', '3-6 오늘 시간표', '3-6 내일 시간표', '3-7 오늘 시간표', '3-7 내일 시간표', '3-8 오늘 시간표', '3-8 내일 시간표']
            }
        })
    elif responder == '3-8 내일 시간표':
        return JsonResponse({
            'message': {
                'text': tomorrow_date.strftime("3-8반의 %m월 %d일 ") + nextdaystring[today] + '요일 시간표입니다. \n \n' + data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면으로', '3-5 오늘 시간표', '3-5 내일 시간표', '3-6 오늘 시간표', '3-6 내일 시간표', '3-7 오늘 시간표', '3-7 내일 시간표', '3-8 오늘 시간표', '3-8 내일 시간표']
            }
        })
    elif responder == '학사일정':
        return JsonResponse({
            'message': {
                'text': '학교 금년 학사일정을 열람합니다.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['전체 학사일정', '1학기 학사일정', '2학기 학사일정', '초기화면으로']
            }
        })
    elif responder == '전체 학사일정':
        return JsonResponse({
            'message': {
                'text': data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['전체 학사일정', '1학기 학사일정', '2학기 학사일정', '초기화면으로']
            }
        })
    elif responder == '1학기 학사일정':
        return JsonResponse({
            'message': {
                'text': data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['전체 학사일정', '1학기 학사일정', '2학기 학사일정', '초기화면으로']
            }
        })
    elif responder == '2학기 학사일정':
        return JsonResponse({
            'message': {
                'text': data_from_db(responder, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['전체 학사일정', '1학기 학사일정', '2학기 학사일정', '초기화면으로']
            }
        })
    elif responder == '오늘의 날씨':
        return JsonResponse({
            'message': {
                'text': 'https://search.naver.com/search.naver?query=%EB%82%A0%EC%94%A8'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['식단표', '3학년 시간표', '학사일정', '오늘의 날씨', '홈페이지 공지사항']
            }
        })
    elif responder == '홈페이지 공지사항':
        return JsonResponse({
            'message': {
                'text': 'http://gsh.hs.kr/m/main.jsp?SCODE=S0000000718&mnu=M001006001'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['식단표', '3학년 시간표', '학사일정', '오늘의 날씨', '홈페이지 공지사항']
            }
        })
    elif responder == '초기화면으로':
        return JsonResponse({
            'message': {
                'text': '항목을 선택해 주세요.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['식단표', '3학년 시간표', '학사일정', '오늘의 날씨', '홈페이지 공지사항']
            }
        })
    else:
        return JsonResponse({
            'message': {
                'text': '잘못된 명령어입니다 ' + '[' + responder + ']' + '\n입력 가능 명령어 : 월 화 수 목 금 토'
            },
            'keyboard': {
                'type': 'text'
            }
        })

# DB에 저장된 자료 내보내기(급식, 시간표, 학사일정 등)
def data_from_db(responder, today, daystring):
    day_eng = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    con = sqlite3.connect("element/database/responder.db")
    cur = con.cursor()

    if responder == '오늘 식단표':
        query = ("SELECT " + (day_eng[today]) + " FROM meal")
    if responder == '내일 식단표':
        if today == 6:
            query = ("SELECT mon FROM meal")
        else:
            query = ("SELECT " + (day_eng[today + 1]) + " FROM meal")
    if responder in daystring:
        query = ("SELECT " + (day_eng[daystring.index(responder)]) + " FROM meal")
    if responder == '3-5 오늘 시간표':
        query = ("SELECT " + (day_eng[today]) + " FROM alpha")
    if responder == '3-5 내일 시간표':
        if today == 6:
            query = ("SELECT mon FROM alpha")
        else:
            query = ("SELECT " + (day_eng[today + 1]) + " FROM alpha")
    if responder == '3-6 오늘 시간표':
        query = ("SELECT " + (day_eng[today]) + " FROM beta")
    if responder == '3-6 내일 시간표':
        if today == 6:
            query = ("SELECT mon FROM beta")
        else:
            query = ("SELECT " + (day_eng[today + 1]) + " FROM beta")
    if responder == '3-7 오늘 시간표':
        query = ("SELECT " + (day_eng[today]) + " FROM cinnamon")
    if responder == '3-7 내일 시간표':
        if today == 6:
            query = ("SELECT mon FROM cinnamon")
        else:
            query = ("SELECT " + (day_eng[today + 1]) + " FROM cinnamon")
    if responder == '3-8 오늘 시간표':
        query = ("SELECT " + (day_eng[today]) + " FROM donut")
    if responder == '3-8 내일 시간표':
        if today == 6:
            query = ("SELECT mon FROM donut")
        else:
            query = ("SELECT " + (day_eng[today + 1]) + " FROM donut")
    if responder == '전체 학사일정':
        query = ("SELECT whole FROM schedule")
    if responder == '1학기 학사일정':
        query = ("SELECT par FROM schedule")
    if responder == '2학기 학사일정':
        query = ("SELECT part FROM schedule")

    cur.execute(query)
    data = cur.fetchone()

    return data[0]
