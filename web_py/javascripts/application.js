$(document).ready(function(){
	
	panel_width = 800;
	panel_height = 400;
	panel_padding = 5;
	panels = new Array('home', 'mix', 'identify', 'visualize');
	current_panel = panels[0];
		
	adaptToScale();	
	setTimeout("adaptToScale()", 250);
	setTimeout("adaptToScale()", 500);
	setTimeout("adaptToScale()", 1000);
	setTimeout("showHome()", 300);
	
	Mixer.init();
	Identifier.init();
});


$(window).resize(function() {
	adaptToScale();
});

function showHome() {
	$('li.home').css({visibility:'visible',display:'none'});	
	$('li.home').fadeIn(1500);
}

function adaptToScale() {
	
		// Make #panels wide enough to hold all the panels (plus extra for safety)
		// and as tall as the screen minus scrollbars
		$('ul#panels').width($(window).width() * panels.length + 100);
		$('ul#panels').height($(window).height() - $(window).scrollTop());

		// Get screen size (now that panel has been expanded as necessary)
		var panel_x_margin = ($(window).width() - panel_width)/2;
		var panel_y_margin = ($(window).height() - $(window).scrollTop() - panel_height)/2;

		// Give each panel enough margin to center itself.
		$('ul#panels > li').css({
			marginLeft: panel_x_margin,
			marginRight: panel_x_margin,
			marginTop: panel_y_margin,
			marginBottom: panel_y_margin
		});
		
		// Logo left justified above panel
		$('#logo').css({
			left: panel_x_margin,
			top: panel_y_margin - $('#logo').outerHeight()
		});
		
		// Logo right justified above panel		
		$('#nav').css({
			right: panel_x_margin,
			top: panel_y_margin - $('#nav').outerHeight()
		});

		// Center the footer at the bottom of the screen
		$('#footer').css({
			left: $(window).width()/2 - $('#footer').outerWidth()/2,
			bottom: 0
		});
		
		// Adjust panel arrangment without using animation
		Panel.switchTo(current_panel, true);

		// HOME
		// **********************************************************		
		$('li.home a').css({
			left: $('li.home').outerWidth()/2 - $('li.home a').width()/2,
			top: $('li.home').outerHeight()/2 - $('li.home a').height()/2
		});

		// MIX
		// **********************************************************
		$('li.mix ul#sliders').css({
			top: $('li.mix input.name').outerHeight(),
			left: 0
		});
		
		$('li.mix a.next_color').css({
			top: $('li.mix input.name').outerHeight(),
			left: 0
		});

		
		$('li.mix ul#slider_labels').css({
			top: $('li.mix ul#sliders').position().top + $('li.mix ul#sliders').outerHeight(),
			left: 0
		});
		
		// $('li.mix form').css({
		// 	top: 0,
		// 	left: 0
		// });
		// 
		// $('li.mix form input.name').css({
		// 	left: panel_padding,
		// 	top: panel_padding,
		// 	width: panel_width - (panel_padding*2)
		// });
		
}

Panel = {
	
	switchTo: function(panel_name, instant){
		current_panel = panel_name;
		var offset = panels.indexOf(panel_name);
				
		// Highlight active nav item
		$('#nav a').removeClass('active');
		$('#nav a.'+panel_name).addClass('active');
		
		// zero is the home panel
		// so turn off the nav'n stuff
		if (offset == 0) {
			$('#logo').fadeOut();
			$('#nav').fadeOut();
		} else {
			$('#logo').fadeIn();
			$('#nav').fadeIn();
		}

		if (instant) {
			$('#panels').css(
				{left: -$(window).width()*offset}
			);			
		} else {
			$('#panels').animate(
				{left: -$(window).width()*offset},
				"slow",
				'easeInOutCubic',
				function() {
				}
			);
		}


	}
};



// Logging function that accounts for browsers that don't have window.console
function log(m) {
	if (window.console) console.log(m);
}