var TitleTyping = function(el, text) {
    this.text = text+" ";
    this.el = el;
    this.i = 0;
    this.txt = '';
    classie.addClass(this.el, 'typing')
    this.tick();
}
  
TitleTyping.prototype.tick = function() {
    this.txt = this.text.substring(0, this.txt.length + 1);
    new_text = this.txt.replace(/ /g, "&nbsp");
    this.el.innerHTML = new_text;
    var delta = 200 - Math.random() * 100;
    if (this.text.substring(this.txt.length, this.txt.length + 1) === " " || this.text.substring(this.txt.length-1, this.txt.length) === " ") {
        delta *= 3; 
    }
    var that = this;
    if (this.txt != this.text) {
        setTimeout(function() {that.tick();}, delta);
    } else {
        setTimeout(function() {that.stop1();}, 400);
        setTimeout(function() {that.stop2();}, 3550);
    }
}

TitleTyping.prototype.stop1 = function() {
    classie.addClass(this.el, 'typing-end')
}

TitleTyping.prototype.stop2 = function() {
    classie.removeClass(this.el, 'typing-end')
    classie.removeClass(this.el, 'typing')
}
  
window.onload = function() {
    var elements = document.getElementsByClassName('title_text');
    for (var i=0; i<elements.length; i++) {
        var text = elements[i].getAttribute('data-text');
        new TitleTyping(elements[i], text);
    }
}