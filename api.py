import serial

def printcheckin(post):
    msg = "<p>"+post["name"]
    people = post["with_tags"]
    if "data" in people:
        msg += " w/ "
        numpeople = len(people["data"])
        for j in range(0,numpeople):
            if j < numpeople-1:
                msg += people["data"][j]["name"]+", "
            else:
                msg += people["data"][j]["name"]
    return msg

def printnews(newsfeed, start, ser):
    for i in range(start,start+6):
        msg = ""
        post = newsfeed["data"][i]
        msg += post["from"]["name"].strip()+": "
        if "message" in post:
            msg += "\""+post["message"]+"\""
        if post["type"] == "link":
            if ("name" in post) and ("description" in post):
                msg += "<l>"+post["name"]+", "+post["description"]
        if post["type"] == "checkin":
            msg += printcheckin(post)

        msg = "".join([x if ord(x) < 128 else '?' for x in msg]) #strips non-ASCII characters
        ser.write(msg)
        print msg

def printitem(newsfeed, itemnum, ser):
    msg = ""
    post = newsfeed["data"][itemnum]
    msg += post["from"]["name"].strip()+": "
    try:
        if "message" in post:
            msg += "\""+post["message"]+"\""
        if post["type"] == "link":
            msg += "<l>"+post["name"]+", "+post["description"]
            msg = "".join([x if ord(x) < 128 else '?' for x in msg]) #strips non-ASCII characters
        if post["type"] == "checkin":
            msg += printcheckin(post)
        if "likes" in post:
            msg += "<l>"+post["likes"]["count"]
        if "comments" in post:
            comments = post["comments"]
            if "data" in comments:
                comments = comments["data"]
                numcomments = len(comments)
                for j in range(0,min(numcomments,6)):
                    comment = comments[j]
                    msg += "<c>"
                    msg += comment["from"]["name"]+": "
                    msg += "\""+comment["message"]+"\""
    except KeyError:
        msg += "<error>"
    ser.write(msg)
    print msg
