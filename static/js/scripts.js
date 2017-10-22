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
}

function openfile()
{
    document.getElementById("IMP").innerHTML="<input type='file'/>";
}