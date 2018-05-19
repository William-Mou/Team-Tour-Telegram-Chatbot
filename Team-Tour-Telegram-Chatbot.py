


# coding: utf-8

# Team-Tour-Telegram-Chatbot

# coding by William Mou

# coding on spring, 2018

import telepot
from telepot.loop import MessageLoop
import json
import random
import time

#自行更新 #自行更新 #自行更新
TOKEN =  ''#自行更新
password = '' #自行更新
manager = ''  #自行更新
#自行更新 #自行更新 #自行更新

bot = telepot.Bot(TOKEN)

# task[number<int>] = { ans:<string>, score:<int>, }
task = {'001':{'ans':'學長好帥','score':4}}
#hint[number<string>] = [hint1<string>,hint2<string>]
hint = {'001': ['交付第一個任務', '答案：學長好帥']}
# self[username<sting>] = {team<int>, score:<int>, }
self = {}
# team[team_number<int> = {members<list>, total<int>, task:[<int finish<bool>]}, bounus:<int>, }
team = {1:{
          #"task_number" : 0, 
          "members":[], 
          "total":0,
          "hint":[]},
        2:{
          #"task_number" : 0, 
          "members":[], 
          "total":0,
          "hint":[]},
        3:{
          #"task_number" : 0, 
          "members":[], 
          "total":0,
          "hint":[]},
        4:{
          #"task_number" : 0, 
          "members":[], 
          "total":0,
          "hint":[]},
        5:{
          #"task_number" : 0, 
          "members":[], 
          "total":0,
          "hint":[]},
        }

admins_list = []
chats = []
lock = False

# 列印訊息接收log
def print_msg(msg):
    print(json.dumps(msg, indent=4))

