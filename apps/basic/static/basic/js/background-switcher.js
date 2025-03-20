var bg_object = $('#home-wrapper');
var counter_object = $('#switcher-counter');
var title_object = $('#switcher-title');
var forward_object = $('#switcher-forward');
var backward_object = $('#switcher-backward');


var number_backgrounds = backgrounds.length;
var delay = 5000;

function preload(arrayOfImages) {
    $(arrayOfImages).each(function () {
        $('<img />').attr('src',this).appendTo('body').css('display','none');
    });
}


var resetOpacity = function() {
    // set the opacity of the before element to 0
    bg_object.css('--beforeOpacity', 0);
}


var assignBackground = function(i) {
    bg_object.css('background-image', 'url(' + backgrounds[i] + ')');
    counter_object.text((i+1) + ' / ' + (number_backgrounds));
    title_object.text(titles[i]);

    // reset the opacity of the before element to 0
    setTimeout(function() {
        resetOpacity();
    }
    , 100);
}


var changeBackground = function() {
    // set the opacity of the before element to 1
    bg_object.css('--beforeOpacity', 1);

    // wait for 200 ms, then change the background
    setTimeout(function() {
        assignBackground(i_background);
    }
    , 200);
}



var incrementBackground = function() {
    i_background++;
    if (i_background >= number_backgrounds) {
        i_background = 0;
    }
    changeBackground();
};


var decrementBackground = function() {
    i_background--;
    if (i_background < 0) {
        i_background = number_backgrounds-1;
    }
    changeBackground();
};


var timer = function(){
    interval = setInterval(function(){incrementBackground();}, delay);
};

preload(backgrounds);
timer();

forward_object.click(function() {incrementBackground(); clearInterval(interval); timer()});
backward_object.click(function() {decrementBackground(); clearInterval(interval); timer();});