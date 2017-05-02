$(document).ready(function() {
    $('.fault-tr').click(function(event) {
        $("#options-modal").width("0px");
        $("#options-modal").show();
        let header = $(".body-header span").text().trim();
        let id = $(this).attr('id');

        if (header === gettext('resolved faults')) {
            var content = $('<div class="options-menu">'+
                                '<a class="option-button">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-option-horizontal"></span>'+
                                    '</div>'+
                                '</a>'+
                                '<a href="/admin/fault_details/'+id+'" class="option-button details-button" title="'+gettext('details')+'">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-file"></span>'+
                                    '</div>'+
                                '</a>'+
                                '<a href="/admin/restore_fault/'+id+'" class="option-button restore-button" title="'+gettext('restore')+'">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-share"></span>'+
                                    '</div>'+
                                '</a>'+
                                '<a class="option-button">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-option-horizontal"></span>'+
                                    '</div>'+
                                '</a>'+
                            '</div>');
        }
        else if (header === gettext('deleted faults')) {
            var content = $('<div class="options-menu">'+
                                '<a class="option-button">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-option-horizontal"></span>'+
                                    '</div>'+
                                '</a>'+
                                '<a href="/admin/fault_details/'+id+'" class="option-button details-button" title="'+gettext('details')+'">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-file"></span>'+
                                    '</div>'+
                                '</a>'+
                                '<a href="/admin/restore_fault/'+id+'" class="option-button restore-button" title="'+gettext('restore')+'">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-share"></span>'+
                                    '</div>'+
                                '</a>'+
                                '<a class="option-button">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-option-horizontal"></span>'+
                                    '</div>'+
                                '</a>'+
                            '</div>');
        }
        else if (header === gettext('faults assigned to me')) {
            var content = $('<div class="options-menu">'+
                                '<a href="/admin/fault_details/'+id+'" class="option-button details-button" title="'+gettext('details')+'">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-file"></span>'+
                                    '</div>'+
                                '</a>'+
                                '<a href="/admin/edit_fault/'+id+'" class="option-button edit-button" title="'+gettext('edit')+'">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-pencil"></span>'+
                                    '</div>'+
                                '</a>'+
                                '<a href="/admin/finish_fault/'+id+'" class="option-button finish-button" title="'+gettext('finish')+'">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-check"></span>'+
                                    '</div>'+
                                '</a>'+
                                '<a href="/admin/delete_fault/'+id+'" class="option-button delete-button" title="'+gettext('delete')+'">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-trash"></span>'+
                                    '</div>'+
                                '</a>'+
                            '</div>');
        }
        else {
            var content = $('<div class="options-menu">'+
                                '<a href="/admin/fault_details/'+id+'" class="option-button details-button" title="'+gettext('details')+'">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-file"></span>'+
                                    '</div>'+
                                '</a>'+
                                '<a href="/admin/edit_fault/'+id+'" class="option-button edit-button" title="'+gettext('edit')+'">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-pencil"></span>'+
                                    '</div>'+
                                '</a>'+
                                '<a href="/admin/assign_to_me/'+id+'" class="option-button assign-button" title="'+gettext('assign to me')+'">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-plus"></span>'+
                                    '</div>'+
                                '</a>'+
                                '<a href="/admin/delete_fault/'+id+'" class="option-button delete-button" title="'+gettext('delete')+'">'+
                                    '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                        '<span class="glyphicon glyphicon-trash"></span>'+
                                    '</div>'+
                                '</a>'+
                            '</div>');
        }

        $("#options-modal").html(content).offset({ top: event.pageY, left: event.pageX}).animate({width: "160px"});
    });

    $('.user-tr').click(function(event) {
        $("#options-modal").width("0px");
        $("#options-modal").show();
        let id = $(this).attr('id');

        var content = $('<div class="options-menu">'+
                            '<a href="/admin/user_details/'+id+'" class="option-button details-button" title="'+gettext('details')+'">'+
                                '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                    '<span class="glyphicon glyphicon-file"></span>'+
                                '</div>'+
                            '</a>'+
                            '<a href="/admin/edit_user/'+id+'" class="option-button edit-button" title="'+gettext('edit')+'">'+
                                '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                    '<span class="glyphicon glyphicon-pencil"></span>'+
                                '</div>'+
                            '</a>'+
                            '<a href="/admin/restore_user/'+id+'" class="option-button restore-button" title="'+gettext('restore')+'">'+
                                '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                    '<span class="glyphicon glyphicon-share"></span>'+
                                '</div>'+
                            '</a>'+
                            '<a href="/admin/block_user/'+id+'" class="option-button delete-button" title="'+gettext('block')+'">'+
                                '<div class="col-xs-3 col-sm-3 col-md-3 option">'+
                                    '<span class="glyphicon glyphicon-trash"></span>'+
                                '</div>'+
                            '</a>'+
                        '</div>');

        $("#options-modal").html(content).offset({ top: event.pageY, left: event.pageX}).animate({width: "160px"});
    });

    $(document).click(function(event) {
        if(!$(event.target).hasClass('fault-td') && !$(event.target).hasClass('user-td') ) {
            $("#options-modal").hide();
        }
    });
});