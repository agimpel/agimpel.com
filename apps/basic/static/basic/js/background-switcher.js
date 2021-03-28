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

var assignBackground = function() {
    // set the new image url in css
    bg_object.css('background-image', 'url(' + backgrounds[i_background] + ')');

    // update the image switcher counter
    counter_object.text((i_background+1) + ' / ' + (number_backgrounds));

    // update the image title
    title_object.text(titles[i_background])
}



var incrementBackground = function() {
    i_background++;
    if (i_background >= number_backgrounds) {
        i_background = 0;
    }
    assignBackground();
};


var decrementBackground = function() {
    i_background--;
    if (i_background < 0) {
        i_background = number_backgrounds-1;
    }
    assignBackground();
};


var timer = function(){
    interval = setInterval(function(){incrementBackground();}, delay);
};

preload(backgrounds);
timer();

forward_object.click(function() {incrementBackground(); clearInterval(interval); timer()});
backward_object.click(function() {decrementBackground(); clearInterval(interval); timer();});