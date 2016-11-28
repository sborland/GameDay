// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };
    
    
     //Gets the game that is coming out that month
    //month is a value between 01 to 12 (MUST INCLUDE THE 0 for the single digits)
    //year is any valid year value
    function get_gaming_month_url(month, year) {
        var pp = {
            month: month,
            year: year
        };
        //console.log(get_games_url + "?" + $.param(pp))
        return get_games_list_url + "?" + $.param(pp);
    }
   
    self.get_games = function (month,year) {
        $.getJSON(get_gaming_month_url(month,year), function (data) {
            self.vue.game_list = data.game_list;
           // console.log(self.vue.game_list);
        })  
    };
    
    
        
    //Given ID, returns game data
    function get_game_url(id) {
        console.log(id);
        var pp = {
            id: id
        };

        return get_game_data_url + "?" + $.param(pp);
    }
    self.get_game_data = function (id) {
        $.getJSON(get_game_url(id), function (data) {
            self.vue.game_data = data.game_data;
            self.vue.get_game_posts(0,'more',self.vue.game_data.id);
            console.log(self.vue.game_data);
        })
        self.vue.form_post_content="";
        $("#vue-div").show();
    };
    
    
    
    //Given game id and other info, adds game to user list 
    function add_game_list_url(id,name,thumb) {
        console.log(id);
        var pp = {
            id: id,
            name: name,
            thumb: thumb
        };
        console.log(add_game_to_userlist_url + "?" + $.param(pp))
        return add_game_to_userlist_url + "?" + $.param(pp);
    }
    self.add_game_list = function (id,name,thumb) {
        $.getJSON(add_game_list_url(id,name,thumb), function (data) {
            self.vue.game_data['game_in_list'] = 'minus';
            self.vue.game_data['game_likes'] = data.game_likes;
            self.vue.$set(self.vue,'user_game_list',data.game_list);
            self.vue.$set(self.vue,'user_game_list_size',data.game_list.length);
            //self.vue.user_game_list_size = self.vue.user_game_list_size+1;
            //self.vue.user_game_list = data.game_list;
           // console.log(self.vue.user_game_list);
        }) 
        self.vue.form_post_content="";
        //self.get_user_game_list();
        //self.get_game_data(id);
    };
    
    
    //Given game id, removes game from user's list 
    function rem_game_list_url(id) {
        console.log(id);
        var pp = {
            id: id
        };
        console.log(rem_game_from_userlist_url + "?" + $.param(pp))
        return rem_game_from_userlist_url + "?" + $.param(pp);
    }
    self.rem_game_list = function (id) {

        $.getJSON(rem_game_list_url(id), function (data) {
            self.vue.game_data['game_in_list'] = 'plus';
            self.vue.game_data['game_likes'] = data.game_likes;
            console.log(data.game_likes)
            self.vue.$set(self.vue,'user_game_list',data.game_list);
            self.vue.$set(self.vue,'user_game_list_size',data.game_list.length);

            //self.vue.user_game_list_size = self.vue.user_game_list_size-1;
            //console.log(self.vue.user_game_list);
        })
       
    };
    
    //gets the user personal's game list
    self.get_user_game_list = function () {
        
        $.getJSON(get_games_from_userlist_url, function (data) {
            self.vue.user_id=data.user_id;
            self.vue.$set(self.vue,'user_game_list',data.game_list);
            self.vue.$set(self.vue,'user_game_list_size',data.game_list.length);

        })

        $("#vue-div").show();
    };
    
    //Gets the posts for the current game selected
    function get_postings_url(curIndex,navi,game_id) {
        var pp = {
            curIndex:curIndex,
            navi :navi,
            game_id:game_id
        };
        return get_game_posts_url + "?" + $.param(pp);
    }
      self.get_game_posts = function (curIndex,navi,game_id) {
        $.getJSON(get_postings_url(curIndex, navi,game_id), function (data) {
            self.vue.game_posts = data.posts;
            self.vue.more_post = data.has_more;
            self.vue.less_post = data.has_less;
            self.vue.index_post = data.currentIndex;
        })
    };
    
    
    //adds a new post to the current game's postingss
    self.add_game_post = function (game_id) {
        var pp = {
            user_email: self.vue.user_id,
                post_content: self.vue.form_post_content,
                game_id: game_id,
        };
        var add_posting_url = add_game_post_url+ "?" + $.param(pp)
        $.post(add_posting_url, 
            function (data) {
                
                //self.post_button(false,null);

            });
            self.get_game_posts(0,'more',self.vue.game_data.id);
            form_post_content=null;
    };
    
     self.rem_game_post = function (post_id,game_id) {
        var pp = {
                post_id: post_id,
                game_id: game_id,
        };
        var rem_posting_url = rem_game_post_url+ "?" + $.param(pp)
        $.post(rem_posting_url, 
            function (data) {
            });
            self.get_game_posts(0,'more',self.vue.game_data.id);
    };
    
    
    
    
    //gets gaming news from Reddit
    self.get_gaming_news = function () {
        $.getJSON(get_gaming_news_url, function (data) {
            self.vue.gaming_news = data.listofNews;
            self.vue.gaming_news_response = data.responseStatus;
        }) 

    };
    
    


    //Vue stuff
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            logged_in: false,
            game_list: [],
            game_data: 'null',
            gaming_news: [],
            gaming_news_response: 'error',
            user_id: 'null',
            user_game_list: [],
            user_game_list_size:0,
            game_posts:[],
            form_post_content:null,
            more_post: false,
            less_post: false,
            index_post:0,
        },
        methods: {
            get_games: self.get_games,
            get_game_data: self.get_game_data,
            get_gaming_news: self.get_gaming_news,
            add_game_list: self.add_game_list,
            rem_game_list: self.rem_game_list,
            get_user_game_list: self.get_user_game_list,
            get_game_posts: self.get_game_posts,
            add_game_post:self.add_game_post,
            rem_game_post:self.rem_game_post
        }

    });

    //Starts on the current month
    var d = new Date();
    var m = d.getMonth();
    var y = d.getFullYear();
    self.get_games(m+1,y);
    self.get_gaming_news();
    self.get_user_game_list();
    $("#vue-div").show();
    
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
