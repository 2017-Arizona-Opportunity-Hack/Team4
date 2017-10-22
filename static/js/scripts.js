var map;
var markers = [];

function print(str)
{
    document.getElementById('test').innerHTML = str;
}

function addMarker(lat, lng, c) {
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(lat, lng),
        map: map,
        icon: (c == 1) ? 'static/markers/blue_MarkerI.png' : 'static/markers/red_MarkerI.png'
    });
    markers.push(marker);
}

function initMap()
{
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 33.4402295, lng: -111.9295916},
        zoom: 13
    });
    map.setCenter(new google.maps.LatLng(37.6872, -97.3301));
    map.setZoom(5);
}

function openfile(type)
{
    document.getElementById("IMP" + type).innerHTML="<form action='opencsv/' method=post enctype=multipart/form-data><p><input type=file name=file><br/><br/><input type=submit value=Upload><input style='display: none' name=type value='" + type + "'/></form>";
}

function submitfilters()
{
    var type = (!document.getElementById('Tm1').checked && !document.getElementById('Tf1').checked) ? -1 : document.getElementById('Tf1').checked ? 1 : 0;
    var gender = (!document.getElementById('m1').checked && !document.getElementById('f1').checked) ? 'All' : document.getElementById('m1').checked ? 'Male' : 'Female';
    var state = document.getElementById('st').value;
    var location = document.getElementById('addr').value == "" ? "" : codeAddress();
    var location_range = document.getElementById('range').value;
    var age_max = document.getElementById('lg-age').value;
    var age_min = document.getElementById('sm-age').value;
    var method = $('#method').val();
    var date_min = (document.getElementById('datepicker1').value == "") ? "1/1/1970" : document.getElementById('datepicker1').value;
    var date_max = (document.getElementById('datepicker2').value == "") ? "1/1/9999" : document.getElementById('datepicker2').value;
    $.ajax({
        url: '/requests/',
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({
            gender: gender,
            state: state,
            location: location,
            loc_range: location_range,
            age_min: age_min,
            age_max: age_max,
            methods: $('#method').val(),
            date_min: date_min,
            date_max: date_max
        })
    }).done(function(data) {
        var arrayLength = data.length;
        $("#lure_info").prop("src", "../static/images/lure_info.png?" + new Date().valueOf());
        $("#day_time_stats").prop("src", "../static/images/day_time_stats.png?" + new Date().valueOf());
        for (var i = 0; i < markers.length; i++) {
          markers[i].setMap(null);
        }
        markers = [];
        for (var i = 0; i < arrayLength; i++) {
            if(type == -1)
            {
                addMarker(data[i][1][0], data[i][1][1], data[i][0])
            } else
            {
                if (data[i][0] == type)
                {
                    addMarker(data[i][1][0], data[i][1][1], data[i][0])
                }
            }
        }
    });
}

function ageSliderHandler() {
    if (parseInt(document.getElementById('sm-age').value) > parseInt(document.getElementById('lg-age').value)) {
        temp = document.getElementById('sm-age').value;
        document.getElementById('sm-age').value = document.getElementById('lg-age').value;
        document.getElementById('lg-age').value = temp;
    }
    document.getElementById('minage').innerHTML = "Min: " + document.getElementById('sm-age').value;
    document.getElementById('maxage').innerHTML = "Max: " + document.getElementById('lg-age').value;
}

function rangeSliderHandler() {
    document.getElementById('rnglbl').innerHTML = document.getElementById('range').value + " mi";
}

window.onload = function() {
    $( "#datepicker1" ).datepicker();
    $( "#datepicker2" ).datepicker();
}

var geocoder, moved;

moved = false;

function codeAddress() {
    var address = document.getElementById('addr').value;
    var data = $.ajax({
        url: 'http://maps.googleapis.com/maps/api/geocode/json',
        method: 'GET',
        async: false,
        data: {
            address: address,
            sensor: false
        }
    });
    return data.responseJSON.results[0].geometry.location;
}

function expandPlot(file) {
    if (!moved) {
        $('#map').width($('#map').width() - 250);
        $('#ana').width($('#ana').width() + 250);
        moved = true;
    }
    else {
        $('#map').width($('#map').width() + 250);
        $('#ana').width($('#ana').width() - 250);
        moved = false;
    }
}

function hidePlot() {
    document.getElementById("map").style.visibility='visible';
    document.getElementById("plt").style.visibility='hidden';
}