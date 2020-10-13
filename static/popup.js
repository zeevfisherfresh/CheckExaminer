function runSwitchjs(html) {
    var name = document.getElementById("fname").value;
    fetch("data?name=" + name)
        .then(function(response) {
            if (response.status !== 200) {
                document.getElementById("result").innerHTML =
                    "Looks like there was a problem. Status Code: " + response.status;
                return;
            }

            response.json().then((json) => {
                const months = [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ];
                document.getElementById("result").innerHTML = html + `
        <div class='container'>
          <span class='container-title'>Examiner:</span>
          <span class='container-data'>${json["examiner_name"]} <br> (Stats based on ${json["examiner_apps_we_have"]} apps)</span>
        </div>
        <div class='container'>
          <span class='container-title'>Response success rate:</span>
          <span class='container-data'>${json["response_success_rate"]}</span>
        </div>
        <div class='container'>
          <span class='container-title'>Average eventual grant rate:</span>
          <span class='container-data'>${json["examiner_grant_rate"]}</span>
        </div>
        <div class='container'>
          <span class='container-title'>Average eventual grant rate with interview:</span>
          <span class='container-data'>${json["examiner_grant_rate_with_interview"]}</span>
        </div>
        <div class='container'>
          <span class='container-title'>Average eventual grant rate without interview:</span>
          <span class='container-data'>${json["examiner_grant_rate_without_interview"]} </span>
        </div>
        <div class='container'>
          <span class='container-title'>Interview benefit:</span>
          <span class='container-data'>${json["interview_improvement_rate"]}</span>
        </div>

        <div class='months'>
          <span class='months-title'>Success percentage rate by month</span>
          <canvas id="myChart" width="350" height="200"></canvas>
        </div>
        `;
                new Chart(document.getElementById("myChart"), {
                    type: "bar",
                    options: {
                        legend: {
                            display: false,
                        },
                    },
                    data: {
                        labels: months,
                        datasets: [{
                            backgroundColor: "rgb(40, 83, 184)",
                            borderColor: "rgb(40, 83, 184)",
                            data: months.map((month) => json["months"][month].slice(0, -1)),
                        }, ],
                    },
                });
            });
        })
        .catch(function(err) {
            console.log("Fetch Error :-S", err);
        });
}



