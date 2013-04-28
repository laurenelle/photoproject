    <script type="text/javascript">



      function makeInfoWindowEvent(map, infowindow, marker) {  
        return function() {  
          infowindow.open(map, marker);
        };  
      } 

      function init() {
        var mapOptions = {
          center: new google.maps.LatLng(37.463, 122.255),
          zoom: 2,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

        {% for photo in photos %}

          var content{{photo.id}} = '<div><IMG BORDER="0" ALIGN="Left" SRC="{{photo.thumbnail}}"><p>{{photo.caption}}</p></div>';
          var marker{{photo.id}} = new google.maps.Marker({
            position: new google.maps.LatLng({{photo.latitude}}, {{photo.longitude}}),
            map: map,
          });
      
          var infoWindow{{photo.id}} = new google.maps.InfoWindow({content: content{{photo.id}}});
          google.maps.event.addListener(marker{{photo.id}}, 'click', 
            makeInfoWindowEvent(map, infoWindow{{photo.id}}, marker{{photo.id}}));



        {% endfor %}

      }

      google.maps.event.addDomListener(window, 'load', init);
    </script>


