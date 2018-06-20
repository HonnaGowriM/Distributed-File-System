
                          DFS programming assignament 4

  Overview
  ---------

  A distributed file system is implemented with 1 client and 4 servers. Fucntions such as PUT,GET and LIST is implemented.

  Python Version
  ---------------

  The python version used for the assignment is Python 3.6


  Method of Execution
  --------------------
  1.Run the client program with Client.py followed by the conf file name.
  
  2.Run the server program with Server.py followed by /DFS1(2,3,4) 10001(02,03,04)

  3.Input the required option according to the display.


  DFS
  ------------
  PUT
  1.User inputs the desired file that needs to be uploaded into the servers.

  2.With the hash value that's been generated the file is broken down into 4 chunks and uploaded according the table provided.

  3.Each user file is stored in his/her directory.

  GET
  1.The user inputs the desired file that needs to be retrived from the servers
 
  2.The file is downloaded at the client end only if the whole file chunks are present else no.

 LIST
  1.Displays the list of files present in the user folder.
