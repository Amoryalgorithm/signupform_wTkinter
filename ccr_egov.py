import time
from datetime import date
import MySQLdb
import tkMessageBox
from Tkinter import * 
import os
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

def registerToDB():
    #db connection
    db = MySQLdb.connect("localhost","root","","egov")
    cursor = db.cursor()
    
    #get teamID first (increment last teamID)
    cursor.execute("select count(*) from teams")
    data = cursor.fetchone()
    teamID_str = "%d" %data
    teamID = int(teamID_str) + 1
    
    member_names = [e_captain_name.get(),e_member2_name.get(),e_member3_name.get()]
    member_ages = [int(e_captain_age.get()),int(e_member2_age.get()),int(e_member3_age.get())]
    member_roles = ["captain","member","member"]
    member_ids = [1,2,3]
    member_cnps = [e_captain_cnp.get(),e_member2_cnp.get(),e_member3_cnp.get()]
    member_countys = [e_captain_county.get(),e_member2_county.get(),e_member3_county.get()]
    member_sex = [e_captain_sex.get(),e_member2_sex.get(),e_member3_sex.get()]
    team_name = e_team_name.get()
    
    try:
        for i in range(3):
            cursor.execute("""insert into members values(%s,%s,%s,%s,%s,%s,%s,%s)""",(member_ids[i],member_names[i],member_roles[i],teamID,member_cnps[i],
            member_countys[i],member_sex[i],member_ages[i]))
        cursor.execute("""insert into teams values(%s,%s)""",(team_name,teamID))
        db.commit()
    except:
        db.rollback()
        print "Exception: Rolledback DB"
    print "Commited to DB, uploading XML.."
    writeFiles()
    uploadFile()
    db.close()
    os.system("start "+e_team_name.get()+".txt")

def writeFiles():
    filename = e_team_name.get() + ".xml"
    f = open(filename,'w')
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f.write("<teamName>"+e_team_name.get()+"</teamName>\n")
    f.write("\t<captainName>"+e_captain_name.get()+"</captainName>\n")
    f.write("\t<captainCNP>"+e_captain_cnp.get()+"</captainCNP>\n")
    f.write("\t<captainCounty>"+e_captain_county.get()+"</captainCounty\n")
    f.write("\t<captainSex>"+e_captain_sex.get()+"</captainSex>\n")
    f.write("\t<captainAge>"+e_captain_age.get()+"</captainAge>\n")
    f.write("\t<member2Name>"+e_member2_name.get()+"</member2Name>\n")
    f.write("\t<member2CNP>"+e_member2_cnp.get()+"</member2CNP>\n")
    f.write("\t<member2County>"+e_member2_county.get()+"</member2County\n")
    f.write("\t<member2Sex>"+e_member2_sex.get()+"</member2Sex>\n")
    f.write("\t<member2Age>"+e_member2_age.get()+"</member2Age>\n")
    f.write("\t<member3Name>"+e_member3_name.get()+"</member3Name>\n")
    f.write("\t<member3CNP>"+e_member3_cnp.get()+"</member3CNP>\n")
    f.write("\t<member3County>"+e_member3_county.get()+"</member3County\n")
    f.write("\t<member3Sex>"+e_member3_sex.get()+"</member3Sex>\n")
    f.write("\t<member3Age>"+e_member3_age.get()+"</member3Age>\n")
    f.close()
    
    paymentOrderFilename = e_team_name.get() + ".txt"
    f = open(paymentOrderFilename,'w')
    f.write("Ordin de plata - Taxa inscriere competitie\n")
    f.write("Echipa:\t"+e_team_name.get()+"\n")
    f.write("Membri:\t"+e_captain_name.get()+"\t"+e_member2_name.get()+"\t"+e_member3_name.get()+"\n")
    f.write("Suma platita:\t 30RON\n")
    date_str = "%s" %date(int(time.strftime("%Y")),int(time.strftime("%m")),int(time.strftime("%d")))
    f.write("Data platii:\t"+date_str)
    f.close()
    
