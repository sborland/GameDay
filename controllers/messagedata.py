
import random, string,json 
#returns a list of emails of friends 
def get_chat_friends():
    curuser_email = db(db.auth_user.id==auth.user_id).select().first().email
    user_messages_pull = db(db.user_messages.user_email==curuser_email).select()
    emailList = []
    print user_messages_pull
    if user_messages_pull is not None:
        for row in user_messages_pull:
            post_user = db(db.auth_user.email == row.friend_email).select().first()
            post_name= post_user.first_name + ' ' + post_user.last_name
            friend = {'name':post_name,'email':str(row.friend_email)}
            emailList.append(friend)
       
    
    return response.json(dict(email_list=emailList))

#get the posts for a specific messaging chat
def get_chat_posts():
    user_email=request.vars.user_email
    friend_email=request.vars.friend_email
    post_list = []
    
    friend_user = db(db.auth_user.email == friend_email).select().first()
    friend_name =friend_user.first_name + ' ' + friend_user.last_name
    
    user_messages_entry = db((db.user_messages.user_email==user_email)&(db.user_messages.friend_email==friend_email)).select().first()
    list_games_chat = get_list_of_games_chat(user_email,friend_email)
    if user_messages_entry is not None:
        user_messages_pull = user_messages_entry.message_json
        for post in user_messages_pull:
            post_user = db(db.auth_user.email == post['user_email']).select().first()
            posts_name= post_user.first_name + ' ' + post_user.last_name
            
            if user_email == post['user_email']:
                    belong_to_user = True
            else:
                    belong_to_user = False
                    
            post = dict(
                    user_email = post['user_email'],
                    post_name = posts_name,
                    post_content = post['post_content'],
                    created_on = post['created_on'],
                    id = post['id'],
                    belongs_to_user = belong_to_user
                )
            post_list.append(post)
            post_list = sorted(post_list, key = lambda k: k['created_on'],reverse=True)
    return response.json(dict(posts=post_list,friend_name=friend_name,list_games_chat=list_games_chat))

def get_list_of_games_chat(user_email,friend_email):
    user_games_pull = db(db.user_games_list.user_id==user_email).select().first()
    friend_games_pull =  db(db.user_games_list.user_id==friend_email).select().first()

    if user_games_pull==None:
          user_games =[]
    else:
        user_games_dict =  json.loads(user_games_pull.games_list_json)
    if friend_games_pull==None:
          friend_games=[]
    else:
        friend_games_dict = json.loads(friend_games_pull.games_list_json)
    
    listofsamegames=[]
    for key in user_games_dict.keys():
        if key in friend_games_dict.keys():
            listofsamegames.append(friend_games_dict[str(key)]['name'])
    return listofsamegames      
    
    
    
#add post to specific chat
def add_chat_post():
    user_email=request.vars.user_email
    friend_email=request.vars.friend_email
    post_content=request.vars.post_content
    
    friend_user = db(db.auth_user.email == friend_email).select().first()
    friend_name= friend_user.first_name + ' ' + friend_user.last_name
    
    post = {}
    post['user_email']=user_email
    post['created_on']= datetime.datetime.utcnow()
    post['post_content']=post_content
    #generates random id for post 
    post['id']= ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
    
    
    user_messages_entry = db((db.user_messages.user_email==user_email)&(db.user_messages.friend_email==friend_email)).select().first()
    friend_messages_entry = db((db.user_messages.user_email==friend_email)&(db.user_messages.friend_email==user_email)).select().first()
    if (user_messages_entry is not None and friend_messages_entry is not None):
        message_list= user_messages_entry.message_json
        message_list.append(post)
        user_messages_entry.message_json = message_list
        friend_messages_entry.message_json = message_list
        user_messages_entry.update_record()
        friend_messages_entry.update_record()
    else:
         message_list=[]
         message_list.append(post)
         db.user_messages.insert(user_email=user_email,friend_email=friend_email,message_json=message_list)
         db.user_messages.insert(user_email=friend_email,friend_email=user_email,message_json=message_list)
    message_list = message_list[::-1]
    for message in message_list:
        if message['user_email'] == user_email:
              belong_to_user = True
              post_name="You"
        else:
              belong_to_user = False
              post_name=friend_name
        message['belongs_to_user']=belong_to_user
        message['post_name']=post_name
              
    return response.json(dict(posts=message_list))