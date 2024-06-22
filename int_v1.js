/*
    Ideen: 
    - Zeitraum der gezeigten Daten skalieren (zB nur letzte 20 Games anzeigen)
        - auswahlknopf, bei dem 'alle', '25', '10' letzte games zur Auswahl steht
    - Hover ueber Punkt gibt Rang als EMERALD, IV, 4 LP an
    - Hintergrund ueber momentanem Rang blau faerben, alles darunter rot
    - auswahl von oft genutzten namen

*/
////////////////////////////////////   General Functions   /////////////////////////////////////////


// Eingabe des Textfeldes auslesen
function getNameInput() { // von inputButton
    const inputTxt = document.getElementById('inputText');

    console.log('inputText: ' + inputTxt.value);
    return inputTxt.value;

}

function useFetchDataForChart(playerData) {
    {
        inputName = getNameInput().split('#')[0]; // fuerteb (ohne #euw) erhalten
        let index = -1;

        for(let i=0; i < playerData.players.length; i++){ // prufe, ob JSON den eingegebenen Namen enthaelt
            if (inputName.toLowerCase() === playerData.players[i].name.toLowerCase()) {
                index = i;
                break;
            } 
        }

        if (index !== -1) { // es wurde ein entsprechender Spieler in der JSON gefunden

            soloChart.config.data.labels = createNeededLabels(playerData, index, 'solo');
            soloChart.config.data.datasets[0].data = playerData.players[index].solo.lp_number;
            soloChart.update();

            flexChart.config.data.labels = createNeededLabels(playerData, index, 'flex');
            flexChart.config.data.datasets[0].data = playerData.players[index].flex.lp_number;
            flexChart.update();

        }
    }
}


///////////////////////////////////   SEND/RECEIVE DATA   //////////////////////////////////////////


async function fetchToPython() {

    inputName = getNameInput(); // im Textfeld eingegebener Name
    pythonFile = 'http://localhost:8000/lp_tracker_v4.py';

    // stelle POST request an pythonFile, diese fuehrt lp_tracker aus und dieser updated die json Datei
    const response = await fetch(pythonFile, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'params': inputName})
    });
    return response;

}

async function fetchFromJSON() {
    const url = './player_list.json';
    const response = await fetch(url);
    const pData = await response.json();
    console.log('JSON Data: ' + pData);
    return pData;
};








////////////////////////////////////   Chart.js Functions   ////////////////////////////////////////



function createEmptyChart(queueType){ // erschafft leere Chart und fuegt sie im Canvas zur entsprechenden Queue hinzu
    let chartObject;
    let newChart;
    if (queueType === 'solo'){
        chartObject = document.getElementById('soloChart');
        newChart = new Chart(chartObject, soloConfig);
    }
    else if(queueType === 'flex'){
        chartObject = document.getElementById('flexChart');
        newChart = new Chart(chartObject, flexConfig);
    }

    return newChart;
}



function createNeededLabels(pData, ind, queueType){
    
    let neededLength;
    if(queueType === 'solo'){
        neededLength = pData.players[ind].solo.lp_number.length;
    }
    if(queueType === 'flex'){
        neededLength = pData.players[ind].flex.lp_number.length;
    }
    let ret = [];
    for(let i=1; i <= neededLength; i++) {
        ret.push(i.toString());
    }
    return ret;
}

function setChartDefaults() {
    Chart.defaults.font.family = 'Roboto';
    Chart.defaults.font.size = 14;

}




/////////////////////////////////   Chart.js Chart Configs   ///////////////////////////////////////




let soloOptions = {
    elements: {
        point: {
            radius: 5,
            pointStyle: 'rectRounded',
            backgroundColor: 'rgb(187, 189, 193)',    // 'rgba(0,156,74, 1)',
            borderColor: 'rgba(0,71,33,1)',
            hoverRadius: 8, // vergroessert Punkt beim Hovern auf diesen Radius
            hoverBorderWidth: 2
        },
        line: {
            tension: 0.3,
            borderColor: 'rgba(0,156,74, 1)',
            borderCapStyle: 'round', // Form des Endes der Linie
            fill: {
                target: 'start',    // TODO setzt die Farbe des hintergrundes
                above: 'rgba(127, 169, 177, 0.4)',   
              }
        }
    },
    animations: {
        tension: {
            duration: 5000,
            easing: 'linear',
            from: 0.3,
            to: 0.6,
            loop: true
        }
    },
    scales: {
        x: {
            title: {
                display: true,
                text: 'Gespielte Spiele',
            }
        },
        y: {
            title: {
                display: true,
                text: 'LP Score'
            }
        }
    },
    plugins: {
        legend: {
            labels: {
                font: {
                    family: 'Roboto',
                    size: 16,
                }
            }
        },
        tooltip: {
            // TODO custom tooltip (Anzeige beim Hovern) mit Rankanzeige
        }
    }
}