# 接收chat後執行：
def on_chat(msg):
    global admins_list, chats, lock
    # 得取基礎資料：訊息類型\聊天室總類\聊天室id
    header = telepot.glance(msg, flavor="chat")
    print_msg(msg)
    data=""
    chats.append(header[2])
    chats=list(set(chats))

    if header[0] == "text":
        text = msg["text"]
        username = msg["from"]["username"]
        try:
            userteam = self[username]["team"]
        except:
            print("err")
        # command
        if text.startswith("/"):
            command = text.lstrip("/")
            
            if command == "start":
                text = "OK， {}\n你準備好了...... 讓我們開始一場奇幻冒險ㄅ OwO"
                bot.sendMessage(header[2], text.format(msg["from"]["first_name"]))
                bot.sendMessage(header[2], "請先輸入您的組別 /team <阿拉伯數字>～\n請小心輸入，這會影響你的計分唷～")
                bot.sendMessage(header[2], "/ans <題號> <答案> 回傳任務答案\n/hint <題號> 回傳當題提示\n/total 獲取總計分\n/list 查看完整小隊資訊\n/score_board 查看記分板")
                
            elif command[:4] == "help":
                bot.sendMessage(header[2], "/ans <題號><答案> 回傳任務答案\n/hint <題號> 回當題提示\n/total 獲取總計分\n/list 查看完整小隊資訊\n/score_board 查看記分板")
            
            elif command[:11] == "score_board":
                send = "以下為所有小隊的分數！\n"
                ma = -1
                win = []
                for i in range(1,6):
                    send += "第" + str(i) + "小隊：" + str(team[i]["total"]) + "分\n"
                    if team[i]["total"] > ma:
                        ma = team[i]["total"]
                        win = []
                        win.append(i)
                    elif team[i]["total"] == ma:
                        win.append(i)
                winner = ' '
                for i in win:
                    winner += str(i) + ' '
                send += "恭喜第{}小隊以{}分獲得第一！\n".format(winner, ma)
                bot.sendMessage(header[2], send)
            
            elif command[:3] == "set":
                if username == manager:
                    admins_dict=bot.getChatAdministrators (msg['chat']['id'])
                    for i in admins_dict:
                        admins_list.append(i['user']['username'])
                    admins_list = list(set(admins_list))
                    bot.sendMessage(header[2], "There are admins_list : " + str(admins_list))

            # user設定組別
            elif command[:4] == "team":
                if lock == True:
                     bot.sendMessage(header[2], "小組變更已鎖定！！禁止變心！！")
                else:
                    data = command[4:].split()
                    data=int(data[0])
                    if username in self:
                        if username in team[data]["members"]:
                            bot.sendMessage(header[2], "ni已經註冊過ㄖ")
                        else:
                            self[username] = {"team" : data}
                            team[int(userteam)]["members"].remove(username)
                            team[data]['members'].append(username)
                            send = "Hello, Your new partner are :\n"
                            for j in team[data]["members"]:
                                send += "@"+str(j)+"\n"
                            bot.sendMessage(header[2], send)
                    else:
                        self[username] = {"team" : data}
                        team[data]['members'].append(username)
                        if len(team[data]["members"]) == 1:
                            bot.sendMessage(header[2], "You are the First!\nGo to help your other partners!")
                        if len(team[data]["members"]) == 2:
                            bot.sendMessage(header[2], "You are the Second!\nGo to help your other partners!")   
                        send = "Hello, Your new partner are :\n"    
                        for j in team[data]["members"]:
                            send += "@"+str(j)+"\n"
                        bot.sendMessage(header[2], send)
                    
            # manager 設定題目        
            elif command[:3] == "add":
                data = command[3:].split()
                if len(data) == 4:
                    if data[0] == password:
                        if data[2] == 'x':
                            data[2] = random.randrange(0, 1080503, 2)
                        task[data[1]] = {"ans" : data[2], "score" : int(data[3]) }
                        bot.sendMessage(header[2], "Thank you! We have add it to our data base.")
                    else:
                        bot.sendMessage(header[2], "Please enter the true password !")
                else:
                    bot.sendMessage(header[2], "Please enter the correct data!\n/add <password> <task_number> <task_answer> <task_score> !")

            # user answer the question                     
            elif command[:3] == "ans":
                data = command[3:].split()
                task_number = data[0]
                try:
                    task_answer = data[1]
                except:
                    if "ans" in task[task_number]:
                        bot.sendMessage(header[2], "請依照格式輸入您的答案 /ac 題號 答案")
                    else:
                        print("圖片")
                if (not task_number in team[userteam]) or (team[userteam][task_number] >=-3) or (team[userteam][task_number] <-3 and time.time() >= team[userteam]["penalty"]) :                        
                    if "ans" in task[task_number]:
                        if task[task_number]["ans"] == task_answer:
                            if task_number in team[userteam]:
                                if team[userteam][task_number] == 1:
                                    bot.sendMessage(header[2], "You have sended the correct answer...\nGo on to find the next task! ouo")
                                else:
                                    team[userteam][task_number] = 1
                                    team[userteam]["total"] += task[task_number]["score"]
                                    bot.sendMessage(header[2], "Congratulations! You answered the correct answer!\nGo on to find the next task!")
                            else:
                                team[userteam][task_number] = 1
                                team[userteam]["total"] += task[task_number]["score"]
                                bot.sendMessage(header[2], "Congratulations! You answered the correct answer!\nGo on to find the next task!")
                        else:
                            if task_number in team[userteam] and team[userteam][task_number] != 1:
                                if team[userteam][task_number] % 3 == 0:
                                    team[userteam]["penalty"] = time.time()+60
                                    team[userteam][task_number] -= 1
                                    bot.sendMessage(header[2], "You have sent too many answers,\nplease wait " + str(int(team[userteam]["penalty"]-time.time())) + " seconds and try again!")
                                else:
                                    team[userteam][task_number] -= 1
                                    bot.sendMessage(header[2], "Sorry... It's also not correct answer. QAQ")
                            else :
                                team[userteam][task_number] = -1
                                bot.sendMessage(header[2], "Sorry... It's not correct answer 0.0")
                    else:
                        bot.sendMessage(header[2], "答案已收到，請等候 admins 審核 ouo! #待審核")
                else:
                    bot.sendMessage(header[2], "You have sent too many answers,\nplease wait " + str(int(team[userteam]["penalty"]-time.time())) + " seconds and try again!")
            
            # user request the list of team info
            elif command[:4] == "list":
                for i in team[userteam]:
                    send = ""
                    if i == "members":
                        send += "partner : \n"
                        for j in team[userteam][i]:
                            send += '@' + str(j)
                            send += "\n"
                    elif i == "hint":
                        send = "你隊伍的提示使用狀況為：" + str(team[userteam]['hint'])
                    elif i == "total":
                        send = "你隊伍的總分為：" + str(team[userteam][i]) + "分"
                    elif i == "penalty":
                        send = "你的懲罰時間為：" + str(team[userteam][i]) + "秒"
                    else:
                        send = "第 " +str(i) + " 題通過！"
                    bot.sendMessage(header[2], send)
                    
            # user request the total score of team        
            elif command[:5] == "total":
                bot.sendMessage(header[2],"Your total score is "+ str(team[userteam]['total']) + ".")
            
            # /bonus <username> <score>
            elif command[:5] == "bonus":
                print(username)
                if username in admins_list:
                    data = command[5:].split()
                    bonus_user = data[0][1:]
                    bonus_score = int(data[1])
                    userteam = self[bonus_user]["team"]
                    team[userteam]["total"] += bonus_score
                    bot.sendMessage(header[2],"Congratulations! team " + str(userteam) + " got " + str(bonus_score) + " scores!")

            # /ac <username> <task_number>
            elif command[:2] == "ac":
                re_username = msg["reply_to_message"]["from"]["username"]
                userteam = self[re_username]["team"]
                data = msg["reply_to_message"]["text"].split()
                task_number = data[1]
                if username in admins_list:
                    if task_number in team[userteam]:
                        if team[userteam][task_number] == 1:
                            bot.sendMessage(header[2], "You have sended the correct answer...\nGo on to find the next task! ouo")
                    else:
                        team[userteam][task_number] = 1
                        team[userteam]["total"] += task[task_number]["score"]
                        bot.sendMessage(header[2], "Congratulations! team " + str(userteam) + " send the correct answer!")
                        
            elif command[:2] == "to":
                data = command[3:]
                if username in admins_list:
                    for chat in chats:
                        bot.sendMessage(chat,"各位，這兒有一筆來自虛空中的捲軸，請詳閱：\n" + str(data))
            
            #/hint <task_number>
            elif command[:4] == "hint":
                data = command[4:].split()
                if data in team[userteam]['hint']:
                    bot.sendMessage(header[2],hint[data[0]][1])
                    team[userteam]['total']-=3
                else:
                    bot.sendMessage(header[2],hint[data[0]][0])
                    team[userteam]['hint'].append(data)
                    team[userteam]['total']-=1
                    
            elif "@all" in msg["text"] or command[:3] == "all":
                admins_dict=bot.getChatAdministrators (msg["chat"]["id"])
                chat_name=msg["chat"]["title"].encode('utf8')
                print(admins_dict)
                send = ""
                for admin in admins_dict:
                    if 'username' in admin['user']:
                        send += '@'+str(admin['user']["username"])+"\n"
                bot.sendMessage(header[2],send)                    
                  
            elif command[:4] == "lock":
                if username in admins_list and lock == False:
                    lock = True
                    bot.sendMessage(header[2],"小隊變更已鎖定！")           
            elif command[:6] == "unlock":
                if username in admins_list and lock == True:
                    lock = False
                    bot.sendMessage(header[2],"小隊變更已解除！")   
        
MessageLoop(bot, {
    'chat': on_chat,
    #'callback_query': on_callback_query,
}).run_as_thread()

print('Listening ...')