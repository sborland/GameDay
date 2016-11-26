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
        console.log(get_game_data_url + "?" + $.param(pp))
        return get_game_data_url + "?" + $.param(pp);
    }
    self.get_game_data = function (id) {
        $.getJSON(get_game_url(id), function (data) {
            self.vue.game_data = data.game_data;
            console.log(self.vue.game_data);
        }) 
        $("#vue-div").show();
    };
    
    
    //gets gaming news from Reddit
    self.get_gaming_news = function () {
        console.log("HERE");
        $.getJSON(get_gaming_news_url, function (data) {
            self.vue.gaming_news = data.listofNews;
            self.vue.gaming_news_response = data.responseStatus;
            console.log(self.vue.gamingNewsResponse);
            console.log("done");
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
            game_data: {},
            gaming_news: [],
            gaming_news_response: 'error',
        },
        methods: {
            get_games: self.get_games,
            get_game_data: self.get_game_data,
            get_gaming_news: self.get_gaming_news,
        }

    });

    //Starts on the current month
    var d = new Date();
    var m = d.getMonth();
    var y = d.getFullYear();
    self.get_gaming_news();
    self.get_games(m+1,y);
    self.get_game_data(19441);
    
    $("#vue-div").show();
    
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
