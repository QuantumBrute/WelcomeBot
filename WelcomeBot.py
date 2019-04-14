import praw
import LoginInfo
import json
import time
#Created by u/QuantumBrute
    
data = []
itemname = []

print ("Starting Bot...")
print ("Logging in...")

#To login into reddit
reddit = praw.Reddit(client_id= LoginInfo.client_id,
		     client_secret= LoginInfo.client_secret,
		     username= LoginInfo.username,
		     password= LoginInfo.password,
		     user_agent= LoginInfo.user_agent)

print ("Logged in!")

print("Opening LastApprovedUser...")
with open('LastApprovedUser.txt', 'r') as infile:
    info = json.load(infile,)

subreddit = reddit.subreddit("TheApexCollective") # Defines which subreddit the bot should work on

print("Looking for new and unflaired users...")

def unflaired():
    n = len(info) + 1
    m = info[n-2].get("Number")
    mnew1 = m + 1
    #mnew2 = 0
    #mnew3 = 0
    print("Current number of existing users: " + str(m))
    flag = 0
    #check = 0
    checknew = 0
    for contributor1 in subreddit.contributor():
        for flair in subreddit.flair(redditor=contributor1):
            if flair.get("flair_text") == None:
                print("Unflaired user found!")
                itemname.append(contributor1)
                checknew = 1
            else:
                flag = 1
                break
        if flag == 1:
            break
    itemname.reverse()
    if checknew == 1:
        for a in range(len(itemname)):
            print(str(itemname[a]) + " will be flaired: Mortal ("  + str(mnew1) + "th)")
            newflair = ("Mortal (" + str(mnew1) + "th)")
            subreddit.flair.set(str(itemname[a]),newflair))
            itemfinal = { "Name" : str(itemname[a]), "Number" : mnew1}
            data.append(itemfinal)
            mnew1 = mnew1 + 1
        with open('LastApprovedUser.txt', 'w') as outfile:
            json.dump(data, outfile, indent=2)
        print("User appended successfully!")
        print("New number of existing users: " + str(mnew1 - 1))
             
    elif flag == 1:
        print("No new users found!")

    '''if n==1:
        for contributor2 in subreddit.contributor():
            itemname.append(str(contributor2))
        itemname.reverse()
        for x in range(len(itemname)):
            mnew2 = m + 1
            itemfinal = { "Name" : itemname[x], "Number" : mnew2}
            data.append(itemfinal)
            with open('LastApprovedUser.txt', 'w') as outfile:
                json.dump(data, outfile, indent=2)
        print("First Time!")
        print("Data added successfully")
        n = 0
    else:
        for y in range(len(info)):
            for contributor3 in subreddit.contributor():
                if contributor3 == info[y].get("Name"):
                    print("Users already in list!")
                    flag = 0
                    check = 1
                    break
                else:
                    flag = 1
            if flag == 1:
                itemname.append(str(contributor3))
            if check == 1:
                break
        if flag == 1:
            itemname.reverse()
            for x in range(len(itemname)):
                mnew3 = m + 1
                itemfinal = { "Name" : itemname[x], "Number" : mnew3}
                data.append(itemfinal)
                print("User Appended!")
                with open('LastApprovedUser.txt', 'w') as outfile:
                    json.dump(data, outfile, indent=2)
                print("Data added successfully")
        else:
            print("No data to add!")'''
   
while True:
    unflaired()
    print("Sleeping for 30 minutues!")
    time.sleep(30)


