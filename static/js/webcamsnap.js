Webcam.set({
  width: 320,
  height: 240,
  image_format: 'jpeg',
  jpeg_quality: 90
});
Webcam.attach( '#my_camera' );
var webcamdiv = document.getElementById('my_camera');
var results = document.getElementById('results')
var overlay = document.createElement('div');
overlay.setAttribute('id', 'overlay');
webcamdiv.appendChild(overlay);
var userdirectory = "False";
var imgnmb = 0;

function take_snapshot() {
  // take snapshot and get image data
  Webcam.snap( function(data_uri) {
    // display results in page
    $('#results').css('visibility', 'visible');

      var data = {'imgdata': data_uri, 'userdirectory': userdirectory, 'imgnmb': imgnmb+1};
      $.post(URL, data, function(response){
                    let userdata = JSON.parse(response);
                    let userUrl = userdata["user_url"];
                    userdirectory = userdata["userdirectory"];
                    imgnmb = userdata["imgnmb"];

                    $('#convertedimage').prop('src', userUrl);
                    $('#decisiondiv').css('visibility', 'visible');
                    $('#overlay').remove();
                    var overlay = document.createElement('div');
                    overlay.setAttribute('id', 'overlay');
                    webcamdiv.appendChild(overlay);
                    var imgbox = document.getElementById('imgbox');
                    var overlay2 = document.createElement("div");
                    overlay2.setAttribute('id', 'overlay2');
                    $('#overlay2').css('background-image', 'url("/media/' + userdirectory + '/' + 'userimage' +imgnmb+ '.jpg")');

                    imgbox.appendChild(overlay2);

                    $('#overlay').css('background-image', 'url(static/img/overlay' + imgnmb + '.png)');
                    imgnmb2 = imgnmb - 1;
                    document.getElementById('overlay2').innerHTML = '<img src="/static/img/overlay'+imgnmb2+'.png">';


          });
  });
  converted = document.getElementById('converted');
  converted.style.visibility = 'visible';
}

function delete_and_try_again() {
  imgnmb = 0
}
