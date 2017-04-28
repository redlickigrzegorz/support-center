$(function() {
    $('#contact-button').click(function () {
        $.dialog({
            title: 'contact and information',
            content: gettext('Project was written for:')+
                     '<br>'+gettext('- credit with subject')+
                     '<br>'+gettext('- cloud computing for web application')+
                     '<br>'+gettext('- operation system for web application')+
                     '<br><br>'+gettext('In the same time, mobile application is developed')+
                     '<br>'+gettext('For now application is ready only for CTI building')+
                     '<br><br>'+gettext('Emergency number: 112')+
                     '<br>'+gettext('Municipal Police: 986')+
                     '<br>'+gettext('Energy Ambulance: 991')+
                     '<br>'+gettext('Gas Ambulance: 992')+
                     '<br>'+gettext('Police: 997')+
                     '<br>'+gettext('Fire brigade: 998')+
                     '<br>'+gettext('Emergency Medical Services: 999')+
                     '<br><br>'+gettext('Administration of CTI building:')+
                     '<br>'+gettext('- email: cti@adm.p.lodz.pl')+
                     '<br>'+gettext('- telephone: + 48 42 631 24 40'),
            backgroundDismiss: true,
            columnClass: 'medium',
            type: 'red'
        });
    });
});