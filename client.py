import requests
import json
import sys


"""
url has been defined so doesnt need to be passed into login as an argument
"""
url = "http://ll15a9h.pythonanywhere.com"

endpoints = {
    "list": url + "/api/list",
    "register": url + "/api/register",
    "logout": url + "/api/logout",
    "login": url + "/api/login",
    "logout": url + "/api/logout",
    "view": url + "/api/view",
    "average": url + "/api/average",
    "rate": url + "/api/rate",
}


session = requests.Session()


"""
This main function runs in an infinite loop waiting for commans, it takes in
a input as an arfument and the first argument 'argument[0]' will be the Command
such as list, view and rate
"""
def main():
    while(1):
        argument = input("Command:\n").split()

        if argument[0] == "exit":
            exit()
        if argument[0] == "quit":
            exit()
        elif argument[0] == "list":
            list()
        elif argument[0] == "register":
            register()
        elif argument[0] == "login":
            loginuser()
        elif argument[0] == "logout":
            logoutuser()
        elif argument[0] == "view":
            view()
        elif argument[0] == "average":
            average(argument)
        elif argument[0] == "rate":
            rate(argument)
        else:
            print("command does not exist")


"""
The list function lists all modules instabces and professors teach them
"""
def list():

    try:
        response = session.request("GET", endpoints["list"])
    except Exception:
        return "Error: request failed"

    body = json.loads(response.text)


    for i in body:
        code = i["module id"]
        modulename = i["module"]
        year = i["year"]
        semester = i["semester"]

        profs = ''
        for j in i['professors']:
            profs += j + ", "
        print((modulename) + "(" + (code) + ")"+ "\t Year:" + str(year) + "\t Semester:" + str(semester) + "\tTaught by:" + (profs) )
        # print("%5s %s %20d %10d %10s" % (code,modulename, year, semester, profs))
        print("-----------------------------------------------------------------------------------------------------------")


"""
The register function allpws someone to register to the web services but doesnt
log them in. uses a post methof to pass a dictionary of the relevent data to
a specified end point
"""
def register():

    username = input("Username:")
    email = input("Email:")
    password = input("Password:")

    params = {
        "username": username,
        "email": email,
        "password": password,
    }

    register_user = session.post(endpoints["register"], data=params)

    if register_user.status_code == 200:
        print("User has been registered succesfully, you may now attempt to login")
    else:
        print("Error: " +  str(register_user.status_code) + "\nMessage: " + (register_user.text))


"""
The login function passed a dictionary of username and password to the endpoint
which initiales a session for the user
"""
def loginuser():
    # define endpoint
    endpoint = endpoints["login"]
    # get user input
    username = input("Username: ")
    password = input("Password: ")
    dict = {
        "username": username,
        "password": password,
    }
    log_in = session.post(url = endpoint, data = dict)

    if (log_in.status_code == 200):
        print("Logged in")
    else:
        print("Error Status: " + str(log_in.status_code) + "\nMessage: " + (log_in.text))

"""
The logout functions connects to the logout endpoint to log a user out and
closes the session
"""
def logoutuser():
    endpoint = endpoints["logout"]
    log_out = session.get(url = endpoint)
    if (log_out.status_code == 200):
        print("User Logged out")
    else:
        print(f"Errror: Status  {log_out.status_code} \nMessage: {log_out.text}")

"""
the view function retirves data about the professior and their average rating
from the view endpoint
"""
def view():
    endpoint = endpoints["view"]
    view_ratings = session.get(url=endpoint)
    if view_ratings.status_code == 200:
        ratings = json.loads(view_ratings.text)
        for i in ratings:

            print("The rating for " + (i['name']) + " ("+ (i['code']) + ") is " + str(i['rating']))
    else:
        print("Error")

"""
The avaerage function retrives and average for a given professor and module.
"""
def average(argument):
    module_input = argument[2]
    professor_input = argument[1]

    # if input is empty
    # please provide input
    endpoint = endpoints["average"]
    dict = {
        "professor":professor_input,
        "module": module_input,
    }
    get_average = session.get(url = endpoint, params= dict)

    if get_average.status_code ==200:
        result = json.loads(get_average.text)
        print("The rating for" +  result['professor'] +" "+ ({result['code']}) +" is "+ (result['rating']) + "/5")
    else:
        print("Error " + str(get_average.status_code))

"""
The user provides 5 arguemtns which is wrapped in a dictionary, this data is
the passed to the end point to creare a Professor ratings
"""

def rate(argument):
    endpoint = endpoints["rate"]
    try:
        professor_id = argument [1]
        module_code = argument [2]
        year = argument [3]
        semester = argument [4]
        rating = argument [5]
    except IndexError:
        print ("Provide correct arguments")


    dict = {
        'professor_id':professor_id,
        'module_code':module_code,
        'year':year,
        'semester':semester,
        'rating':rating,
    }
    rate_prof = session.post(url = endpoint, data=dict)
    if rate_prof.status_code == 200:
        print("Rating has been made")
    else:
        print("Error")

if __name__ == "__main__":
    main()
