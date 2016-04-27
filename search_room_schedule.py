#-*- encoding=utf-8 -*-
import requests
from lxml import etree

login_url="http://webap1.kuas.edu.tw/kuas/perchk.jsp"
query_room_url="http://webap1.kuas.edu.tw/kuas/ag_pro/ag302_01.jsp"
query_room_context_url="http://webap1.kuas.edu.tw/kuas/ag_pro/ag302_02.jsp"
LOGIN_TIMEOUT = 5.0
room_courses=[]

class course:
	def __init__(self,name,room_id):
		self.name=name
		self.room_id=room_id

def login(session, username, password):
    payload = {"uid": username, "pwd": password}
    r = session.post(login_url, data=payload, timeout=LOGIN_TIMEOUT)
    root = etree.HTML(r.text)
    try:
        is_login = not root.xpath("//script")[-1].text.startswith("alert")
    except:
        is_login = False

    return is_login

def catch_room(session,username,password):
	payload={
		"arg01":"104",
		"arg02":"2",
		"arg03":"guest",
		"fncid":"AG302",
		"uid":username
		}
	r=session.get(query_room_url,data=password,timeout=LOGIN_TIMEOUT)
	root=etree.HTML(r.text)
	a=root.xpath("//select[@name='room_id']/option")

	for i in a:
		room_courses.append(course(i.text,i.attrib["value"]))
	
	search_room=input("search_room (ex:108) :")
	while search_room =="":
		search_room = input("try again :")

	search_week=input("search_week (ex:一,二,三...) : ")
	while search_week not in ["一","二","三","四","五","六","日",""]:
		search_week=input("input (ex:一,二,三...): ")

	if search_week =="":
		print("if you don't input,all week print")

	for room_course in room_courses:
		if room_course.name.find(search_room) != -1:
			search_id=room_course.room_id
			payload2={
				"yms_yms":payload["arg01"]+"#"+payload["arg02"],
				"room_id":search_id,
				"unit_serch":"查 詢"
				}
			r= session.post(query_room_context_url,data=payload2,timeout=LOGIN_TIMEOUT)
			root=etree.HTML(r.text)
			a=root.xpath('//form/table/tr/td')
			print (room_course.name)
			for i in range(8,len(a),11) :
				if search_week !="" :
					if list(a[i].itertext())[0].find(search_week) != -1:
						print(list(a[i].itertext())[0])
				else:
					print(list(a[i].itertext())[0])

if __name__ == "__main__":
    s = requests.session()
    is_login = login(s, "guest", "123")
    print(is_login)
    catch_room(s,"guest","123")
