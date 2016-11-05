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
    
    
     function get_gaming_url(month, year) {
        var pp = {
            month: month,
            year: year
        };
        console.log(get_games_url + "?" + $.param(pp))
        return get_games_url + "?" + $.param(pp);
    }
    //Gets the game that is coming out that month
    //month is a value between 01 to 12 (MUST INCLUDE THE 0 for the single digits)
    //year is any valid year value
    self.get_games = function (month,year) {
        console.log("HERE!")
        $.getJSON(get_gaming_url(month,year), function (data) {
            self.vue.game_list = data.game_list;
            console.log(self.vue.game_list);
        })
        
    };


    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            logged_in: false,
            game_list: [],
        },
        methods: {
            get_games: self.get_games,
        }

    });

    //Currently only gets November. Change values to get different months.
    self.get_games(11,2016);
    $("#vue-div").show();
    
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
