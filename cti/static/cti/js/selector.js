$(document).ready(function() {
    $('.menu-button').click(function(event) {
        $('.menu-button').removeClass('selected');
        $(this).addClass('selected');
        event.preventDefault();
    })
});

$(document).ready(function() {
    $('#language-select').niceSelect();
});