import requests

BASE = " http://127.0.0.1:5000/"

# response = requests.get(BASE + "helloworld")# what this is saying is send a get request to this base url/helloworld --- 
# #so any url that has the BASEE/hellowrd the end point will be hit 

# response = requests.get(BASE + "helloworld/ven/19")# what this is saying is send a get request to this base url/helloworld --- 
# #so any url that has the BASEE/hellowrd the end point will be hit 


# response = requests.get(BASE + "helloworld/tim")# what this is saying is send a get request to this base url/helloworld --- 
#so any url that has the BASEE/hellowrd the end point will be hit 


#using this for the put method
#response = requests.put(BASE + "video/1", {"likes":10, "name":"Welcome to python", "views":10}) #this is trying to pass in extra information as a form 
#print(response.json())


# input()
#after putting we get the what we have just inserted
# response = requests.get(BASE + "video/6") #this is trying to pass in extra information as a form 
# print(response.json())

# data = [
#     {"likes":10, "name":"Welcome to python", "views":10},
#     {"likes":50, "name":"Intro to Rest", "views":90},
#     {"likes":20, "name":" flask python", "views":40}
# ]


# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), data[i])  #this is trying to pass in extra information as a form 
#     print(response.json())



# input()
# response = requests.get(BASE + "video/6 ")#this is trying to pass in extra information as a form 
# print(response.json())



response = requests.patch(BASE + "video/2", {'views':1000, 'likes':2000})#this is trying to pass in extra information as a form 
print(response.json())

