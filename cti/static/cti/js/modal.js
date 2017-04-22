function contact() {
    $.dialog({
        title: 'contact',
        content: 'Projekt napisany pod katem <br>zaliczenia z przedmiotów:'+
                 '<br>- Przetwarzanie w chmurze <br>dla aplikacji mobilnych'+
                 '<br>- Systemy operacyjne na <br>platformach mobilnych.'+
                 '<br>Równolegle wykonywana jest aplikacja mobilna o tej samej tematyce, która będzie'+
                 'współpracowała z aplikacją webową.'+
                 '<br>Początkowo aplikacja zostanie wdrożona jedynie w Centrum Technologii Informatycznych'+
                 'w celach testowych.'+
                 '<br><br>Projekt będzie bazą dla pracy inżynierskiej.'+
                 '<br>Numery alarmowe:'+
                 '<br>- numer alarmowy: 112'+
                 '<br>- Pogotowie Rzeczne: 984'+
                 '<br>- Ratownictwo Morskie i Górskie: 985'+
                 '<br>- Straż Miejska: 986'+
                 '<br>- woj. zarządzanie kryzysowe: 987'+
                 '<br>- Pogotowie Energetyczne: 991'+
                 '<br>- Pogotowie Gazowe: 992'+
                 '<br>- Pogotowie Ciepłownicze: 993'+
                 '<br>- Pogotowie Wodociągowe: 994'+
                 '<br>- Policja: 997'+
                 '<br>- Straż Pożarna: 998'+
                 '<br>- Pogotowie Ratunkowe: 999'+
                 '<br><br>Kontakt z administracją Centrum Technologii Informatycznych:'+
                 '<br>- email: cti@adm.p.lodz.pl'+
                 '<br>- telefon: + 48 42 631 24 40',
        backgroundDismiss: true,
        columnClass: 'medium',
        type: 'dark'
    });
}