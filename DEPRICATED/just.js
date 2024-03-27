
/*

    Testdatei zum setzen der Diagramme + dessen Einstellungen






*/






let soloOptions = {
    elements: {
        point: {
            radius: 6,
            pointStyle: 'rectRounded',
            backgroundColor: 'rgb(187, 189, 193)',    // 'rgba(0,156,74, 1)',
            borderColor: 'rgba(0,71,33,1)',
            hoverRadius: 10, // vergroessert Punkt beim Hovern auf diesen Radius
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
    labels: ['eins', 'zwei', 'drei', '4', '5', '6', '7', '8', '9', '10'],
    datasets: [{
        label: 'Solo/Duo',
        data: getRandomList(10, 20),
        
        }]
    }


let soloConfig = {
    type: 'line',
    data: soloData,
    options: soloOptions,
    
}








function main() {
    
    Chart.defaults.font.size = 14;
    let soloChartObject = document.getElementById('soloChart');
    let soloChart = new Chart(soloChartObject, soloConfig);

    let flexChartObject = document.getElementById('flexChart');
    let flexChart = new Chart(flexChartObject, {
        type: 'line',
        data: {
            labels: ['vier', 'fuenf', 'sechs'],
            datasets: [{
                label: 'meine Daten',
                data: [5, 6, 3]
                }]
            }
        });

}



//////////////////////////   RANDOM   ////////////////////////


function getRandomInt(max) {
    return Math.floor(Math.random() * max);
  }


function getRandomList(len, maxVal) {
    let list = [];
    for (let i=0; i<len; i++){
        list.push(getRandomInt(maxVal+1));
    }
    return list;
}