def submitCallback():
    status = 1
    print "checking data..."
    f1 = Frame(root)
    f1.tkraise()    
    cnps = [e_captain_cnp.get(),e_member2_cnp.get(),e_member3_cnp.get()]
    for cnp in cnps:
        if(len(cnp) != 13):
            print "CNP gresit!"
            tkMessageBox.showinfo("Submit Error", "CNP gresit")
            status = 0
            break
    
    ages = [e_captain_age.get(),e_member2_age.get(),e_member3_age.get()]
    #check all ages are present in the form
    for age in ages:
        if(len(age)<1):
            status=0
            tkMessageBox.showinfo("Submit Error", "Nu sunt completate toate varstele")
            print "Nu sunt completate toate varstele"
            break;
    
    if status !=0:
        for age in ages:
            if(int(age) < 15):
                print "Varsta minima pt participare este 15 ani"
                tkMessageBox.showinfo("Submit Error", "Varsta minima pt participare este de 15 ani")
                status = 0
                break
    names = [e_team_name.get(),e_captain_name.get(),e_member2_name.get(),e_member3_name.get()]
    for name in names:
        if(len(name) < 1):
            status=0
            tkMessageBox.showinfo("Submit Error", "Nu sunt completate toate numele")
            print "Nu sunt completate toate numele"
            break
    if(status==1):
        #succes, commit data to dbserver and make xml file
        print "Succes"
        tkMessageBox.showinfo("Submit", "Succes")
        registerToDB()
        exit()
    else:
        print "Completati toate campurile"
        
def eventHandlerCaptainCNP(event):
    cnp = e_captain_cnp.get()
    status=1
    if (len(cnp) == 13):
            
            #cnp of correct size, autofill age,sex,county
            e_captain_sex.delete(0,50)#remove first 50 characters
            if(cnp[0] == "1"):
                #male
                e_captain_sex.insert(0,"Barbat")
            else:
                e_captain_sex.insert(0,"Femeie")
            
            
            #check if county part of CNP is correct
            if(int(cnp[7:9])<=52):
                e_captain_county.delete(0,50)
                e_captain_county.insert(0,lista_judete[int(cnp[7]+cnp[8])-1])
            else:
                e_captain_cnp.config(fg="red")
                status=0
            
            #check if age part of cnp is correct(day,month)
            if(int (cnp[3:5])>12 or int(cnp[5:7])>31):
                e_captain_cnp.config(fg="red")
                status=0
            else:
                e_captain_age.delete(0,3)
                curr_date = date(int(time.strftime("%Y")),int(time.strftime("%m")),int(time.strftime("%d")))
                year=0;
                if(int(cnp[1:3])>16):
                    year=int(cnp[1:3])+1900
                else:
                    year=int(cnp[1:3])+2000
                    
                d1=date(year,int(cnp[3:5]),int(cnp[5:7]))
                age = abs(d1-curr_date).days/365
                e_captain_age.insert(0,age)
            if(status==1):
                e_captain_cnp.config(fg="black")
    else:
        #incomplete CNP
        e_captain_cnp.config(fg="red")
        
def eventHandlerMember2CNP(event):
    cnp = e_member2_cnp.get()
    status=1
    if (len(cnp) == 13):
            
            #cnp of correct size, autofill age,sex,county
            e_member2_sex.delete(0,50)#remove first 50 characters
            if(cnp[0] == "1"):
                #male
                e_member2_sex.insert(0,"Barbat")
            else:
                e_member2_sex.insert(0,"Femeie")
            
            
            #check if county part of CNP is correct
            if(int(cnp[7:9])<=52):
                e_member2_county.delete(0,50)
                e_member2_county.insert(0,lista_judete[int(cnp[7]+cnp[8])-1])
            else:
                e_member2_cnp.config(fg="red")
                status=0
            
            #check if age part of cnp is correct(day,month)
            if(int (cnp[3:5])>12 or int(cnp[5:7])>31):
                e_member2_cnp.config(fg="red")
                status=0
            else:
                e_member2_age.delete(0,3)
                curr_date = date(int(time.strftime("%Y")),int(time.strftime("%m")),int(time.strftime("%d")))
                year=0;
                if(int(cnp[1:3])>16):
                    year=int(cnp[1:3])+1900
                else:
                    year=int(cnp[1:3])+2000
                    
                d1=date(year,int(cnp[3:5]),int(cnp[5:7]))
                age = abs(d1-curr_date).days/365
                e_member2_age.insert(0,age)
            if(status==1):
                e_member2_cnp.config(fg="black")
    else:
        #incomplete CNP
        e_member2_cnp.config(fg="red")

