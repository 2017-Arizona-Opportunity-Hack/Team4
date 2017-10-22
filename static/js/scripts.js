var map;
var marker;

function print(str)
{
    document.getElementById('test').innerHTML = str;
}

function addMarker(lat, lng) {
    map.setCenter(new google.maps.LatLng(33.4340698,-111.9041857));
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(lat, lng),
        map: map,
        icon: 'static/markers/blue_MarkerI.png'
    });
    console.log(marker);
}

function initMap()
{
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 33.4402295, lng: -111.9295916},
        zoom: 13
    });
    if(navigator.geolocation)
    {
        navigator.geolocation.getCurrentPosition(function(pos) {
            map.setCenter(new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude))
        });
    }
}

function openfile()
{
    document.getElementById("IMP").innerHTML="<form action='opencsv/' method=post enctype=multipart/form-data><p><input type=file name=file><br/><br/><input type=submit value=Upload></form>";
}

function submitfilters()
{
    var gender = (!document.getElementById('m1').checked && !document.getElementById('f1').checked) ? 'All' : document.getElementById('m1').checked ? 'Male' : 'Female';
    var state = document.getElementById('st').value;
    var location = document.getElementById('addr').value;
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
        console.log(data)
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

function codeAddress(address) {
    geocoder = new google.maps.Geocoder();
    geocoder.geocode({
        'address': address
    }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location)
        }
    });
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