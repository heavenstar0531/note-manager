# -*- coding: utf-8 -*- 
import sys
from urllib2 import Request, urlopen, HTTPError
import json

def NotePrint(noteID,title,content,category,labels):
	
	if len(labels) >=1:
		tags=labels[0]
		for i in range(1,len(labels)):
			tags+=(','+labels[i])
	else:
		tags=""
	print 'ID: ', noteID
	print 'Title: ', title
	print 'Content: ', content
	print 'Category: ', category
	print 'Tags: ', tags
	print " "

if len(sys.argv) == 1:
	print "Please write -h , /h or -help as parameter for user guide."
	sys.exit()

if sys.argv[1]=="-h"  or sys.argv[1]=="/h" or sys.argv[1]=="-help":
	print "Notes Manager v1.0"
	print ""
	print "Available functions:"
	print "notes - show all notes"
	print "note X - where X is notesId. Show notes with selected id."
	print "categories - show all categories"
	print "notesofcategory X - where X is category name. Show notes with selected category name."
	print "labels - show all labels "
	print "notesoflabel X - where X is label name. Show notes with selected label"
	print "delete X - where X is notesId. Delete notes with selected ID. In this test version user cannot delete note with id lower than 4!"
	print "add - add new note"
	print "edit X - where X is notesId. Edit selected note."
	sys.exit()

if sys.argv[1]=="notes":
	request = Request("<API_HOST>/notes")
        response_body = urlopen(request).read()
        data  = json.loads(response_body)
	for i in range(len(data)):
        	NotePrint(data[i]['ID'],data[i]['title'],data[i]['content'],data[i]['category'],data[i]['labels'])

if sys.argv[1]=="note":
	try:
		noteid = int(sys.argv[2])
		request = Request("<API_HOST>/notes/"+sys.argv[2])
		response_body = urlopen(request).read()
		if response_body=="None":
			print "Note with ID not exists."
			sys.exit()
		data  = json.loads(response_body)
		NotePrint(data['ID'],data['title'],data['content'],data['category'],data['labels'])
	except ValueError:
		print "Podaj liczbe"
		sys.exit()

if sys.argv[1]=="categories":
        request = Request("<API_HOST>/category")
        response_body = urlopen(request).read()
        data  = json.loads(response_body)
	print "Categories:"
	for i in range(len(data)):
		print i+1,"-",data[i]
		
if sys.argv[1]=="labels":
        request = Request("<API_HOST>/labels")
        response_body = urlopen(request).read()
        data  = json.loads(response_body)
        print "Labels:"
        for i in range(len(data)):
                print i+1,"-",data[i]

if sys.argv[1]=="add":
	title = raw_input("Enter the title of the note:")
	content = raw_input("Enter the content of the note:")
	print "Enter categories from the available below:"
	req = Request("<API_HOST>/category")
        response = urlopen(req).read()
        categories  = json.loads(response)
	for i in range(len(categories)):
		print categories[i]
	spr = 0
	category = raw_input("Category:")
	for i in range(len(categories)):
		if category == categories[i]:
			spr = 1
	if spr == 0:
		print "You have entered the wrong categories. Please try adding the note again."
		sys.exit()
	labels = raw_input("Enter labels separated by commas:")
	values = json.dumps({"title": title, "content": content, "category": category, "labels": labels})
	headers = {"Content-Type": "application/json"}
	request = Request("<API_HOST>/notes", data=values, headers=headers)
	response_body = urlopen(request).read()
	print response_body	

if sys.argv[1]=="edit":
	try:
		noteID = int(sys.argv[2])
		print "Available options:"
		print "title - edit title"
		print "content - edit content"
		print "category - edit category"
		print "labels - edit labels"
		print "exit - end of edit"
	        request = Request("<API_HOST>/notes/"+sys.argv[2])
                response_body = urlopen(request).read()
                if response_body=="None":
                        print "Note with ID not exists"
                        sys.exit()
                data  = json.loads(response_body)
		data['labels'] = ",".join(data['labels'])
		what = raw_input("Enter one of the available options:")
		while what != "exit":
			if what == "title":
				newtitle = raw_input("Enter new title:")
				data['title'] = newtitle
			if what == "content":
				newcontent = raw_input("Enter new content:")
				data['content'] = newcontent
			if what == "category":
				req = Request("<API_HOST>/category")
        			response = urlopen(req).read()
        			cat  = json.loads(response)
        			print "Available categories:"
        			for i in range(len(data)):
                			print cat[i]
				newcategory = raw_input("Enter categories from the available below :")
				spr = 0
				for i in range(len(cat)):
                			if newcategory == cat[i]:
                        			spr = 1
        			if spr == 0:
                			print "You have entered the wrong categories. Please try adding the note again."
                			sys.exit()
				data['category'] = newcategory
			if what == "labels":
				newlabels = raw_input("Enter labels separated by commas:")
				data['labels'] = newlabels
			what = raw_input("Enter the next option or enter exit if you want to finish editing: ")
		values = json.dumps({"content": data['content'], "category": data['category'], "labels": data['labels'], "title": data['title']})
		headers = {"Content-Type": "application/json"}
		request = Request("<API_HOST>/notes/"+str(noteID), data=values, headers=headers)
		request.get_method = lambda: 'PUT'
		response_body = urlopen(request).read()
		print response_body
	except ValueError:
		print "Note with ID not exists"
		sys.exit()


if sys.argv[1]=="notesofcategory":
	try:
		request = Request("<API_HOST>/category/"+sys.argv[2])
		response_body = urlopen(request).read()
		if response_body == "None":
			print 'No notes from the given category'
			sys.exit()
		data  = json.loads(response_body)
		if len(data) == 0:
       	        	print 'No notes from the given category'
		for i in range(0,len(data)):
			NotePrint(data[i]['ID'],data[i]['title'],data[i]['content'],data[i]['category'],data[i]['labels'])
	except HTTPError:
		print 'Incorrect category name.'
		sys.exit()

if sys.argv[1]=="notesoflabel":
	try:
	        request = Request("<API_HOST>/labels/"+sys.argv[2])
      	  	response_body = urlopen(request).read()
		if response_body == "None":
                	print 'No notes with the given tag'
                	sys.exit()
        	data  = json.loads(response_body)
        	if len(data) == 0:
               		print 'No notes with the given tag'
       	 	for i in range(0,len(data)):
                	NotePrint(data[i]['ID'],data[i]['title'],data[i]['content'],data[i]['category'],data[i]['labels'])
	except HTTPError:
		print "Incorrect label name."
		sys.exit()	

if sys.argv[1]=="delete":
	try:
		request = Request("http://len.iem.pw.edu.pl/~lelenp/apps/demo/note/"+sys.argv[2])
		request.get_method = lambda: 'DELETE'
		response_body = urlopen(request).read()
		print response_body
	except HTTPError:
		print "Wrong Note Id."
		sys.exit()
