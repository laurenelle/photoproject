// http://secretlab.thegreenspatula.net/pd/airDealMapper/airDealMapper.html
<script>
function $(x) {
  return document.getElementById(x);
}

var geocoder;
var map;
var results = [];
var destinationMarkers = [];
var destinationInfoWindows = [];

function initialize() {
  geocoder = new google.maps.Geocoder();

  var latlng = new google.maps.LatLng(37.69716666666667, -122.446));
  
  var myOptions = {
  zoom: 4,
  center: latlng,
  mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  
  map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
}

function createMarkerAndWindow(address, details, url, i) {
  geocoder.geocode({'address': address + ' airport'}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        var marker = new google.maps.Marker({
          map: map,
              position: results[0].geometry.location
              });

        destinationMarkers[i] = marker;

        var content = '<div class="infoWindow">' + details + '<br/>' + 
          '<a href="' + url + '">See this deal</a></div>';
        var infoWindow = new google.maps.InfoWindow({content: content});

        google.maps.event.addListener(marker, 'click', function() {
            infoWindow.open(map, marker);
            });

        destinationInfoWindows[i] = infoWindow;
      } else {
        alert("Geocode was not successful for the following reason: " + address + status);
      }
    });
}

function deleteMarkers() {
  if (destinationMarkers) {
    for (var i in destinationMarkers) {
      destinationMarkers[i].setMap(null);
    }
  }
}

function displayResults(rawResults) {
  var dealListing = document.getElementById('dealListing'); 
  
  dealListing.innerHTML = '';
  deleteMarkers();

  for (var i = 0; i < rawResults.Result.length; i++) {
    results[i] = rawResults.Result[i];

    var orig = results[i].OriginAirportCode;
    var dest = results[i].DestinationAirportCode;
    var startdate = results[i].StartDate;
    var enddate = results[i].EndDate;
    var price = '$' + results[i].Price + '0';
    var url = results[i].Url;

    var detailsString = '<span class="price">' + price + '</span>' +
      orig + ' to ' + dest + '<br/>' +
      startdate + ' - ' + enddate;

    createMarkerAndWindow(dest, detailsString, url, i);
    // CAPTION
    dealListing.innerHTML += '<a href="' + url + '" id="dealListing' + i + '">' + 
      '<li>' + detailsString + '</li></a>'; 
  }
}

function stopDefaultAction(e) {
    e.preventDefault();

    var form = document.getElementById('dealForm');
    var weekendValue = '';

    for (var i = 0; i < form.weekend.length; i++) {
      if (form.weekend[i].checked) {
        weekendValue = form.weekend[i].value;
      }
    }

    var rawParameters = {
    'apikey' : 'pf4xna45a4d446qq6c6vrnzu',
    'format' : 'json',
    'orig' : document.getElementById('orig').value,
    'dest' : document.getElementById('dest').value,
    'startdate' : document.getElementById('startdate').value,
    'enddate' : document.getElementById('enddate').value,
    'duration' : document.getElementById('duration').value,
    'weekend' : weekendValue,
    'limit' : 10,
    'diversity' : 'destairport'
    }

    var parameters = '';

    if (rawParameters.startdate != '' && rawParameters.enddate != '') {
      rawParameters.duration = '';
    }

    if ((rawParameters.orig != '' && rawParameters.dest != '') || 
        (rawParameters.orig == '' && rawParameters.dest == ''))  {
      rawParameters.diversity = '';
    }

    for (var key in rawParameters) {
      parameters += '&' + key + '=' + rawParameters[key];
    }

    var url = 'http://api.hotwire.com/v1/deal/air?' + parameters;

    console.log(url);

    var xmlhttp;

    if (window.XMLHttpRequest) {
      xmlhttp = new XMLHttpRequest();
    } else {
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4) {
            var rawResults = eval('(' + xmlhttp.responseText + ')');

            if (rawResults.Result[0]) {
              displayResults(rawResults);
            } else {
              var dealListing = document.getElementById('dealListing');
              dealListing.innerHTML = '<p>Sorry, no flight deals were found.</p>' +
              '<p>Try broadening your search parameters.</p>';
            }
        }
    }

    xmlhttp.open('GET', 'proxy.php?url=' + encodeURIComponent(url), true);
    xmlhttp.send();
}

$('orig').focus();
</script>
