$("#form-user-address").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = 'https://trilong0610.pythonanywhere.com/customer/change_address/'

    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
                showToastr(data);

           },
            error: function (data) {
                showToastr(data);
            },
         });


});

$("#form-user-info").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = 'https://trilong0610.pythonanywhere.com/customer/change_info/'

    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
               showToastr(data);
           },
            error: function (data) {
                showToastr(data);
            },
         });


});

// Add the following code if you want the name of the file appear on select
$(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

//--------CROP AVATAR---------
/* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
$("#user_avatar").change(function () {
    if (this.files && this.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#image").attr("src", e.target.result);
        $("#modalCrop").modal("show");
      }
      reader.readAsDataURL(this.files[0]);
    }
});

/* SCRIPTS TO HANDLE THE CROPPER BOX */
var $image = $("#image");
var cropBoxData;
var canvasData;
$("#modalCrop").on("shown.bs.modal", function () {
    $image.cropper({
      viewMode: 1,
      aspectRatio: 1/1,
      minCropBoxWidth: 720,
      minCropBoxHeight: 720,
        cropBoxResizable: false,
      ready: function () {
        $image.cropper("setCanvasData", canvasData);
        $image.cropper("setCropBoxData", cropBoxData);
      }
});
}).on("hidden.bs.modal", function () {
cropBoxData = $image.cropper("getCropBoxData");
canvasData = $image.cropper("getCanvasData");
$image.cropper("destroy");
});

$(".js-zoom-in").click(function () {
$image.cropper("zoom", 0.1);
});

$(".js-zoom-out").click(function () {
$image.cropper("zoom", -0.1);
});

/* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
$(".js-crop-and-upload").click(function () {
var cropData = $image.cropper("getData");
$("#id_x").val(cropData["x"]);
$("#id_y").val(cropData["y"]);
$("#id_height").val(cropData["height"]);
$("#id_width").val(cropData["width"]);
$("#form-user-avatar").submit();
});

function showToastr(data) {
    var i = -1,
        toastCount = 0,
        $toastlast,
        getMessage = function () {
            var msgs = ['Hello, some notification sample goes here',
                '<div><input class="form-control input-small" value="textbox"/>&nbsp;<a href="http://themeforest.net/item/metronic-responsive-admin-dashboard-template/4021469?ref=keenthemes" target="_blank">Check this out</a></div><div><button type="button" id="okBtn" class="btn blue">Close me</button><button type="button" id="surpriseBtn" class="btn default" style="margin: 0 8px 0 8px">Surprise me</button></div>',
                'Did you like this one ? :)',
                'Totally Awesome!!!',
                'Yeah, this is the Metronic!',
                'Explore the power of App. Purchase it now!'
            ];
            i++;
            if (i === msgs.length) {
                i = 0;
            }

            return msgs[i];
        };

    var shortCutFunction = data.tag;
    var msg = data.data;
    var title = data.title || '';

    var toastIndex = toastCount++;

    toastr.options = {
        closeButton: "checked",
        positionClass: 'toast-top-right',
        onclick: null,
        showDuration: 1000,
        hideDuration:1000,
        timeOut : 2000,
        extendedTimeOut : 1000
    };

    toastr.options.showEasing = "swing";
    toastr.options.hideEasing = "linear";
    toastr.options.showMethod = "fadeIn";
    toastr.options.hideMethod = "fadeOut";


    if (!msg) {
        msg = getMessage();
    }
    var $toast = toastr[shortCutFunction](msg, title); // Wire up an event handler to a button in the toast, if it exists

}


//--------END CROP AVATAR---------