function onSearch(e) {
    e.preventDefault();
    let form = e.currentTarget;
    let id = $(form).attr('id');
    const tablename = $("#search-type :selected").val();
    let formData = $(form).serializeArray();
    
    sendSearchRequest(tablename, formData, id);
}

function sendSearchRequest(tablename, formData, id) {
    $('.page-loading').fadeIn(1000);

    var req = []

    for (var i=1; i < formData.length; i++) {
        if (formData[i].value != "") {
            req.push(formData[i])
        }
    }

    $.ajax("/search/" + tablename, {
        type: 'GET',
        data: req,
        success: function (data, status) {
            showData(data)
            onClear(id);
        },
        error: function (errorMessage) {
            toastr.error("failed to insert.");
        },
        complete: function () {
            $('.page-loading').fadeOut(1000);
        }
    });
}

function showData(data) {
    var searchContainer = $('#searchContainer')[0];
   
    while (searchContainer.firstChild){
        searchContainer.removeChild(searchContainer.firstChild);
    }

    var rowDiv = document.createElement("div");
        rowDiv.className = "row";
        var colDiv1 = document.createElement("div");
        colDiv1.className = "col-sm"
        var colDiv2 = document.createElement("div");
        colDiv2.className = "col-sm"
        var colDiv3 = document.createElement("div");
        colDiv3.className = "col-sm"
        var emptyMsg = document.createElement("div");

        var searchButton = document.createElement("button");
        searchButton.className = "btn btn-outline-primary";
        searchButton.innerText = "Search again";
        searchButton.addEventListener("click", function() {window.location.href = "/showSearch"} );

    if (data.data.length == 0) {
        emptyMsg.innerHTML = "Sorry, no results were found. ";
        colDiv2.appendChild(emptyMsg);
    }

    else {
        var dataTable = makeDataTable(data.data, data.cols);
        colDiv2.appendChild(dataTable);
    }

    colDiv2.appendChild(searchButton);
    rowDiv.appendChild(colDiv1);
    rowDiv.appendChild(colDiv2);
    rowDiv.appendChild(colDiv3);
    searchContainer.appendChild(rowDiv);
}

function makeDataTable(data, cols) {
    var table = document.createElement("table");
    let thead = table.createTHead();
    thead.className = "thead-dark";
    let row = thead.insertRow();
    for (let col of cols) {
        let th = document.createElement("th");
        let text = document.createTextNode(col.name);
        th.appendChild(text);
        row.appendChild(th);
      }

    
      for (let item of data) {
        let row = table.insertRow();
        for (var i=0; i < item.length; i++) {
          let cell = row.insertCell();
          let text = document.createTextNode(item[i]);
          cell.appendChild(text);
        }
      }
    
    return table;

}

$(document).ready(function () {
    $("#search-type").on('change', function(){
        const selectedType = $("#search-type :selected").val();
        $.ajax({
            url: 'http://localhost:5000/getFields',
            data: {"search-type": selectedType},
            type: 'GET',
            success: function(response){
                addQueryFields(response)

            },
            error: function(error){
                console.log(error);
            }
        });

    });

    function addQueryFields(colsData) {
        var newElement;


        var searchDiv = document.getElementById("query-fields");
        while (searchDiv.childNodes.length > 0) {
            searchDiv.removeChild(searchDiv.lastChild);
          }
        const br = document.createElement("br");

        searchDiv.appendChild(br);
        searchDiv.appendChild(br);


        for (var i=0; i< colsData.length; i++) {
            col = colsData[i]
            switch (col["type"]) {
                case "varchar":
                    newElement = document.createElement("input");
                    newElement.setAttribute("type", "text");
                    //newElement.setAttribute("placeholder", col["name"])


                    break;
                case "int":
                    newElement = document.createElement("input");
                    newElement.setAttribute("type", "number");
                    //newElement.setAttribute("placeholder", col["name"])

                    break;
                case "date":
                    newElement = document.createElement("input");
                    newElement.setAttribute("type", "date");
                    //newElement.setAttribute("placeholder", col["name"])
 
                    break;
            }
            newElement.className = "form-control"
            newElement.name = col["name"]

            var colDiv = document.createElement("div")
            colDiv.className = "col-lg-6"
            colDiv.innerHTML += col["name"]
            colDiv.appendChild(newElement)

            searchDiv.appendChild(colDiv);
            searchDiv.appendChild(br);
            searchDiv.appendChild(br);

        }
       
    }
});

