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

        console.log(searchDiv.childNodes.length)
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

