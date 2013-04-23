


var map;

function initialize() {
  var mapOptions = {
    zoom: 8,
    center: new google.maps.LatLng(-34.397, 150.644),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
 
  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);
}

google.maps.event.addDomListener(window, 'load', initialize);






        var myLatlng = new google.maps.LatLng('photo.latitude','photo.longitude');
        var mapOptions = {
        zoom: 11,
        center: myLatlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
        }
        // instantiate a marker object
        var marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        // alt text - 
        title:"ALT TEXT"
  });


        //caption
        var content = 'photo.caption';
        //instantiating a new infowindow for the marker
        var infoWindow = new google.maps.InfoWindow({content: content});

        google.maps.event.addListener(marker, 'click', function() {
            infoWindow.open(map, marker);
            });
      }
      google.maps.event.addDomListener(window, 'load', initialize);