def eventHandlerMember3CNP(event):
    cnp = e_member3_cnp.get()
    status=1
    if (len(cnp) == 13):
            
            #cnp of correct size, autofill age,sex,county
            e_member3_sex.delete(0,50)#remove first 50 characters
            if(cnp[0] == "1"):
                #male
                e_member3_sex.insert(0,"Barbat")
            else:
                e_member3_sex.insert(0,"Femeie")
            
            
            #check if county part of CNP is correct
            if(int(cnp[7:9])<=52):
                e_member3_county.delete(0,50)
                e_member3_county.insert(0,lista_judete[int(cnp[7]+cnp[8])-1])
            else:
                e_member3_cnp.config(fg="red")
                status=0
            
            #check if age part of cnp is correct(day,month)
            if(int (cnp[3:5])>12 or int(cnp[5:7])>31):
                e_member3_cnp.config(fg="red")
                status=0
            else:
                e_member3_age.delete(0,3)
                curr_date = date(int(time.strftime("%Y")),int(time.strftime("%m")),int(time.strftime("%d")))
                year=0;
                if(int(cnp[1:3])>16):
                    year=int(cnp[1:3])+1900
                else:
                    year=int(cnp[1:3])+2000
                    
                d1=date(year,int(cnp[3:5]),int(cnp[5:7]))
                age = abs(d1-curr_date).days/365
                e_member3_age.insert(0,age)
            if(status==1):
                e_member3_cnp.config(fg="black")
    else:
        #incomplete CNP
        e_member3_cnp.config(fg="red")
    
def eventHandlerCaptainAge(event):
    age = e_captain_age.get()
    if(len(age)>0):
        if(int(age)<15):
            e_captain_age.config(fg="red")
        else:
            e_captain_age.config(fg="black")

def eventHandlerMember2Age(event):
    age = e_member2_age.get()
    if(len(age)>0):
        if(int(age)<15):
            e_member2_age.config(fg="red")
        else:
            e_member2_age.config(fg="black")    

def eventHandlerMember3Age(event):
    age = e_member3_age.get()
    if(len(age)>0):
        if(int(age)<15):
            e_member3_age.config(fg="red")
        else:
            e_member3_age.config(fg="black")

def uploadFile():
    filename = e_team_name.get() + ".xml"
    FILES =((filename,False)) #plain text, fara conversie in format gdrive
    folder_id = "0B89gzdi5QGF6dXdJSEJoRWZjYW8"

    metadata = {'title': filename,'parents': folder_id }
    res = DRIVE.files().insert(body=metadata,
            media_body=filename, fields='mimeType').execute()
    
    if res:
        print('Uploaded "%s" (%s)' % (filename, res['mimeType']))
        
lista_judete=['Alba','Arad','Arges','Bacau','Bihor','Bistrita-Nasaud','Botosani','Brasov','Braila','Buzau','Caras-Severin','Cluj','Constanta','Covasna',
'Dambovita','Dolj','Galati','Gorj','Harghita','Hunedoara','Ialomita','Iasi','Ilfov','Maramures','Mehedinti','Mures','Neamt','Olt','Prahova','Satu Mare',
'Salaj','Sibiu','Suceava','Teleorman','Timis','Tulcea','Vaslui','Valcea','Vrancea','Bucuresti','Bucuresti S.1','Bucuresti S.2','Bucuresti S.3','Bucuresti S.4',
'Bucuresti S.5','Bucuresti S.6','Calarasi,Giurgiu']

#gdrive setup
SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('storage.json')
creds = store.get()

#first time -- get authorization
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('secret.json', SCOPES)

DRIVE = build('drive', 'v2', http=creds.authorize(Http()))


#Tkinter form
root = Tk()
root.geometry('250x650')
root.wm_title("Formular Inscriere")


for x in range(2):
    Grid.columnconfigure(root, x, weight=1)

for y in range(25):
    Grid.rowconfigure(root, y, weight=1)

