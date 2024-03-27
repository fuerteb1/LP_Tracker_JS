



function getButtonInfo() { // von inputButton
    const inputTxt = document.getElementById('inputText');

    console.log(inputTxt.value);
    return inputTxt.value;

}

// DEPRICATED
function sendToPython() { // sendet eingegebenen Namen zum Python script und fuehrt es aus
    
    let playerName = getButtonInfo();
    
    console.log('starte py');
    let xhr = new XMLHttpRequest();
    let url = 'http://localhost:8000/lp_tracker_v4.py'; 
    let dataToSend = JSON.stringify({params: playerName});
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function() {
        if(xhr.readyState === 4 && xhr.status === 200) {
            // Erfolgreiche Antwort erhalten
            console.log('Antwort von Python: erfolgreich');
            updateChart(playerName); // name#tag

        }
    };
    xhr.onerror = function() {
        console.error('AJAX-Post fehlgeschlagen');
    };

    xhr.send(dataToSend);
    console.log('wurde gesendet');
    
}




///////////   update Chart   ///////////////////


async function fetchData() {
        const url = './player_list.json';
        const response = await fetch(url);
        const playerData = await response.json();
        console.log(playerData);
        return playerData;
    };





function updateChart(inputText) {

    let inputTextName = inputText.split('#')[0];
    console.log('before fetch');


    
    fetchData().then(playerData => {
        let ind = -1;

        for (let i = 0; i < playerData.players.length; i++) {
            if (inputTextName === playerData.players[i].name) { // prueft, ob der eingegebene Name einem in der JSON-Datei matched
                ind = i;
                break;
            }
            console.log('name: ' + playerData.players[i].name)
        }

        if (ind === -1) { // falls kein entsprechender Spieler gefunden wurde
            console.log('Es wurde kein Spieler mit diesem Namen gefunden');
        }
        else {
            lpChart.config.data.labels = retNumberOfLabels(playerData.players[ind].solo.lp_number, playerData.players[ind].flex.lp_number);
            lpChart.config.data.datasets[0].data = playerData.players[ind].solo.lp_number; // solo lp nummern 
            lpChart.config.data.datasets[1].data = playerData.players[ind].flex.lp_number;


           lpChart.update(); 
        }


    });

}





function retNumberOfLabels(lpListSolo, lpListFlex) {
    let retList = [];
    let maxListe = lpListSolo;
    if (lpListSolo.length < lpListFlex.length) {
        maxListe = lpListFlex;
    }

    for (let i = 1; i <= maxListe.length; i++) {
        retList.push(i.toString());
    }

    return retList;
};




////////////////////////////////   Chart Info   ////////////////////////////////////////////////////


let xData = { // alle Daten, die das Diagramm nutzt
    labels: ['eins', 'zwei'], // x-Achse
    datasets: [
        {
            label: 'Solo/Duo', // Titel des Diagramms
            data: [1, 2, 3], // Werte
            backgroundColor: 'rgba(133, 237, 188, 0.4)', // hellgruen
            borderColor: 'rgba(240, 192, 48, 1)', //gold
            borderJoinStyle: 'round',
            borderWidth: 4,
            fill: true, // macht den backgroundColor sichtbar
            hoverBackgroundColor: 'rgba(240, 192, 48, 1)', // gold
            hoverBorderColor: 'rgba(59, 196, 255, 1)', // hellblau
            pointRadius: 10,
            showLine: false
        }, {
            label: 'Flex',
            data: [3, 4, 5],
            borderWidth: 3,
            
            pointRadius: 3,
            backgroundColor: 'rgba(33, 69, 145, 0,4)',
            borderColor: 'rgba(144, 196, 71, 0,1)'

        }
    ]
}

let xConfig = { // Alle Einstellungen / Informationen des Diagramms
    type: 'line', // Diagrammart
    data: xData,
    options: {
        scales: {
            y: {
                beginAtZero: false
            }
        }
    }
}


let docChart = document.getElementById('LPTracker') // verbindung von der hier generierten Chart zur Darstellung im canvas tag
let lpChart = new Chart(docChart, xConfig); // Chart erstellen

















