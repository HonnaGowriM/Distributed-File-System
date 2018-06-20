#author: Honna Gowri Manjuanth honna.manjunath@colorado.edu
#name:
#purpose:
#date
#version
import os
import sys
import socket
import time
from hashlib import md5
class Client():
    def __init__(self):
        '''
        Check if the conf file is present else exit the program.
        '''
        try:
            self.confname=sys.argv[1]
        except:
            print("Kindly enter the conf file name.")
            sys.exit(1)
        check=os.path.isfile("Client"+"//"+self.confname)
        if (check==True):
            print("Conf file is present")
        else:
            print("Conf file doesn't exist")
            sys.exit(1)
        self.display(self.confname)
        
    def display(self,connfile):

        print("*"*110)
        print("Enter PUT along with the file name to PUT the file\nEnter GET along with the file name to GET the file\nEnter LIST to get the LIST\n" )
        print("*"*110)
        ans=str(input("Input the option:"))
        print(ans)
        if ans=="LIST":
            print("Call the list function")
            self.list(self.confname)
        else:
            try:
                ans=ans.split()
                self.option=ans[0]
                self.filename=ans[1]
            except:
                print("Kindly try again and enter the desired option.")
                sys.exit(1)
            print("Option is "+self.option+" Filename is"+self.filename)
            if self.option=="PUT":
                check=os.path.isfile("Client"+"//"+self.filename)
                if check!=True:
                    print("The requested file doesn't exist.Exiting the program.")
                    sys.exit(1)
                else:
                    self.put(self.filename,self.confname,self.option)
            
            elif self.option=="GET":
                self.get(self.filename,connfile,self.option)
                
            else:
                print("Enter a valid option.")
                sys.exit(1)
                
    def list(self,connname):
        
        det=self.details(connname)
        user=det[0]
        print("The username is "+user)
        a=self.ports(self.confname)
        response1=self.clarifys1(a,connname)
        print("The response from S1 is: ",response1)
        
        a=self.ports(self.confname)
        response2=self.clarifys2(a,connname)
        print("The response from S2 is: ",response2)
        
        a=self.ports(self.confname)
        response3=self.clarifys3(a,connname)
        print("The response from S3 is: ",response3)
        
        a=self.ports(self.confname)
        response4=self.clarifys4(a,connname)
        print("The response from S4 is: ",response4)
            
        if response1!="S1DOWN" or response3!="S3DOWN":
            try:
                self.s1.send(str("LIST").encode())
                time.sleep(0.01)
                
                self.s3.send(str("LIST").encode())
                time.sleep(0.01)
                
                self.s1.send(str(user).encode())
                time.sleep(0.01)
                
                self.s3.send(str(user).encode())
                time.sleep(0.01)
                
                reply1=self.s1.recv(65535)
                reply1=reply1.decode()
                time.sleep(0.01)
                    
                reply3=self.s3.recv(65535)
                reply3=reply3.decode()
                time.sleep(0.01)  
                
                if reply1=="NILL":
                    print("No files present in the user directory on Server 1.")
                else:
                    self.list=self.s1.recv(65535)
                    self.list=self.list.decode()
                    time.sleep(0.01)
                    print("The files at the server S1 end are:",self.list)
                
                #print("ABOVE")
                if reply3=="NILL":
                    print("No files present in the user directory on Server 3.")
                else:
                    self.list3=self.s3.recv(65535)
                    self.list3=self.list3.decode()
                    time.sleep(0.01)
                    print("The files at the server S3 end are:",self.list3)
                #print("BELOW")
                
                if reply1!="NILL":
                    final=[]
                    response1=self.listfilecheck1(self.list)

                if reply3!="NILL":
                    final=[]
                    response3=self.listfilecheck3(self.list3)
                
                file13=response1+response3    
                u=sorted(file13)
                if len(u)<4:
                    print("Either S1 or S3 is down hence can't retrieve all files.")
                    
                else:
                    print("The files present are:",u)
                    

            except:
                pass   
            
        if response2!="S2DOWN" or response4!="S4DOWN":
            try:
                self.s2.send(str("LIST").encode())
                time.sleep(0.01)
                
                self.s4.send(str("LIST").encode())
                time.sleep(0.01)
                
                self.s2.send(str(user).encode())
                time.sleep(0.01)
                
                self.s4.send(str(user).encode())
                time.sleep(0.01)
                
                reply2=self.s2.recv(65535)
                reply2=reply2.decode()
                time.sleep(0.01)
                    
                reply4=self.s4.recv(65535)
                reply4=reply4.decode()
                time.sleep(0.01)  
                
                if reply2=="NILL":
                    print("No files present in the user directory on Server 2.")
                else:
                    self.list2=self.s2.recv(65535)
                    self.list2=self.list2.decode()
                    time.sleep(0.01)
                    print("The files at the server S2 end are:",self.list2)
                
                #print("ABOVE")
                if reply4=="NILL":
                    print("No files present in the user directory on Server 4.")
                else:
                    self.list4=self.s4.recv(65535)
                    self.list4=self.list4.decode()
                    time.sleep(0.01)
                    print("The files at the server S4 end are:",self.list4)
                #print("BELOW")
                
                if reply2!="NILL":
                    final=[]
                    response2=self.listfilecheck2(self.list2)
                
                if reply4!="NILL":
                    final=[]
                    response4=self.listfilecheck4(self.list3)
                
                file24=response2+response4   
                u1=sorted(file24)
                if len(u1)<4:
                    print("Either S2 or S4 is down hence can't retrieve all files.")
                    self.display(connname)
                else:
                    print("The files present are:",u1)
                    self.display(connname)
            except:
                pass
    
    def listfilecheck1(self,list):
        list=self.list
        total=[]
        list1=self.list.strip("[")
        list1=list1.strip("]")
        list1=list1.strip()
        list1=list1.split(",")
        
        for i in list1:
            i=i.strip()
            i=i.strip("'")
            i=os.path.splitext(i)[0]+''
            total.append(i)
            #print(i)
        print("Files in S1:",total)
        return total
        
    def listfilecheck3(self,list):   
        total1=[]
        listb=self.list3.strip("[")
        listb=listb.strip("]")
        listb=listb.strip()
        listb=listb.split(",")
        for i in listb:
            i=i.strip()
            i=i.strip("'")
            i=os.path.splitext(i)[0]+''
            total1.append(i)
            #print(i)
        print("Files in S3:",total1)
        
        return total1
    
    def listfilecheck2(self,list):
        list=self.list2
        total=[]
        list1=self.list2.strip("[")
        list1=list1.strip("]")
        list1=list1.strip()
        list1=list1.split(",")
        
        for i in list1:
            i=i.strip()
            i=i.strip("'")
            i=os.path.splitext(i)[0]+''
            total.append(i)
            #print(i)
        print("Files in S4:",total)
        return total
        
    def listfilecheck4(self,list):   
        total1=[]
        listb=self.list4.strip("[")
        listb=listb.strip("]")
        listb=listb.strip()
        listb=listb.split(",")
        for i in listb:
            i=i.strip()
            i=i.strip("'")
            i=os.path.splitext(i)[0]+''
            total1.append(i)
            #print(i)
        print("Files in S5:",total1)
        
        return total1
        
    def ports(self,connname):
        pair={}
        file=open("Client"+"//"+self.confname,'r')
        a=file.readlines()
        for i in a:
            if "DFS" in i:
                (key,value)=i.split()
                pair[key]=value
        file.close()
        return pair
    
    def details(self,connname):
        user=[]
        password=[]
        conopen=open("Client"+"//"+self.confname,'r')
        conopen=conopen.readlines()
        for i in conopen:
            i=i.split(":")
            if "Username" in i[0]:
                user.append(i[1])
            if "Password" in i[0]:
                password.append(i[1])
        user=user[-1].strip("\n")
        password=password[-1].strip("\n")
        print("The username is "+user+"The password is "+password)
        return(user,password)           
     
    def clarifys1(self,a,connname):
        print("Checking the authentication for S1")
        if "DFS1" in a.keys():
                b=a["DFS1"].split(":")
                TCP_IP=b[0]
                TCP_PORT=b[1]
                self.s1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                try:
                    self.s1.connect((TCP_IP,int(TCP_PORT)))
                    print("Socket S1 to DFS1 created and connected on port: ", TCP_PORT)
                    det=self.details(connname)
                    user=det[0]
                    password=det[1]
                    
                    
                    self.s1.send(str(user).encode())
                    time.sleep(0.01)
                    print("Username sent.")
                    
                    self.s1.send(str(password).encode())
                    time.sleep(0.01)
                    print("password sent.")
                    
                    reply=self.s1.recv(65535)
                    reply=reply.decode()
                    time.sleep(0.01)
                    print("Reply from server is:",reply)
                    
                    if reply=="MATCH":
                        return "MATCH"
                    else:
                        print("Invalid Username/Password.Please try again")
                        self.s1.close()
                        sys.exit(1) 
                except:
                    return "S1DOWN"
                    print("DFS1 is not available")
                    pass
    
    def clarifys2(self,a,connname):
        print("Checking the authentication for S2")
        if "DFS2" in a.keys():
                b=a["DFS2"].split(":")
                TCP_IP=b[0]
                TCP_PORT=b[1]
                self.s2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                try:
                    self.s2.connect((TCP_IP,int(TCP_PORT)))
                    print("Socket S2 to DFS2 created and connected on port: ", TCP_PORT)
                    det=self.details(connname)
                    user=det[0]
                    password=det[1]
                    
                    self.s2.send(str(user).encode())
                    time.sleep(0.01)
                    print("Username sent.")
                    
                    self.s2.send(str(password).encode())
                    time.sleep(0.01)
                    print("password sent.")
                    
                    reply=self.s2.recv(65535)
                    reply=reply.decode()
                    time.sleep(0.01)
                    print("Reply from server is:",reply)
                    
                    if reply=="MATCH":
                        return "MATCH"
                    else:
                        print("Invalid Username/Password.Please try again")
                        self.s2.close()
                        sys.exit(1) 
                except:
                    return "S2DOWN"
                    print("DFS2 is not available")
                    pass
    
    def clarifys3(self,a,connname):
        print("Checking the authentication for S3")
        if "DFS3" in a.keys():
                b=a["DFS3"].split(":")
                TCP_IP=b[0]
                TCP_PORT=b[1]
                self.s3=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.s3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                try:
                    self.s3.connect((TCP_IP,int(TCP_PORT)))
                    print("Socket S3 to DFS3 created and connected on port: ", TCP_PORT)
                    det=self.details(connname)
                    user=det[0]
                    password=det[1]
                    
                    self.s3.send(str(user).encode())
                    time.sleep(0.01)
                    print("Username sent.")
                    
                    self.s3.send(str(password).encode())
                    time.sleep(0.01)
                    print("password sent.")
                    
                    reply=self.s3.recv(65535)
                    reply=reply.decode()
                    time.sleep(0.01)
                    print("Reply from server is:",reply)
                    
                    if reply=="MATCH":
                        return "MATCH"
                    else:
                        print("Invalid Username/Password.Please try again")
                        self.s3.close()
                        sys.exit(1) 
                except:
                    return "S3DOWN"
                    print("DFS3 is not available")
                    pass
          
    def clarifys4(self,a,connname):
        print("Checking the authentication for S4")
        if "DFS4" in a.keys():
                b=a["DFS4"].split(":")
                TCP_IP=b[0]
                TCP_PORT=b[1]
                self.s4=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.s4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                try:
                    self.s4.connect((TCP_IP,int(TCP_PORT)))
                    print("Socket S4 to DFS4 created and connected on port: ", TCP_PORT)
                    det=self.details(connname)
                    user=det[0]
                    password=det[1]
                    
                    self.s4.send(str(user).encode())
                    time.sleep(0.01)
                    print("Username sent.")
                    
                    self.s4.send(str(password).encode())
                    time.sleep(0.01)
                    print("password sent.")
                    
                    reply=self.s4.recv(65535)
                    reply=reply.decode()
                    time.sleep(0.01)
                    print("Reply from server is:",reply)
                    
                    if reply=="MATCH":
                        return "MATCH"
                    else:
                        print("Invalid Username/Password.Please try again")
                        self.s4.close()
                        sys.exit(1) 
                except:
                    return "S4DOWN"
                    print("DFS4 is not available")
                    pass
       
    def get(self,filename,connname,option):
        print("Inside GET function.")
        filename=self.filename
        print("The requested filename to GET is: ",self.filename)
        det=self.details(connname)
        user=det[0]
        print("The username is "+user)
        a=self.ports(self.confname)
        response1=self.clarifys1(a,connname)
        print("The response from S1 is: ",response1)
        
        a=self.ports(self.confname)
        response2=self.clarifys2(a,connname)
        print("The response from S2 is: ",response2)
        
        a=self.ports(self.confname)
        response3=self.clarifys3(a,connname)
        print("The response from S3 is: ",response3)
        
        a=self.ports(self.confname)
        response4=self.clarifys4(a,connname)
        print("The response from S4 is: ",response4)
            
        if response1!="S1DOWN" and response3!="S3DOWN":
            self.s1.send(str(option).encode())
            time.sleep(0.01)
            
            self.s3.send(str(option).encode())
            time.sleep(0.01)
            
            self.s1.send(str(user).encode())
            time.sleep(0.01)
            
            self.s3.send(str(user).encode())
            time.sleep(0.01)
            
            reply1=self.s1.recv(65535)
            reply1=reply1.decode()
            time.sleep(0.01)
                
            reply3=self.s3.recv(65535)
            reply3=reply3.decode()
            time.sleep(0.01)  
            
            if reply1=="NILL":
                print("No files present in the user directory on Server 1.")
            else:
                self.list=self.s1.recv(65535)
                self.list=self.list.decode()
                time.sleep(0.01)
                print("The files at the server S1 end are:",self.list)
            
            #print("ABOVE")
            if reply3=="NILL":
                print("No files present in the user directory on Server 3.")
            else:
                self.list3=self.s3.recv(65535)
                self.list3=self.list3.decode()
                time.sleep(0.01)
                print("The files at the server S3 end are:",self.list3)
            #print("BELOW")
            
            if reply1!="NILL" and reply3!="NILL":
                final=[]
                response=self.filecheck13(self.list,self.list3,filename)
                print("Files in Server 1",response[0])
                print("Files in Server 3",response[1])
                final=response[0]+response[1]
                print(final)
                u=sorted(final)
                print("Sorted list of files:",u)
                seen = ['1','2','3','4']
                if seen==u:
                    check=os.path.isdir("Client"+"//"+user)
                    print(check)
                    if check==False:
                        os.mkdir("Client"+"//"+user)
                    else:
                        print("User dir present")            
                    print("All file parts are present")
                    
                    self.s1.send(("SEND").encode())
                    time.sleep(0.01)

                    FN=self.s1.recv(65535)
                    FN=FN.decode()
                    time.sleep(2)
                    
                    print("Filename:",FN)
                    
                    
                    data=self.s1.recv(65535)
                    data=data.decode()
                    
                    
                    filea=open("Client"+"//"+user+"//"+FN+".txt",'w')
                    filea.write(data)
                    filea.close()
                    time.sleep(2)
                    
                    FN=self.s1.recv(65535)
                    FN=FN.decode()
                    time.sleep(2)
                    
                    print("Filename:",FN)
                    
                    
                    data=self.s1.recv(65535)
                    data=data.decode()
                    
                    
                    filea=open("Client"+"//"+user+"//"+FN+".txt",'w')
                    filea.write(data)
                    filea.close()
                    time.sleep(2)
                    
                    self.s3.send(("SEND").encode())
                    time.sleep(0.01)
                    
                    FN3=self.s3.recv(65535)
                    FN3=FN3.decode()
                    time.sleep(2)
                    print("Filename:",FN3)
                    
                    data3=self.s3.recv(65535)
                    data3=data3.decode()
                    file3=open("Client"+"//"+user+"//"+FN3+".txt",'w')
                    file3.write(data3)
                    file3.close()
                    time.sleep(2)
                    
                    FN3=self.s3.recv(65535)
                    FN3=FN3.decode()
                    time.sleep(2)
                    
                    print("Filename:",FN3)
                    data3=self.s3.recv(65535)
                    data3=data3.decode()
                    file3=open("Client"+"//"+user+"//"+FN3+".txt",'w')
                    file3.write(data3)
                    file3.close()
                    time.sleep(2)
                            
                    filenames = [filename+".1.txt",filename+".2.txt",filename+".3.txt",filename+".4.txt"]
                    for i in filenames:
                        print(i)
                        re=open("Client"+"//"+user+"//"+i,'r')
                        wr=open("Client"+"//"+user+"//"+filename,'a')
                        for line in re.readlines():
                            wr.write(line)
                        wr.close()
                        re.close()
                        self.display(connname)
                            
                else:
                    print("All file parts are not present")
                    self.s1.send(("NOSEND").encode())
                    time.sleep(0.01)
            
                    self.s3.send(("NOSEND").encode())
                    time.sleep(0.01)
                    self.display(connname)
                    
                 
                    
                    
        elif response2!="S2DOWN" and response4!="S4DOWN":
            print("From 2 & 4 Server.")
            self.s2.send(str(option).encode())
            time.sleep(0.01)
           
            self.s4.send(str(option).encode())
            time.sleep(0.01)
            
            self.s2.send(str(user).encode())
            time.sleep(0.01)
            
            self.s4.send(str(user).encode())
            time.sleep(0.01)
     
            reply2=self.s2.recv(65535)
            reply2=reply2.decode()
            time.sleep(0.01)
            
            reply4=self.s4.recv(65535)
            reply4=reply4.decode()
            time.sleep(0.01)  
            print("Waiting")
            if reply2=="NILL":
                print("No files present in the user directory on Server 2.")
            else:
                self.list2=self.s2.recv(65535)
                self.list2=self.list2.decode()
                time.sleep(0.01)
                print("The files at the server S2 end are:",self.list2)
            
            print("ABOVE")
            if reply4=="NILL":
                print("No files present in the user directory on Server 4.")
            else:
                self.list4=self.s4.recv(65535)
                self.list4=self.list4.decode()
                time.sleep(0.01)
                print("The files at the server S4 end are:",self.list4)
            print("BELOW")
            
            if reply2!="NILL" and reply4!="NILL":
                final=[]
                response=self.filecheck24(self.list2,self.list4,filename)
                print("Files in server 2:",response[0])
                print("Files in server 4:",response[1])
                final=response[0]+response[1]
                print(final)
                u=sorted(final)
                print("Sorted files from 2 and 4:",u)
                seen = ['1','2','3','4']
                if seen==u:
                    check=os.path.isdir("Client"+"//"+user)
                    print(check)
                    if check==False:
                        os.mkdir("Client"+"//"+user)
                    else:
                        print("User dir present")
                    print("All file parts are present")
                    
                    self.s2.send(("SEND").encode())
                    time.sleep(0.01)

                    FN=self.s2.recv(65535)
                    FN=FN.decode()
                    time.sleep(2)
                    
                    print("Filename:",FN)
                    
                    
                    data=self.s2.recv(65535)
                    data=data.decode()
                    
                    
                    filea=open("Client"+"//"+user+"//"+FN+".txt",'w')
                    filea.write(data)
                    filea.close()
                    time.sleep(2)
                    
                    FN=self.s2.recv(65535)
                    FN=FN.decode()
                    time.sleep(2)
                    
                    print("Filename:",FN)
                    
                    
                    data=self.s2.recv(65535)
                    data=data.decode()
                    
                    
                    filea=open("Client"+"//"+user+"//"+FN+".txt",'w')
                    filea.write(data)
                    filea.close()
                    time.sleep(2)
                    
                    self.s4.send(("SEND").encode())
                    time.sleep(0.01)
                    
                    FN3=self.s4.recv(65535)
                    FN3=FN3.decode()
                    time.sleep(2)
                    print("Filename:",FN3)
                    
                    data3=self.s4.recv(65535)
                    data3=data3.decode()
                    file3=open("Client"+"//"+user+"//"+FN3+".txt",'w')
                    file3.write(data3)
                    file3.close()
                    time.sleep(2)
                    
                    FN3=self.s4.recv(65535)
                    FN3=FN3.decode()
                    time.sleep(2)
                    
                    print("Filename:",FN3)
                    data3=self.s4.recv(65535)
                    data3=data3.decode()
                    file3=open("Client"+"//"+user+"//"+FN3+".txt",'w')
                    file3.write(data3)
                    file3.close()
                    time.sleep(2)
                            
                    filenames = [filename+".1.txt",filename+".2.txt",filename+".3.txt",filename+".4.txt"]
                    for i in filenames:
                        print(i)
                        re=open("Client"+"//"+user+"//"+i,'r')
                        wr=open("Client"+"//"+user+"//"+filename,'a')
                        for line in re.readlines():
                            wr.write(line)
                        wr.close()
                        re.close()
                        self.display(connname)
                            
                else:
                    print("All file parts are not present")
                    self.s2.send(("NOSEND").encode())
                    time.sleep(0.01)
            
                    self.s4.send(("NOSEND").encode())
                    time.sleep(0.01)
                    self.display(connname)
                    
                       
                    
        else:
            print("The complete file can't be fetched as it can't be reconstructed since more than 2 servers are down.")   
            self.display(connname)
            
                          
    def filecheck24(self,list2,list4,filename):
        list=self.list2
        list4=self.list4
        total=[]
        fi=[]
        list1=self.list2.strip("[")
        list1=list1.strip("]")
        list1=list1.strip()
        list1=list1.split(",")
        
        for i in list1:
            i=i.strip()
            i=i.strip("'")
            i=os.path.splitext(i)[0]+''
            f=os.path.splitext(i)[0]+''
            total.append(i)
            fi.append(f)
            print("I:",i)
       
        print("Filename",filename)
        print("list",fi)
        n=len(total)
        i=0
        new=[]
        while i<n:
            if filename in fi[i]:
                total[i]=total[i].split(".")[2]
                print(total[i])
                new.append(total[i])
                i=i+1
            else:break
        print("The new:",new)
        
        total1=[]
        fi1=[]
        listb=self.list4.strip("[")
        listb=listb.strip("]")
        listb=listb.strip()
        listb=listb.split(",")
        for i in listb:
            i=i.strip()
            i=i.strip("'")
            i=os.path.splitext(i)[0]+''
            f=os.path.splitext(i)[0]+''
            total1.append(i)
            fi1.append(f)
            print(i)
        n=len(total1)
        i=0
        new1=[]
        while i<n:
            if filename in fi1[i]:
                total1[i]=total1[i].split(".")[2]
                print(total1[i])
                new1.append(total1[i])
                i=i+1
            else:break
        print("The new1:",new1)
        return new,new1       
                         
    def filecheck13(self,list,list2,filename):
        list=self.list
        list2=self.list3
        total=[]
        fi=[]
        list1=self.list.strip("[")
        list1=list1.strip("]")
        list1=list1.strip()
        list1=list1.split(",")
        
        for i in list1:
            i=i.strip()
            i=i.strip("'")
            i=os.path.splitext(i)[0]+''
            f=os.path.splitext(i)[0]+''
            total.append(i)
            fi.append(f)
            print("I:",i)
        print("total:",total)
       
        print("Filename",filename)
        print("list",fi)
        n=len(total)
        i=0
        new=[]
        while i<n:
            if filename in fi[i]:
                total[i]=total[i].split(".")[2]
                print(total[i])
                new.append(total[i])
                i=i+1
            else:break
        print("The new:",new)
        
        total1=[]
        fi1=[]
        listb=self.list3.strip("[")
        listb=listb.strip("]")
        listb=listb.strip()
        listb=listb.split(",")
        for i in listb:
            i=i.strip()
            i=i.strip("'")
            i=os.path.splitext(i)[0]+''
            f=os.path.splitext(i)[0]+''
            total1.append(i)
            fi1.append(f)
            print(i)
        print("The new list:",fi1)
        n=len(total1)
        i=0
        new1=[]
        while i<n:
            if filename in fi1[i]:
                total1[i]=total1[i].split(".")[2]
                print(total1[i])
                new1.append(total1[i])
                i=i+1
            else:break
        print("The new1:",new1)
        return new,new1
        
    def put(self,filename,connfile,option):
        option=self.option
        filename=self.filename
        connfile=self.confname
        print("The file that needs to be uploaded is:",self.filename)
        checkfile=os.path.isfile("Client"+"//"+self.filename)
        if checkfile!=True:
            print("The requested file doesn't exist.")
            sys.exit(1)
        else:
            filehash = md5()
            filehash.update(open("Client"+"//"+self.filename).read().encode())
            b=filehash.hexdigest()
            self.x_value= int(b,base=16) % 4
            print(self.x_value)
            size= os.path.getsize("Client"+"//"+self.filename)
            res=int(size/4)
            print(res)
            offsetlen = []
            offsetlen.append(res)
            offsetlen.append(res)
            offsetlen.append(res)
            offsetlen.append(size-(offsetlen[0]+offsetlen[1]+offsetlen[2]))
            n=0
            print(offsetlen)
            while n < 4:
                with open("Client"+"//"+self.filename,'r') as main:
                    present1=main.read(65532)
                    with open("Client"+"//"+self.filename+"."+str(n+1)+".txt",'w') as fh:
                        data2write = present1[(n*res):(n*res)+offsetlen[n]] #Defining the range of data that must be read
                        fh.write(data2write)
                n=n+1   
        self.subput(self.confname,self.x_value,self.filename,self.option)
    
    def subput(self,connname,x,filename,option):
        option=self.option
        x=self.x_value
        connname=self.confname
        filename=self.filename
        a=self.ports(self.confname)
        print("List of ports and IP is: ",a)
        print("Value of the hash is:",self.x_value)
       
        
        if self.x_value==0:
            print("The hash value is 0 hence the pieces to be uploaded is of the form DFS1:(1,2); DFS2:(2,3); DFS3:(3,4);DFS4:(4,1)")
            
            response1=self.clarifys1(a,connname)
            print("The response from S1 is: ",response1)
            
            if response1=="MATCH":    
                self.s1.send(str(self.option).encode())
                time.sleep(0.01)
                
                self.s1.send(str(self.filename).encode())
                time.sleep(0.01)
                    
                self.s1.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file1=open("Client"+"//"+self.filename+".1.txt",'r')
           
                file1data=file1.read(65535)
                self.s1.send(file1data.encode())
                time.sleep(0.01)
                file1.close()
                file1=open("Client"+"//"+self.filename+".2.txt",'r')
           
                file1data=file1.read(65535)
                self.s1.send(file1data.encode())
                time.sleep(0.01) 
                file1.close() 
            else:
                print("Server 1 is down")
                
            response2=self.clarifys2(a,connname)
            print("The response from S2 is: ",response2)
            
            if response2=="MATCH":
                self.s2.send(str(self.option).encode())
                time.sleep(0.01)
                
                self.s2.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie2=self.s2.recv(65535)
                #dummie2=dummie2.decode()
                #time.sleep(0.01)
                    
                self.s2.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file2=open("Client"+"//"+self.filename+".2.txt",'r')
            
                file2data=file2.read(65535)
                self.s2.send(file2data.encode())
                time.sleep(0.01)
                file2.close()
                file2=open("Client"+"//"+self.filename+".3.txt",'r')
                
                file2data=file2.read(65535)
                self.s2.send(file2data.encode())
                time.sleep(0.01)    
                file2.close()
            
            else:
                print("Server 2 is down.")       
            response3=self.clarifys3(a,connname)
            print("The response from S3 is: ",response3)
            
            if response3=="MATCH":
                self.s3.send(str(self.option).encode())
                time.sleep(0.01)
                
                self.s3.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie3=self.s3.recv(65535)
                #dummie3=dummie3.decode()
                #time.sleep(0.01)
                    
                self.s3.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file3=open("Client"+"//"+self.filename+".3.txt",'r')
        
                file3data=file3.read(65535)
                self.s3.send(file3data.encode())
                time.sleep(0.01)
                file3.close()
                file3=open("Client"+"//"+self.filename+".4.txt",'r')
        
                file3data=file3.read(65535)
                self.s3.send(file3data.encode())
                time.sleep(0.01)
                file3.close()    
            else:
                print("Server 3 is down.")   
            response4=self.clarifys4(a,connname)
            print("The response from S4 is: ",response4)
            
            if response4=="MATCH":
                self.s4.send(str(self.option).encode())
                time.sleep(0.01)
                
                self.s4.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie4=self.s4.recv(65535)
                #dummie4=dummie4.decode()
                #time.sleep(0.01)
                    
                self.s4.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file4=open("Client"+"//"+self.filename+".4.txt",'r')
           
                file4data=file4.read(65535)
                self.s4.send(file4data.encode())
                time.sleep(0.01)
                file4.close()
                file4=open("Client"+"//"+self.filename+".1.txt",'r')
           
                file4data=file4.read(65535)
                self.s4.send(file4data.encode())
                time.sleep(0.01)
                file4.close()
               
                self.display(connname)
            else:
                print("Server 4 is down.")  
              
                self.display(connname)
                
            
                
        elif self.x_value==1:
            print("The hash value is 1 hence the pieces to be uploaded is of the form DFS1:(4,1); DFS2:(1,2); DFS3:(2,3);DFS4:(3,4)")
            
            response1=self.clarifys1(a,connname)
            print("The response from S1 is: ",response1)
            
            if response1=="MATCH":
                self.s1.send(str(self.option).encode())
                time.sleep(0.01)
                
                self.s1.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie=self.s1.recv(65535)
                #dummie=dummie.decode()
                #time.sleep(0.01)
                
                self.s1.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file1=open("Client"+"//"+self.filename+".4.txt",'r')
                
                file1data=file1.read(65535)
                self.s1.send(file1data.encode())
                time.sleep(0.01)
                file1.close()
                file1=open("Client"+"//"+self.filename+".1.txt",'r')
                
                file1data=file1.read(65535)
                self.s1.send(file1data.encode())
                time.sleep(0.01)   
                file1.close()
            else:
                print("Server 1 is down.")
            response2=self.clarifys2(a,connname)
            print("The response from S2 is: ",response2)
            
            if response2=="MATCH":
                self.s2.send(str(self.option).encode())
                time.sleep(0.01)
                
                self.s2.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie2=self.s2.recv(65535)
                #dummie2=dummie2.decode()
                #time.sleep(0.01)
                    
                self.s2.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file2=open("Client"+"//"+self.filename+".1.txt",'r')
            
                file2data=file2.read(65535)
                self.s2.send(file2data.encode())
                time.sleep(0.01)
                file2.close()
                file2=open("Client"+"//"+self.filename+".2.txt",'r')
         
                file2data=file2.read(65535)
                self.s2.send(file2data.encode())
                time.sleep(0.01)
                file2.close()
            else:
                print("Server 2 is down.")   
            response3=self.clarifys3(a,connname)
            print("The response from S3 is: ",response3)
            
            if response3=="MATCH":
                self.s3.send(str(self.option).encode())
                time.sleep(0.01)
                
                self.s3.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie3=self.s3.recv(65535)
                #dummie3=dummie3.decode()
                #time.sleep(0.01)
                    
                self.s3.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file3=open("Client"+"//"+self.filename+".2.txt",'r')
            
                file3data=file3.read(65535)
                self.s3.send(file3data.encode())
                time.sleep(0.01)
                file3.close()
                file3=open("Client"+"//"+self.filename+".3.txt",'r')
              
                file3data=file3.read(65535)
                self.s3.send(file3data.encode())
                time.sleep(0.01) 
                file3.close()
            else:
                print("Server 3 is down.")
                  
            response4=self.clarifys4(a,connname)
            print("The response from S4 is: ",response4)
            
            if response4=="MATCH":
                self.s4.send(str(self.option).encode())
                time.sleep(0.01)
                
                self.s4.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie4=self.s4.recv(65535)
                #dummie4=dummie4.decode()
                #time.sleep(0.01)
                    
                self.s4.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file4=open("Client"+"//"+self.filename+".3.txt",'r')
               
                file4data=file4.read(65535)
                self.s4.send(file4data.encode())
                time.sleep(0.01)
                file4.close()
                file4=open("Client"+"//"+self.filename+".4.txt",'r')
           
                file4data=file4.read(65535)
                self.s4.send(file4data.encode())
                time.sleep(0.01)   
                file4.close() 
          
                self.display(connname) 
            else:
                print("Server 4 is down.")    
              
                self.display(connname)    
                 
        elif self.x_value==2:
            print("The hash value is 2 hence the pieces to be uploaded is of the form DFS1:(3,4); DFS2:(4,1); DFS3:(1,2);DFS4:(2,3)")
            response1=self.clarifys1(a,connname)
            print("The response from S1 is: ",response1)
            
            if response1=="MATCH":
                self.s1.send(str(self.option).encode())
                time.sleep(0.01)
                
                self.s1.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie=self.s1.recv(65535)
                #dummie=dummie.decode()
                #time.sleep(0.01)
                
                self.s1.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file1=open("Client"+"//"+self.filename+".3.txt",'r')
           
                file1data=file1.read(65535)
                self.s1.send(file1data.encode())
                time.sleep(0.01)
                file1.close()
                file1=open("Client"+"//"+self.filename+".4.txt",'r')
             
                file1data=file1.read(65535)
                self.s1.send(file1data.encode())
                time.sleep(0.01)   
                file1.close()
            else:
                print("Server 1 is down.")   
            response2=self.clarifys2(a,connname)
            print("The response from S2 is: ",response2)
            
            
            if response2=="MATCH":
                self.s2.send(str(self.option).encode())
                time.sleep(0.01)
            
                self.s2.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie2=self.s2.recv(65535)
                #dummie2=dummie2.decode()
                #time.sleep(0.01)
                    
                self.s2.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file2=open("Client"+"//"+self.filename+".4.txt",'r')
             
                file2data=file2.read(65535)
                self.s2.send(file2data.encode())
                time.sleep(0.01)
                file2.close()
                file2=open("Client"+"//"+self.filename+".1.txt",'r')
            
                file2data=file2.read(65535)
                self.s2.send(file2data.encode())
                time.sleep(0.01)
                file2.close() 
            else:
                print("Server 2 is down.")      
                
            response3=self.clarifys3(a,connname)
            print("The response from S3 is: ",response3) 
            
            if response3=="MATCH":        
                self.s3.send(str(self.option).encode())
                time.sleep(0.01)
                
                self.s3.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie3=self.s3.recv(65535)
                #dummie3=dummie3.decode()
                #time.sleep(0.01)
                    
                self.s3.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file3=open("Client"+"//"+self.filename+".1.txt",'r')
          
                file3data=file3.read(65535)
                self.s3.send(file3data.encode())
                time.sleep(0.01)
                file3.close()
                file3=open("Client"+"//"+self.filename+".2.txt",'r')
             
                file3data=file3.read(65535)
                self.s3.send(file3data.encode())
                time.sleep(0.01)  
                file3.close()
            else:
                print("Server 3 is down.")                   
                       
            response4=self.clarifys4(a,connname)
            print("The response from S4 is: ",response4)
            if response4=="MATCH":
                self.s4.send(str(self.option).encode())
                time.sleep(0.01)
                
                self.s4.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie4=self.s4.recv(65535)
                #dummie4=dummie4.decode()
                #time.sleep(0.01)
                    
                self.s4.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file4=open("Client"+"//"+self.filename+".2.txt",'r')
              
                file4data=file4.read(65535)
                self.s4.send(file4data.encode())
                time.sleep(0.01)
                file4.close()
                file4=open("Client"+"//"+self.filename+".3.txt",'r')
           
                file4data=file4.read(65535)
                self.s4.send(file4data.encode())
                time.sleep(0.01)
                file4.close()
           
                self.display(connname)
            else:
                print("Server 4 is down.")
            
                self.display(connname)

        
        else:   
            print("The hash value is 3 hence the pieces to be uploaded is of the form DFS1:(2,3); DFS2:(3,4); DFS3:(4,1);DFS4:(1,2)")
            response1=self.clarifys1(a,connname)
            print("The response from S1 is: ",response1)
            
            if response1=="MATCH":
                self.s1.send(str(self.option).encode())
                time.sleep(0.01)
                
                self.s1.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie=self.s1.recv(65535)
                #dummie=dummie.decode()
                #time.sleep(0.01)
                   
                self.s1.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file1=open("Client"+"//"+self.filename+".2.txt",'r')
                file1data=file1.read(65535)
                self.s1.send(file1data.encode())
                time.sleep(0.01)
                file1.close()
                file1=open("Client"+"//"+self.filename+".3.txt",'r')
                file1data=file1.read(65535)
                self.s1.send(file1data.encode())
                time.sleep(0.01)    
                file1.close()
            else:
                print("Server 1 is down.")   
            response2=self.clarifys2(a,connname)
            print("The response from S2 is: ",response2)
            
            
            if response2=="MATCH":
                self.s2.send(str(self.option).encode())
                time.sleep(0.01)
            
                self.s2.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie2=self.s2.recv(65535)
                #dummie2=dummie2.decode()
                #time.sleep(0.01)
                    
                self.s2.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file2=open("Client"+"//"+self.filename+".3.txt",'r')
                file2data=file2.read(65535)
                self.s2.send(file2data.encode())
                time.sleep(0.01)
                file2.close()
                file2=open("Client"+"//"+self.filename+".4.txt",'r')
                file2data=file2.read(65535)
                self.s2.send(file2data.encode())
                time.sleep(0.01) 
                file2.close()  
            else:
                print("Server 2 is down.")   
            response3=self.clarifys3(a,connname)
            print("The response from S3 is: ",response3)
            
            
            if response3=="MATCH":
                self.s3.send(str(self.option).encode())
                time.sleep(0.01)
            
                self.s3.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie3=self.s3.recv(65535)
                #dummie3=dummie3.decode()
                #time.sleep(0.01)
                    
                self.s3.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file3=open("Client"+"//"+self.filename+".4.txt",'r')
                file3data=file3.read(65535)
                self.s3.send(file3data.encode())
                time.sleep(0.01)
                file3.close()
                file3=open("Client"+"//"+self.filename+".1.txt",'r')
                file3data=file3.read(65535)
                self.s3.send(file3data.encode())
                time.sleep(0.01)
                file3.close()
            else:
                print("Server 3 is down.")
            response4=self.clarifys4(a,connname)
            print("The response from S4 is: ",response4)
            
            
            if response4=="MATCH":
                self.s4.send(str(self.option).encode())
                time.sleep(0.01)
            
                self.s4.send(str(self.filename).encode())
                time.sleep(0.01)
                
                #dummie4=self.s4.recv(65535)
                #dummie4=dummie4.decode()
                #time.sleep(0.01)
                    
                self.s4.send(str(self.x_value).encode())
                time.sleep(0.01)
                
                file4=open("Client"+"//"+self.filename+".1.txt",'r')
                file4data=file4.read(65535)
                self.s4.send(file4data.encode())
                time.sleep(0.01)
                file4.close()
                file4=open("Client"+"//"+self.filename+".2.txt",'r')
                file4data=file4.read(65535)
                self.s4.send(file4data.encode())
                time.sleep(0.01) 
                file4.close()
            
                self.display(connname)
            else:
                print("Server 4 is down.") 
                  
                self.display(connname)
                     
if __name__ == '__main__' :
    Client=Client()
    