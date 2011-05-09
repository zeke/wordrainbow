Visualizer = {

    init: function() {

        Visualizer.submit(true);

    },

    submit: function(first_time) {
        var url = '/visualize?callback=?';
        log('Visualizer.submit to URL: ' + url);
        $.getJSON(url,
        function(data) {
            Visualizer.handleResponse(data);
        });
    },

    handleResponse: function(response) {
        log("Visualizer.handleResponse...");
        log(response);
        var hexen = response.hexen;
        var colors = response.colors;
        colors.reverse();
        // var element = document.getElementById("test");
        // var table   = document.getElementById("testTable");
        // table.appendChild(document.createElement("tbody"));
        for (index in colors) {
            var color = colors[index];
            var node = document.createTextNode(color);
            $("li.visualize ul.names").append("<li>" + color + "</li>");
        }
        // for (hex in hexen) {
        //     var cell = document.createElement("tr");
        //     var txt  = document.createTextNode(hexen[hex]);
        //     table.appendChild(cell);
        //     cell.appendChild(txt);
        // h = hexen[hex]
        //            element.innerHTML += h + '<br />';

    }

};