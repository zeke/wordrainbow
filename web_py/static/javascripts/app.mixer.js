Mixer = {
	hue: 500,
	saturation: 500,
	lightness: 500,
	current_color_name: null,
	results: null,
	circles: null,
	
	init: function() {
		$("#hue_slider").slider({
			max:1000,
			value: 500,
			slide: function(event, ui) { Mixer.hue = ui.value; Mixer.refreshAppearance(); }
		});
		$("#saturation_slider").slider({
			max:1000,			
			value: 500,
			slide: function(event, ui) { Mixer.saturation = ui.value; Mixer.refreshAppearance(); }
		});
		$("#lightness_slider").slider({
			max:1000,
			value: 500,
			slide: function(event, ui) { Mixer.lightness = ui.value; Mixer.refreshAppearance(); }
		});
		
		// Initialization
		Mixer.refreshAppearance();
		
		// Fetch initial suggestion
		Mixer.submit(true);
		
		// Define form submission behavior
		$("li.mix form").submit(function(){
			Mixer.submit();
			return false;
		});
		
	},

	// Called..
	// - at runtime
	// - when a slider is moved
	// - after a JSON response comes back
	refreshAppearance: function() {
		// Convert color from HSL to hex
		var color = $.colors([Mixer.hue/1000, Mixer.saturation/1000, Mixer.lightness/1000], 'array3Normalized', "HSL").toString('hex');		
		// Update form inputs
		$('li.mix form input.hex').val(color.replace('#', ''));
		$('li.mix form input.submit').css({ backgroundColor: color, color: (Mixer.lightness < 500 ? 'white' : 'black') });
		$('li.mix form input.name').css({color:color});
	},

	submit: function(first_time) {
		var q = first_time ? '' : $('li.mix form').serialize();
		var url = '/mix?' + q + '&callback=?';
		log('Mixer.submit to URL: ' + url);		
		$.getJSON(url, function(data) {
			Mixer.handleResponse(data);
		});
	},
	
	skipColor: function() {
		var url = '/mix?&callback=?';
		log('Mixer.skip: ' + url);
		$.getJSON(url, function(data) {
			Mixer.handleResponse(data);
		});
	},
	
	showResults: function() {
		$('ul#sliders').fadeOut();
		$('li.mix form input.submit').fadeOut();
		$('li.mix form a.skip').fadeOut();
		$('li.mix form a.hint').fadeOut();
		$('ul#slider_labels').fadeTo('normal', 0, function() {

			Mixer.circles = new Array();
			var d = 30; // diameter
			var duration = 500 + (Math.random() * 4000);
			var w = $(window).width();
			var h = $(window).height();
			var paper = Raphael(0, 0, w, h);
			
			// TODO: find out what's wrong. take a bite outta crime!
			for (i in Mixer.results) {
				var circle = paper.circle(
					d + Math.random() * w-(d*2), // random x not too close to edges
					d + Math.random() * h-d, // random y not too close to edges
					d
				);
				circle.attr("fill", Mixer.results[i]);
				circle.attr("stroke", Mixer.results[i]);
				circle.attr("opacity", 0);
				circle.attr("scale", .5);
				circle.animate({opacity: 1, scale: 1}, duration, ">");
				
				Mixer.circles.push(circle); // keep track
			}
			
			setTimeout('Mixer.revealLinkToNextColor()', 1000);
		});

	},
	
	revealLinkToNextColor: function() {
		$('li.mix a.next_color').fadeIn('slow');
	},
	
	skip: function() {
		
	},
	
	nextColor: function() {
		$('li.mix a.next_color').hide();

		$('li.mix form input.name').fadeOut();
		
		for (i in Mixer.circles) {
			var circle = Mixer.circles[i];
				var duration = 500 + (Math.random() * 1000);
				
				circle.animate(
					{
						"30%": {scale: 2, easing: ">"},
						"100%": {scale: 0, easing: "<", callback: function() { this.remove(); } }
					},
					duration
				);
			
		}
		
		setTimeout("Mixer.revealForm()", 1500);
	},
	
	revealForm: function() {
		Mixer.updateNameInput();
		$('li.mix form input.name').fadeIn();
		$('li.mix form input.submit').fadeIn();
		$('li.mix form a.skip').fadeIn();
		$('li.mix form a.hint').fadeIn();
		$('ul#sliders').fadeIn();
		$('ul#slider_labels').fadeTo('normal', 1);
	},
	
	updateNameInput: function() {
		$('li.mix form input.name').val(Mixer.current_color_name);
		$('li.mix form a.hint').attr('href', "http://wordnik.com/words/"+Mixer.current_color_name);
	},

	handleResponse: function(response) {
		// log("Mixer.handleResponse..");
		log(response);
		
		Mixer.current_color_name = response.nextName;
		Mixer.results = response.tagsForQuery;
		
		$('li.mix form input.hex').val('');
		
		
		// Show results unless this is the first response
		// or this user was the first to mix this color.
		if (Mixer.results.length > 1) {
			Mixer.showResults();
		} else {
			Mixer.updateNameInput();
			Mixer.refreshAppearance();
		}
		
	}

};