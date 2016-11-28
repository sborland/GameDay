# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime


db.define_table('post',
                Field('user_email', default=auth.user.email if auth.user_id else None),
                Field('post_content', 'text'),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('updated_on', 'datetime', update=datetime.datetime.utcnow()),
                )

                
db.define_table('user_games_list',
    Field('user_id', default=auth.user.email if auth.user_id else None),
    Field('games_list_json', 'text'), # user's personal list of games, in json form (list of game IDs)
)

db.define_table('user_messages',
    Field('user_email', default=auth.user.email if auth.user_id else None),
    Field('friend_email'),
    Field('message_json', 'json'), # user's personal list of messages
)

db.define_table('games',
    Field('game_id'), #used to differentiate row for games 
    Field('game_likes_json', 'json'), # list of users that "liked" the game
    Field('game_postings_json','json'),
)

# I don't want to display the user email by default in all forms.
db.post.user_email.readable = db.post.user_email.writable = False
db.post.post_content.requires = IS_NOT_EMPTY()
db.post.created_on.readable = db.post.created_on.writable = False
db.post.updated_on.readable = db.post.updated_on.writable = False

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
