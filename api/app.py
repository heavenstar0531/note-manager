# -*- coding: utf-8 -*- 
import web
import json

prefix = '/notes-manager'

urls = (
    prefix + '/notes', 'NotesList', 		
    prefix + '/notes/(.*)', 'NotesOne', 
    prefix + '/category', 'CategoryList', 	
    prefix + '/category/(.*)', 'CategoryNote', 
    prefix + '/labels', 'LabelsList', 	
    prefix + '/labels/(.*)', 'LabelsNote' 
)

app = web.application(urls, globals())
wsgi = app.wsgifunc()

category = ["School", "Work", "House", "Training", "Science", "Meetings"]
labels = ['today', 'python', 'java', 'february', 'gift', 'example']

notes = [
	{
		"ID": 0,
		"title": "Cleaning",
		"content": "Clean my room",
		"category": category[2],
		"labels": [labels[0]]
	},
	{
		"ID": 1,
		"title": "Student project",
		"content": "Deadline = 22/01",
		"category": category[0],
		"labels": [labels[3]]
	},

	{
		"ID": 2,
		"title": "Meeting with John",
		"content": "Beer in Warsaw pub",
		"category": category[5],
		"labels": [labels[0]]
	},
	{
		"ID": 3,
		"title": "Girlfriend's birthday",
		"content": "21/03",
		"category": category[2],
		"labels": [labels[4], labels[5]]
	}
]

statement = [
	     {"msg": "You can not delete a note with an ID less than 4 (TEST VERSION)"},
	     {"msg": "Incorrect data given as a call parameter"},
	     {"msg": "No data found"}
	    ]

class NotesList:
    def GET(self):
	jsonNotes = json.dumps(notes)
	return jsonNotes
    def POST(self):
        lab = 0
        IDnew = notes[len(notes)-1]["ID"]+1
	dataobject = json.loads(web.data())
        titlenew = dataobject['title']
        contentnew = dataobject['content']
        categorynew = dataobject['category']
        labelsnew = dataobject['labels']
        labelsSplit = labelsnew.split(',')
        for i in range(len(labelsSplit)):
            for j in range(len(labels)):
                if json.dumps(labels[j]) == json.dumps(labelsSplit[i]):
                    lab = 1
            if lab == 0:
                labels.append(labelsSplit[i])
                lab = 0
        notes.append(dict(ID=IDnew, title=titlenew, category=categorynew, content=contentnew, labels=labelsSplit))
        web.created()
        return notes[len(notes)-1]


class NotesOne:
    def GET(self, noteID):
	try:
	    i = int(noteID)
	    if i > notes[len(notes)-1]['ID']:
		web.notfound()
		return None
	    for ind in range(len(notes)):
		if notes[ind]['ID'] == i:
	    	    jsonNote = json.dumps(notes[ind])
	    	    return jsonNote
	except ValueError:
	    web.badrequest()
	    return json.dumps(statement[1])
    def DELETE(self, noteID):
        try:
	    licznik = []
            i = int(noteID)
            if (i <= 4):
                web.badrequest()
                return json.dumps(statement[0])
            elif i > notes[len(notes)-1]['ID']:
		web.notfound()
		return None
	    else:
                for notesindex in range(len(notes)):
		    if int(notes[notesindex]["ID"]) == int(noteID):
			notes.remove(notes[notesindex])
			return
        except ValueError:
            web.badrequest()
	    return json.dumps(statement[1])
    def PUT(self,noteID):
        try:
            ID = int(noteID)
            lab = 0
	    dataobject = json.loads(web.data())
            titlenew = dataobject['title']
            contentnew = dataobject['content']
            categorynew = dataobject['category']
            labelsnew = dataobject['labels']
            labelsSplit = labelsnew.split(',')
            for i in range(len(labelsSplit)):
                for j in range(len(labels)):
                    if json.dumps(labels[j]) == json.dumps(labelsSplit[i]):
                        lab = 1
                if lab == 0:
                    labels.append(labelsSplit[i])
                    lab = 0
	    for index in range(len(notes)):
		if ID == int(notes[index]["ID"]):
	            notes[index].update(title=titlenew, content=contentnew, category=categorynew, labels=labelsSplit)
            	    return json.dumps(notes[index])
        except ValueError:
            web.badrequest()
            return json.dumps(statement[1])

class CategoryList:
    def GET(self):
	jsonCategory = json.dumps(category)	
	return jsonCategory

class CategoryNote:
    def GET(self, CategoryName):
	index = 0
	CategoryNotes = []
	for i in range (len(category)):
	    if json.dumps(category[i]) == json.dumps(CategoryName):
	        index = 1
		for j in range(len(notes)):
		    if json.dumps(notes[j]["category"]) == json.dumps(CategoryName):		
			CategoryNotes.append(notes[j])
		if len(CategoryNotes) == 0:
		    return None
		else:
		    return json.dumps(CategoryNotes)
	if index == 0:
	    web.badrequest()
	    return  json.dumps(statement[1])
		    
class LabelsList:
    def GET(self):
	jsonLabels = json.dumps(labels)
	return jsonLabels

class LabelsNote:
    def GET(self, LabelName):
        index = 0
        LabelNotes = []
        for i in range (len(labels)):
            if json.dumps(labels[i]) == json.dumps(LabelName):
                index = 1
                for j in range(len(notes)):
       		    for k in range(len(notes[j]["labels"])):
		        if json.dumps(notes[j]["labels"][k]) == json.dumps(LabelName):
                            LabelNotes.append(notes[j])
                if len(LabelNotes) == 0:
                    return None
                else:
                    return json.dumps(LabelNotes)
        if index == 0:
            web.badrequest()
            return  json.dumps(statement[1])


if __name__ == "__main__":
    app.run()
