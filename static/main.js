window.onload = function() {
    var markers = document.getElementsByClassName('new-marker');
    for (var i = 0; i < markers.length; i++) {
        markers[i].addEventListener('mouseover', function() {
            this.style.textShadow = '0 0 10px #f00, 0 0 20px #f00, 0 0 30px #f00, 0 0 40px #f00';
        });
        markers[i].addEventListener('mouseout', function() {
            this.style.textShadow = '';
        });
    }
};
