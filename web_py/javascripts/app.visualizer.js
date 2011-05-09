Visualizer = {
    
    init: function() {
        
        Visualizer.submit(true)
        
    }
    
    submit: function(first_time) {
        var url = '/visualize?callback=?';
        log('Visualizer.submit to URL: ' + url);
        $.getJSON(url, function(data) {
			Visualizer.handleResponse(data);
		});
    },
    
    handleResponse: function(results) {
        log("Visualizer.handleResponse...");
        // log(results);
        var node=document.createTextNode("hello world!");
        log(node);
        // document.getElementById("test").appendChild(node);
        $("#test").appendChild(node);
    },
}
