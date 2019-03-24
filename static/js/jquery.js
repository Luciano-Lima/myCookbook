$(document).ready(function () {

	/* Login Slider */
	$("#login-button").on("click", function() {
		$("#login").toggleClass("login-clicked");
		$("#login-button").toggleClass("login-clicked");
		$("#login").animate( {
			width: 'toggle'
		});
	});

});