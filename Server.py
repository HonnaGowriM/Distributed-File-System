#author: Honna Gowri Manjuanth honna.manjunath@colorado.edu
#name:
#purpose:
#date
#version
import threading
import os
import sys
import socket
import time

class Server():
    def __init__(self):
        self.i=0
        self.threads=[]
        try:
            self.dirname=sys.argv[1]
            self.dirname=self.dirname[1:]
            self.Port=sys.argv[2]
        except:
            print("Kindly enter the server directory name and the port number.")
            sys.exit(1)
        '''
        Check if the conf file is present else exit the program
        '''
        
        check=os.path.isfile(self.dirname+"//"+"dfs.conf")
        if (check==True):
            print("Conf file is present.")
            self.IP="127.0.0.1"
            self.prg(self.IP,self.Port,self.dirname)
        else:
            print("Conf file doesn't exist.")
            sys.exit(1)
    
    def prg(self,IP,Port,dirname):   
        '''
        Create the socket
        '''
        try:
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.s.bind((IP,int(Port)))
            self.s.listen(5)
            print("DFS1 is listening on: ",Port)
            while(1):
                    self.conn,addr= self.s.accept()
                    #print("The address of the browser is : ", self.addbro)
                    if self.conn:
                        thread_multiple=multiplethread(self.conn,self.i,self.s,self.dirname) #Calling the thread class.
                        self.threads.append(thread_multiple)
                        thread_multiple.start()
                        self.i=self.i+1
                        print("Thread number running "+str(self.i))
                   
        except socket.error:
            print("Socket wasn't created")
            sys.exit()
            
class multiplethread(threading.Thread):
    def __init__(self,conn,i,s,dirname):
        threading.Thread.__init__(self)
        self.conn=conn
        self.i=i
        self.s=s
        self.dirname=dirname
    
    def run(self):
        print("Threading started")
        user=self.conn.recv(65535)
        user=user.decode()
        print("Username of the user trying to access the DFS:",user)
        time.sleep(0.01)
        
        password=self.conn.recv(65535)
        password=password.decode()
        print("Password of the user trying to access the DFS:",password)
        time.sleep(0.01)
        
        '''
            Extract the conf file to match the credentials
        '''
    
        users={}
        conopen=open(self.dirname+"//"+"dfs.conf",'r')
        conopen=conopen.readlines()
        for i in conopen:
            (key,value)=i.split()
            users[key]=value   
        print(users)
        
        if user in users.keys():
            print("Username "+user+" is present")
            if password==users[user]:
                print("Password matched for"+user+". Hence can provide access")
                self.conn.send("MATCH".encode())
                time.sleep(0.01)
            else:
                print("Password didn't match for"+user)     
                self.conn.send("NOMATCH".encode())
                self.conn.close()
                sys.exit(1)
                
        else:
            print("Username "+user+" is not present")
            self.conn.send("NOMATCH".encode())
            self.conn.close()
            sys.exit(1)
            
        option=self.conn.recv(65535)
        option=option.decode()
        print("The received user option is:",option)
        time.sleep(0.01)
        
        
        if option=="PUT":
            check=os.path.isdir(self.dirname+"//"+user)
            print(check)
            if check==False:
                os.mkdir(self.dirname+"//"+user)
                #self.conn.send("Creating directory".encode())
                #time.sleep(0.01)
            
            
            filename=self.conn.recv(65535)
            filename=filename.decode()
            print("The received user filename is:",filename)
            time.sleep(0.01)
        
                
            x_value=self.conn.recv(65535)
            x_value=x_value.decode()
            time.sleep(0.01)
            
            print("The received hash value is:",x_value)
            if x_value=="0":
                data=self.conn.recv(65535)
                data=data.decode()
                filea=open(self.dirname+"//"+user+"//"+filename+".1.txt",'w')
                filea.write(data)
                time.sleep(0.01)
                data=self.conn.recv(65535)
                data=data.decode()
                fileb=open(self.dirname+"//"+user+"//"+filename+".2.txt",'w')
                fileb.write(data)
                time.sleep(0.01)
                self.conn.close()
                filea.close()
                fileb.close()
            elif x_value=="1":
                data=self.conn.recv(65535)
                data=data.decode()
                filea=open(self.dirname+"//"+user+"//"+filename+".4.txt",'w')
                filea.write(data)
                time.sleep(0.01)
                data=self.conn.recv(65535)
                data=data.decode()
                fileb=open(self.dirname+"//"+user+"//"+filename+".1.txt",'w')
                fileb.write(data)
                time.sleep(0.01)
                self.conn.close()
                filea.close()
                fileb.close()
            elif x_value=="2":
                data=self.conn.recv(65535)
                data=data.decode()
                filea=open(self.dirname+"//"+user+"//"+filename+".3.txt",'w')
                filea.write(data)
                time.sleep(0.01)
                data=self.conn.recv(65535)
                data=data.decode()
                fileb=open(self.dirname+"//"+user+"//"+filename+".4.txt",'w')
                fileb.write(data)
                time.sleep(0.01)
                self.conn.close()
                filea.close()
                fileb.close()
            else:
                data=self.conn.recv(65535)
                data=data.decode()
                filea=open(self.dirname+"//"+user+"//"+filename+".2.txt",'w')
                filea.write(data)
                time.sleep(0.01)
                data=self.conn.recv(65535)
                data=data.decode()
                fileb=open(self.dirname+"//"+user+"//"+filename+".3.txt",'w')
                fileb.write(data)
                time.sleep(0.01)
                self.conn.close()
                filea.close()
                fileb.close()
            sys.exit(1)
        
        elif option=="GET":
            print("GET function")
            user=self.conn.recv(65535)
            user=user.decode()
            time.sleep(0.01)
            print(user)
            list=os.listdir(self.dirname+"//"+user)
            print(len(list))
            
            if len(list)==0:
                self.conn.send("NILL".encode())
                time.sleep(0.01)
            else:
                self.conn.send("PRESENT".encode())
                time.sleep(0.01)
                
                self.conn.send(str(list).encode())
                time.sleep(0.01)
                
                next=self.conn.recv(65535)
                next=next.decode()
                print("Response from Client is:",next)
                
                if next=="SEND":
                    total=[]
                        
                    for i in list:
                        i=i.strip()
                        i=i.strip("'")
                        i=os.path.splitext(i)[0]+''
                        total.append(i)
                        print(i)
                        
                        self.conn.send(i.encode())
                        time.sleep(2)
                        
                        file1=open(self.dirname+"//"+user+"//"+i+".txt",'r')
                        file1data=file1.read(65535)
                        self.conn.send(file1data.encode())
                        time.sleep(2)
                        
             
        else:
            print("List function")
            user=self.conn.recv(65535)
            user=user.decode()
            time.sleep(0.01)
            print(user)
            list=os.listdir(self.dirname+"//"+user)
            print(len(list))
            
            if len(list)==0:
                self.conn.send("NILL".encode())
                time.sleep(0.01)
            else:
                self.conn.send("PRESENT".encode())
                time.sleep(0.01)
                
                self.conn.send(str(list).encode())
                time.sleep(0.01)
            
        
if __name__=="__main__":
    Server=Server()


