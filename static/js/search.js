console.log("I'm runningg!")
$(document).ready(function () {
    $("#search-type").on('change', function(){
        const selectedType = $("#search-type :selected").val();
        console.log(selectedType)
        console.log("making ajax call")
        $.ajax({
            url: 'http://localhost:5000/getFields',
            data: {"search-type": selectedType},
            type: 'GET',
            success: function(response){
                console.log("success")
                console.log(response);
                addQueryFields(response)

            },
            error: function(error){
                console.log("oh no")
                console.log(error);
            }
        });

    });

    function addQueryFields(colsData) {
        var newElement;


        var searchDiv = document.getElementById("query-fields");

        console.log(searchDiv.childNodes.length)
        while (searchDiv.childNodes.length > 0) {
            console.log("removing")
            searchDiv.removeChild(searchDiv.lastChild);
          }
        const br = document.createElement("br");

        searchDiv.appendChild(br);
        searchDiv.appendChild(br);


        for (var i=0; i< colsData.length; i++) {
            col = colsData[i]
            console.log("col")
            console.log(col)
            switch (col["type"]) {
                case "varchar":
                    console.log("case 1")
                    newElement = document.createElement("input");
                    newElement.setAttribute("type", "text");
                    //newElement.setAttribute("placeholder", col["name"])


                    break;
                case "int":
                    console.log("case 2")
                    newElement = document.createElement("input");
                    newElement.setAttribute("type", "number");
                    //newElement.setAttribute("placeholder", col["name"])

                    break;
                case "date":
                    console.log("case 3")
                    newElement = document.createElement("input");
                    newElement.setAttribute("type", "date");
                    //newElement.setAttribute("placeholder", col["name"])
 
                    break;
            }
            newElement.className = "form-control"

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

