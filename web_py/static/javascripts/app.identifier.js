Identifier = {
	
	init: function() {
			
		// Fetch initial suggestion
		Identifier.submit(true);
		
		// Define form submission behavior
		$("li.identify form").submit(function(){
			Identifier.submit();
			return false;
		});
		
	},
	
	submit: function(first_time) {
		var q = first_time ? '' : $('li.identify form').serialize();
		var url = '/identify?' + q + '&callback=?';
		log('Identifier.submit to URL: ' + url);
		$.getJSON(url, function(data) {
			Identifier.handleResponse(data);
		});
	},

	handleResponse: function(response) {
		log("Identifier.handleResponse..");
		log(response);
		$('li.identify form input.hex').val(response.hexCode.replace('#', ''));
		$('li.identify form input.name').val('');
		$('li.identify div.swatch').css({backgroundColor:response.hexCode});
	}

};