function switchTab(evt, cityName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

function fillDataList() {
    fetch("list_examiners" + name)
        .then(function(response) {
            if (response.status !== 200) {
                document.getElementById("result").innerHTML =
                    "Looks like there was a problem. Status Code: " + response.status;
                return;
            }
            console.log(
                response.json().then((json) => {
                    console.log(json);
                    var container = document.getElementById("fname"),
                        i = 0,
                        dl = document.createElement("datalist");

                    dl.id = "dlCities";
                    for (var i = 0; i < json.length; i++) {
                        var obj = json[i];
                        var option = document.createElement("option");
                        option.value = obj;
                        dl.appendChild(option);
                    }
                    container.appendChild(dl);
                })
            );
        })
        .catch(function(err) {
            console.log("Fetch Error :-S", err);
        });
}
fillDataList();



function putResult(item, index) {

        var setButton = document.createElement("small");

      setButton.innerHTML = '<div class="header2" width="80px">  <table >  ' +
          '     <tr width="80%">  ' +
          '       <th width="50%"><div>' + item + '</div></th>  ' +
          '     </tr> '
          '   </table></div>';
      setButton.id = index;
      setButton.href = "#" + item;
      setButton.addEventListener("click", function() {
          get_apps(item);
      });
      document.getElementById("resultsa").appendChild(setButton).appendChild(document.createElement("br"));
}

function putApplication(item, index) {
    var lastEvent = ''
    let transactions = item['transactions']
    var description = ''
    for (var i = transactions.length - 1; i >= 0; --i) {
        let transaction = (transactions[i]);
        console.log(transaction['recordDate'])
        if (transaction['code'] == 'MCTFR' || transaction['code'] == 'MCTFR') {
            lastEvent = transaction['recordDate'].substring(0, 11);
            description = transaction['description']
        }
        if (transaction['code'] == 'A.NE' || transaction['code'] == 'SA..' || transaction['code'] == 'A.QU') {
            lastEvent = ''
            description = ''
        }
    }

    if (lastEvent != '') {

        console.log(lastEvent.replace(/-/g, "/"))
        var date1 = new Date(lastEvent.replace(/-/g, "/"));
        //date1 = new Date(date1.setMonth(date1.getMonth() + 6));
        date3 = new Date(date1.setMonth(date1.getMonth() + 3));
        date4 = new Date(date1.setMonth(date1.getMonth() + 4));
        date5 = new Date(date1.setMonth(date1.getMonth() + 5));
        date6 = new Date(date1.setMonth(date1.getMonth() + 6));
        
        var datenow = new Date();
        var deadline = date1;
        var diffDays = parseInt((date1 - datenow) / (1000 * 60 * 60 * 24), 10);
        console.log ("difference between now and office action")
        console.log (diffDays)

        if (diffDays > 0 && diffDays <90) {
            console.log ('no extension');
            deadline = new Date(date1.setMonth(date1.getMonth() + 3)); 
            console.log (deadline)
        }

        if (diffDays >= 90 && diffDays <120) {

            console.log ('1st extension')
            deadline = new Date(date1.setMonth(date1.getMonth() + 4)); 
            console.log (deadline)

        }

        if (diffDays >= 120 && diffDays <150) {

            console.log ('2st extension')
            deadline = new Date(date1.setMonth(date1.getMonth() + 5)); 
            console.log (deadline)

        }

        if (diffDays >= 150 && diffDays <180) {

            console.log ('3rd extension')
            deadline = new Date(date1.setMonth(date1.getMonth() + 6)); 
            console.log (deadline)

        }

        if (diffDays >= 180) {

            console.log ('Deadline missed')
            deadline = datenow; 
            console.log (deadline)


        }


        var setButton = document.createElement("small");
        setButton.innerHTML = '<div class="header2" width="80px">  <table >  ' +
            '     <tr width="80%">  ' +
            '       <th width="50%"><div>' + name + item['patentTitle'] + '</div></th>  ' +
            '       <th width="50%"> Deadline: ' + description + '</th>  ' +
            '     </tr>  ' +
            '     <tr width="80%">  ' +
            '       <th width="50%">' + '<div>' + lastEvent + '  |  ' + item['applId'] + '</div>' + '</th>  ' +
            '       <th width="50%">Deadline: ' + deadline + ' in ' + diffDays + ' days</th>  ' +
            '     </tr>' +
            '   </table></div>';
        setButton.id = index;
        setButton.href = "#" + item;
        setButton.addEventListener("click", function() {
            getExaminer(item['appExamName'], setButton.innerHTML);
        });
        document.getElementById("resultsa").appendChild(setButton).appendChild(document.createElement("br"));
    }
}

function putApplicationById(item, index) {
    console.log(item, index)
    var setButton = document.createElement("small");
    setButton.textContent = item['patentTitle'];
    setButton.id = index;
    setButton.href = "#" + item;
    setButton.addEventListener("click", function() {
        getExaminer(item['appExamName']);
    });
    document.getElementById("resultbyid").appendChild(setButton).appendChild(document.createElement("br"));
}

function addNextPageButton(name, page) {
    console.log(page)
    var setButton = document.createElement("button");
    setButton.textContent = "Search for more";
    setButton.id = "next";
    setButton.className = "button"
    setButton.addEventListener("click", function() {
        get_apps_page(name, page);
    });
    document.getElementById("resultsa").appendChild(setButton).appendChild(document.createElement("br"));
}


function getExaminer(examiner, html) {
    document.getElementById("fname").value = examiner
    document.getElementById("examtab").click()
    runSwitchjs(html)
}

function search_applicants() {
    switchTab(event, 'Applicants')
    var name = document.getElementById("applicant").value
    fetch('search_app?name=' + name)
        .then(
            function(response) {
                if (response.status !== 200) {
                    document.getElementById('resultsa').innerHTML = 'Looks like there was a problem. Status Code</td><td>' +
                        response.status
                    return;
                }

                console.log(response.json().then(json => {
                    document.getElementById("resultsa").innerHTML = ""
                    document.getElementById("resultsa").innerHTML += "<h3>Matching applicants:</h3>"
                    json.forEach(putResult)
                }))
            }
        )
        .catch(function(err) {
            console.log('Fetch Error :-S', err);
        });
}

document.getElementById('search_app').addEventListener('click', search_applicants);
document.getElementById('examtab').addEventListener('click', (event) => switchTab(event, 'Examiners'));
document.getElementById('apptab').addEventListener('click', (event) => switchTab(event, 'Applicants'));
document.getElementById('appidtab').addEventListener('click', (event) => switchTab(event, 'Applications'));
document.getElementById('abouttab').addEventListener('click', (event) => switchTab(event, 'About'));
switchTab(event, 'Applicants')

function get_apps(name) {
    console.log(name)
    fetch('get_apps?name=' + name)
        .then(
            function(response) {
                if (response.status !== 200) {
                    document.getElementById('resultsa').innerHTML = 'Looks like there was a problem. Status Code</td><td>' +
                        response.status
                    return;
                }

                console.log(response.json().then(json => {
                    console.log(json)
                    document.getElementById("resultsa").innerHTML = "Selected applicant: " + name + "<br/><br/>"
                    document.getElementById("resultsa").innerHTML += "<h3>Applications (" + json['queryResults']['searchResponse']['response']['numFound'] + "):</h3> <br>"
                    json['queryResults']['searchResponse']['response']['docs'].forEach(putApplication)
                    console.log(json)
                    addNextPageButton(name, json['page'] + 1)

                }))
            }
        )
        .catch(function(err) {
            console.log('Fetch Error :-S', err);
        });
}



function get_apps_by_id() {
    var name = document.getElementById("applicationid").value;
    fetch('get_apps_by_id?name=' + name)
        .then(
            function(response) {
                if (response.status !== 200) {
                    document.getElementById('resultbyid').innerHTML = 'Looks like there was a problem. Status Code</td><td>' +
                        response.status
                    return;
                }

                (response.json().then(json => {
                    console.log(json)
                    json['queryResults']['searchResponse']['response']['docs'].forEach(putApplicationById)
                }))
            }
        )
        .catch(function(err) {
            console.log('Fetch Error :-S', err);
        });
}

document.getElementById("search_app_by_id").addEventListener("click", get_apps_by_id);


function get_apps_page(name, page) {
    console.log(name)
    fetch('get_apps?name=' + name + "&page=" + page)
        .then(
            function(response) {
                if (response.status !== 200) {
                    document.getElementById('resultsa').innerHTML = 'Looks like there was a problem. Status Code</td><td>' +
                        response.status
                    return;
                }

                console.log(response.json().then(json => {
                    document.getElementById("resultsa").innerHTML = ""
                    document.getElementById("resultsa").innerHTML += "<h3>Applications for :</h3>"
                    json['queryResults']['searchResponse']['response']['docs'].forEach(putApplication)
                    addNextPageButton(name, page + 1)
                }))
            }
        )
        .catch(function(err) {
            console.log('Fetch Error :-S', err);
        });
}