let soloData = {
    labels: ['0', '0', 'O'],
    datasets: [{
        label: 'Solo/Duo',
        data: [1, 1, 1],
        
        }]
    }


let soloConfig = {
    type: 'line',
    data: soloData,
    options: soloOptions,
    
}





///////////////// flex Options
let flexOptions = {
    elements: {
        point: {
            radius: 5,
            pointStyle: 'rectRounded',
            backgroundColor: 'rgb(187, 189, 193)',    // 'rgba(0,156,74, 1)',
            borderColor: 'rgba(84, 175, 217,1)', // Border des Punktes
            hoverRadius: 8, // vergroessert Punkt beim Hovern auf diesen Radius
            hoverBorderWidth: 2
        },
        line: {
            tension: 0.3,
            borderColor: 'rgba(30, 36, 96, 1)', // Farbe der Linie
            borderCapStyle: 'round', // Form des Endes der Linie
            fill: {
                target: 'start',    // TODO setzt die Farbe des hintergrundes
                above: 'rgba(127, 169, 177, 0.4)',   
              }
        }
    },
    animations: {
        tension: {
            duration: 5000,
            easing: 'linear',
            from: 0.3,
            to: 0.6,
            loop: true
        }
    },
    scales: {
        x: {
            title: {
                display: true,
                text: 'Gespielte Spiele',
            }
        },
        y: {
            title: {
                display: true,
                text: 'LP Score'
            }
        }
    },
    plugins: {
        legend: {
            labels: {
                font: {
                    family: 'Roboto',
                    size: 16,
                }
            }
        },
        tooltip: {
            // TODO custom tooltip (Anzeige beim Hovern) mit Rankanzeige
        }
    }
}


let flexData = {
    labels: ['0', '0', 'O'],
    datasets: [{
        label: 'Flex',
        data: [1, 1, 1],
        }]
    }


let flexConfig = {
    type: 'line',
    data: flexData,
    options: flexOptions,
    
}







///////////////////////////////////////   Main   ///////////////////////////////////////////////////


// 'Track Now' Button
function main() {
    
    document.getElementById('inputText').readOnly = true; // Eingabefeld ist unveraenderbar
    document.getElementById('inputButton').disabled = true; // loescht 'Track LP' Button
    document.getElementById('reloadButton').disabled = false; // macht reload klickbar

    setChartDefaults();
    soloChart = createEmptyChart('solo'); // erschafft leeres Diagramm, auf das spaeter die Daten der SoloQ uebertragen werden
    flexChart = createEmptyChart('flex');

    fetchToPython().then(response => {
        console.log(response);
        // nichts mit dem return value machen
    });

    fetchFromJSON().then(pData => useFetchDataForChart(pData));
}



// 'reset' Button
function resetCanvas() {
    soloChart.destroy();
    flexChart.destroy();

    document.getElementById('inputText').value = ''; // setzt Textfeld zurueck
    document.getElementById('inputText').readOnly = false; // wieder im Textfeld schreibbar
    document.getElementById('inputButton').disabled = false; // stellt Button wieder her
    document.getElementById('reloadButton').disabled = true; // deaktiviert reload Button, bis man wieder eine Eingabe macht
}


// 'reload' Button fuer aktualisiertes Diagramm
function reloadCanvas() { // aehnlich zu main, aktualisiert aber nicht die Daten in der JSON 
    soloChart.destroy();
    flexChart.destroy();

    soloChart = createEmptyChart('solo'); // erschafft leeres Diagramm, auf das spaeter die Daten der SoloQ uebertragen werden
    flexChart = createEmptyChart('flex');

    fetchFromJSON().then(pData => useFetchDataForChart(pData));

}

