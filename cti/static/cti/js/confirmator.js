function confirm_reporting_phone_number() {
    let validation = true;

    if (validation) {
        $.confirm({
            title: gettext('confirm!'),
            content: gettext('are you sure you want to report phone number??'),
            type: 'red',
            buttons: {
                confirm: function () {
                    window.location.replace($("#report-number").attr("href"))
                },
                cancel: function () {
                }
            }
        });
    }

    return false;
}

function confirm_asking_for_reassigning() {
    let validation = true;

    if (validation) {
        $.confirm({
            title: gettext('confirm!'),
            content: gettext('are you sure you want to ask for reassign??'),
            type: 'red',
            buttons: {
                confirm: function () {
                    window.location.replace($("#ask-for-reassign").attr("href"))
                },
                cancel: function () {
                }
            }
        });
    }

    return false;
}