$(document).ready(function() {
    $('.menu-button').click(function(event) {
        $('.menu-button').removeClass('selected');
        $(this).addClass('selected');
        event.preventDefault();
    })
});