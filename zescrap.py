https://discord.com/channels/437048931827056642/437062563620978708/909606373996761089

https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension

https://stackoverflow.com/questions/3206344/passing-html-to-template-using-flask-jinja2



{% if token not in completedString or username in adminList: %}





@app.route('/mockcontest', methods = ['GET', 'POST'])
def mockcontest():
    global problems
    global answers
    global username
    if db[username][1] == False:
        return render_template('mockcontest.html', problems = problems, qname = None, submitted = db[username][1], username = username, email=db[username][3])
    elif request.method == 'GET' and db[username][1] == False and db[username][2] == False:
        print('Hello')
        req = request.form
        score = 0
        for i in range(len(answers)):
            if str(req.get('Q' + str(i))) == answers[i]:
                score = score + 1 
        u = [db[username][0], True, score]
        db[username] = u
        print('Just completed')
        return render_template('submitted.html', score = score)
    elif request.method == 'GET' and db[username][1]:
        print(db[username][1])
        print("Prev Completed")
        return render_template('submitted.html', score = db[username][2])
    elif request.method == 'POST':
        f = open("submissions.txt", 'r')
        info = f.read()
        response = "  [" + username + ", " + db[username][3] + " , ◼︎→  "
        req = request.form
        for i in range(0,len(problems)):
          iden = "Q" + str(i)
          ans = req.get(iden)
          response = response + ans + " | "
        response = response + "]  \n"
        f = open("submissions.txt", 'w')
        info = info + response
        f.write(info)
        return render_template('submitted.html')
