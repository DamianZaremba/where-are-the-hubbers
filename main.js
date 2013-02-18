$(document).ready(function(){
	var mapOptions = {
		center: new google.maps.LatLng(0, 0),
		zoom: 2,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.getElementById("map"), mapOptions);
	var infowindows = [];

	/* Load up the hubbers */
	$.getJSON('hubbers.js', function (data) {
		$.each(data, function(hubber, profile) {
			/*alert(hubber + ' -> ' + profile)
			document.write('<h1>' + hubber + '</h1>');
			document.write('<p>Lat: ' + profile['location_lat'] + '</p>');
			document.write('<p>Lng: ' + profile['location_lng'] + '</p>');
			document.write('<p>Name: ' + profile['name'] + '</p>');
			document.write('<p>Username: ' + profile['username'] + '</p>');
			document.write('<p>Avatar: ' + profile['avatar'] + '</p>');
			*/

			var marker = new google.maps.Marker({
				position: new google.maps.LatLng(profile['location_lat'], profile['location_lng']),
				title: profile['name']
			});

			var content = document.createElement("div");
			content.setAttribute('class', 'infowindow');
			content.innerHTML = "<h1>@" + profile['username'] + "</h1>" + 
								"<p><img src='" + profile['avatar'] + "' /></p>" +
								"<p>" + profile['name'] + "</p>" +
								"<p><a href='http://github.com/" + profile['username'] + ">GH Profile</a></p>";

			var infowindow = new google.maps.InfoWindow({
				content: content,
			});
			infowindows.push(infowindow);

			google.maps.event.addListener(marker, 'click', function () {
				$.each(infowindows, function(i, obj) { obj.close() });
				infowindow.open(map, marker);
			});
			marker.setMap(map);
		});
	});
});