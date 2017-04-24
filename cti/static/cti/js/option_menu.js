$(document).ready(function() {
    $('.fault-tr').click(function(event) {
        $("#options-modal").width("0px");
        $("#options-modal").show();
        var id = $(this).attr('id');
        var content = $('<div class="options-menu">'+
                            '<a href="/admin/fault_details/'+id+'" class="option-button details-button" title="details">'+
                                '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                    '<span class="glyphicon glyphicon-file"></span>'+
                                '</div>'+
                            '</a>'+
                            '<a href="/admin/edit_fault/'+id+'" class="option-button edit-button" title="edit">'+
                                '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                    '<span class="glyphicon glyphicon-pencil"></span>'+
                                '</div>'+
                            '</a>'+
                            '<a href="/admin/assign_to_me/'+id+'" class="option-button assign-button" title="assign to me">'+
                                '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                    '<span class="glyphicon glyphicon-plus"></span>'+
                                '</div>'+
                            '</a>'+
                            '<a href="/admin/delete_fault/'+id+'" class="option-button delete-button" title="delete">'+
                                '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                    '<span class="glyphicon glyphicon-trash"></span>'+
                                '</div>'+
                            '</a>'+
                        '</div>');
        $("#options-modal").html(content).offset({ top: event.pageY, left: event.pageX}).animate({width: "200px"});
    });

    $(document).click(function(event) {
        if(!$(event.target).hasClass('fault-td')) {
            $("#options-modal").hide();
        }
    });
});