l_team_name = Label(root,text="Nume echipa")
l_team_name.grid(row=0,column=0)
e_team_name = Entry(root,bd=5)
e_team_name.grid(row=0,column=1)
l_team_name.bind('FocusOut',eventHandlerCaptainCNP)

Label(root,text="").grid(row=1,column=0)

l_captain_name = Label(root,text="Nume capitan")
l_captain_name.grid(row=2,column=0)
e_captain_name = Entry(root,bd=5)
e_captain_name.grid(row=2,column=1)
l_captain_cnp = Label(root,text="CNP")
l_captain_cnp.grid(row=3,column=0)
e_captain_cnp = Entry(root,bd=5)
e_captain_cnp.grid(row=3,column=1)
l_captain_county = Label(root,text="Judet")
l_captain_county.grid(row=4,column=0)
e_captain_county = Entry(root,bd=5)
e_captain_county.grid(row=4,column=1)
l_captain_sex = Label(root,text="Sex")
l_captain_sex.grid(row=5,column=0)
e_captain_sex = Entry(root,bd=5)
e_captain_sex.grid(row=5,column=1)
l_captain_age = Label(root,text="Varsta")
l_captain_age.grid(row=6,column=0)
e_captain_age = Entry(root,bd=5)
e_captain_age.grid(row=6,column=1)
Label(root,text="").grid(row=7,column=0)

Label(root,text="").grid(row=8,column=0)

l_member2_name = Label(root,text="Nume membru2")
l_member2_name.grid(row=9,column=0)
e_member2_name = Entry(root,bd=5)
e_member2_name.grid(row=9,column=1)
l_member2_cnp = Label(root,text="CNP")
l_member2_cnp.grid(row=10,column=0)
e_member2_cnp = Entry(root,bd=5)
e_member2_cnp.grid(row=10,column=1)
l_member2_county = Label(root,text="Judet")
l_member2_county.grid(row=11,column=0)
e_member2_county = Entry(root,bd=5)
e_member2_county.grid(row=11,column=1)
l_member2_sex = Label(root,text="Sex")
l_member2_sex.grid(row=12,column=0)
e_member2_sex = Entry(root,bd=5)
e_member2_sex.grid(row=12,column=1)
l_member2_age = Label(root,text="Varsta")
l_member2_age.grid(row=13,column=0)
e_member2_age = Entry(root,bd=5)
e_member2_age.grid(row=13,column=1)

Label(root,text="").grid(row=14,column=0)

Label(root,text="").grid(row=15,column=0)

l_member3_name = Label(root,text="Nume membru3")
l_member3_name.grid(row=16,column=0)
e_member3_name = Entry(root,bd=5)
e_member3_name.grid(row=16,column=1)
l_member3_cnp = Label(root,text="CNP")
l_member3_cnp.grid(row=17,column=0)
e_member3_cnp = Entry(root,bd=5)
e_member3_cnp.grid(row=17,column=1)
l_member3_county = Label(root,text="Judet")
l_member3_county.grid(row=18,column=0)
e_member3_county = Entry(root,bd=5)
e_member3_county.grid(row=18,column=1)
l_member3_sex = Label(root,text="Sex")
l_member3_sex.grid(row=19,column=0)
e_member3_sex = Entry(root,bd=5)
e_member3_sex.grid(row=19,column=1)
l_member3_age = Label(root,text="Varsta")
l_member3_age.grid(row=20,column=0)
e_member3_age = Entry(root,bd=5)
e_member3_age.grid(row=20,column=1) 

Label(root,text="").grid(row=21,column=0)

submit = Button(root,text="Submit",command = submitCallback)
submit.grid(row=22,column=1)

Label(root,text="").grid(row=23)

#register event handlers -- after CNP completion, auto-fill age,sex,county
e_captain_cnp.bind('<FocusOut>',eventHandlerCaptainCNP)
e_member2_cnp.bind('<FocusOut>',eventHandlerMember2CNP)
e_member3_cnp.bind('<FocusOut>',eventHandlerMember3CNP)

e_captain_age.bind('<FocusOut>',eventHandlerCaptainAge)
e_member2_age.bind('<FocusOut>',eventHandlerMember2Age)
e_member3_age.bind('<FocusOut>',eventHandlerMember3Age)
def main():    
    root.mainloop()

main()