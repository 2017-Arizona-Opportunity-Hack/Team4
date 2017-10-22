var map;
var marker;

function print(str)
{
    document.getElementById('test').innerHTML = str;
}

function addMarker() {
    map.setCenter(new google.maps.LatLng(33.4340698,-111.9041857));
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(33.4340698,-111.9041857),
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
    $.ajax({
        url: '/requests/',
        type: 'POST',
        datatype: 'JSON',
        data: {
            A: document.getElementById('A').value
        }
    }).done(function(data) {
        console.log(data)
    });
}