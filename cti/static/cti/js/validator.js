$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="tooltip"]').on('shown.bs.tooltip', function () {
        $('.tooltip').addClass('animated tada');
    })
});

function validateFault() {
    let validation = true;

    let phone_number = document.getElementById("phone_number");
    let object_number = document.getElementById("object_number").value;
    let topic = document.getElementById("topic").value;
    let description = document.getElementById("description").value;

    let phone_number_alert = document.getElementById("phone_number_alert");
    let object_number_alert = document.getElementById("object_number_alert");
    let topic_alert = document.getElementById("topic_alert");
    let description_alert = document.getElementById("description_alert");

    let object_number_regex = new RegExp("^([0-9]{10})$");
    let phone_number_regex = new RegExp("^([+]?[1]?[0-9]{9,15})$");

    if (phone_number) {
        if (!phone_number.value) {
            validation = false;
            $('#phone_number').attr('data-original-title', gettext('phone number is required'))
                .tooltip('fixTitle')
                .tooltip('show');
        }
        else {
            if (!phone_number_regex.test(phone_number.value)) {
                validation = false;
                $('#phone_number').attr('data-original-title', gettext('allowed phone number format: +999999999 (9-15 digits with possible plus)'))
                    .tooltip('fixTitle')
                    .tooltip('show');
            }
            else {
                $('#phone_number').tooltip('hide');
            }
        }
    }

    if (!object_number) {
        validation = false;
        $('#object_number').attr('data-original-title', gettext('object number is required'))
                           .tooltip('fixTitle')
                           .tooltip('show');
    }
    else {
        if (!object_number_regex.test(object_number)) {
            validation = false;
            $('#object_number').attr('data-original-title', gettext('allowed object number format: 9999999999 (10 digits)'))
                               .tooltip('fixTitle')
                               .tooltip('show');
        }
        else {
            $('#object_number').tooltip('hide');
        }
    }

    if (!topic) {
        validation = false;
        $('#topic').attr('data-original-title', gettext('topic is required'))
                   .tooltip('fixTitle')
                   .tooltip('show');
    }
    else {
        if (topic.length > 50) {
            validation = false;
            $('#topic').attr('data-original-title', gettext('allowed topic max length: 50 signs'))
                       .tooltip('fixTitle')
                       .tooltip('show');
        }
        else {
            $('#topic').tooltip('hide');
        }
    }

    if (!description) {
        validation = false;
        $('#description').attr('data-original-title', gettext('description is required'))
                         .tooltip('fixTitle')
                         .tooltip('show');
    }
    else {
        if (description.length > 200) {
            validation = false;
            $('#description').attr('data-original-title', gettext('allowed description max length: 200 signs'))
                             .tooltip('fixTitle')
                             .tooltip('show');
        }
        else {
            $('#description').tooltip('hide');
        }
    }

    if (validation) {
        $.confirm({
            title: 'confirm!',
            content: gettext('are you sure you want to do this??'),
            type: 'red',
            buttons: {
                confirm: function () {
                    $('#fault-form').submit();
                },
                cancel: function () {
                }
            }
        });
    }
}

function validateUser() {
    let validation = true;

    let first_name = document.getElementById("first_name").value;
    let last_name = document.getElementById("last_name").value;
    let email = document.getElementById("email").value;

    let name_regex = new RegExp("^([A-Z][a-z]+)$");
    let email_regex = new RegExp("^(\\S+@\\S+)$");

    if (!first_name) {
        validation = false;
        $('#first_name').attr('data-original-title', gettext('first name is required'))
                        .tooltip('fixTitle')
                        .tooltip('show');
    }
    else {
        if (!name_regex.test(first_name)) {
            validation = false;
            $('#first_name').attr('data-original-title', gettext('first name must have first capital letter and rest lowercase'))
                            .tooltip('fixTitle')
                            .tooltip('show');
        }
        else {
            $('#first_name').tooltip('hide');
        }
    }
    if (!last_name) {
        validation = false;
        $('#last_name').attr('data-original-title', gettext('last name is required'))
                       .tooltip('fixTitle')
                       .tooltip('show');
    }
    else {
        if (!name_regex.test(last_name)) {
            validation = false;
            $('#last_name').attr('data-original-title', gettext('last name must have first capital letter and rest lowercase'))
                           .tooltip('fixTitle')
                           .tooltip('show');
        }
        else {
            $('#last_name').tooltip('hide');
        }
    }
    if (!email) {
        validation = false;
        $('#email').attr('data-original-title', gettext('email is required'))
                   .tooltip('fixTitle')
                   .tooltip('show');
    }
    else {
        if (!email_regex.test(email)) {
            validation = false;
            $('#email').attr('data-original-title', gettext('email must have \'@\' sign and any white space'))
                       .tooltip('fixTitle')
                       .tooltip('show');
        }
        else {
            $('#email').tooltip('hide');
        }
    }

    if (validation) {
        $.confirm({
            title: 'confirm!',
            content: gettext('are you sure you want to do this??'),
            type: 'red',
            buttons: {
                confirm: function () {
                    $('#user-form').submit();
                },
                cancel: function () {
                }
            }
        });
    }
}

function validatePassword() {
    let validation = true;

    let old_password = document.getElementById("old_password").value;
    let new_password = document.getElementById("new_password").value;
    let new_password_repeat = document.getElementById("new_password_repeat").value;

    if (!old_password) {
        validation = false;
        $('#old_password').attr('data-original-title', gettext('field is required'))
                          .tooltip('fixTitle')
                          .tooltip('show');
    }
    else {
        $('#old_password').tooltip('hide');
    }
    if (!new_password) {
        validation = false;
        $('#new_password').attr('data-original-title', gettext('field is required'))
                          .tooltip('fixTitle')
                          .tooltip('show');
    }
    else {
        $('#new_password').tooltip('hide');
    }
    if (!new_password_repeat) {
        validation = false;
        $('#new_password_repeat').attr('data-original-title', gettext('field is required'))
                                 .tooltip('fixTitle')
                                 .tooltip('show');
    }
    else {
        $('#new_password_repeat').tooltip('hide');
    }

    if (validation) {
        $.confirm({
            title: 'confirm!',
            content: gettext('are you sure you want to do this??'),
            type: 'red',
            buttons: {
                confirm: function () {
                    $('#password-form').submit();
                },
                cancel: function () {
                }
            }
        });
    }
}