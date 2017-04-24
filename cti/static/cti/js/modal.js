$(function() {
    $('#contact-button').click(function () {
        $.dialog({
            title: 'contact and information',
            content: 'Project was written for:'+
                     '<br>- credit with subject'+
                     '<br>- cloud computing for web application'+
                     '<br>- operation system for web application'+
                     '<br><br>In the same time, mobile application is developed'+
                     '<br>For now application is ready only for CTI building'+
                     '<br><br>Emergency number: 112'+
                     '<br>Municipal Police: 986'+
                     '<br>Energy Ambulance: 991'+
                     '<br>Gas Ambulance: 992'+
                     '<br>Police: 997'+
                     '<br>Fire brigade: 998'+
                     '<br>Emergency Medical Services: 999'+
                     '<br><br>Administration of CTI building:'+
                     '<br>- email: cti@adm.p.lodz.pl'+
                     '<br>- telephone: + 48 42 631 24 40',
            backgroundDismiss: true,
            columnClass: 'medium',
            type: 'red'
        });
    });
});