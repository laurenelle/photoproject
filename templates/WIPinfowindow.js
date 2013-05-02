var label1 = new InfoBox({
        content: "<div id='label1'> content{{photo.id}}})<br><small>Pane: floatPane (above)</small></div>",
        boxClass: "labelMap label1",
        disableAutoPan: true,
        position: new google.mapsLatLng({{photo.latitude}}, {{photo.longitude}}),
        closeBoxURL: "",
        isHidden: false,
        pane: "floatPane" ,    // Pane 2
        enableEventPropagation: true,
});
label1.setMap(_map);





google.maps.event.addListener(this._w, 'domready', function () {
$('#map .bubbleContent')
    .parent().parent().parent().prev()
    .css('borderRadius', 5);
});