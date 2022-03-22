$('.ui.dropdown')
  .dropdown()
;

//Show model add social
$("#btn_customer_social_add_social").click(function (){
    $('.ui.modal').modal('show')
})

// gán placeholder để người dùng biết cần nhập gì
$("#input_customer_social_social_id").change(function (e){
    var id = parseInt($(this).val())
    // Place holder
    switch (id) {
        case 1: //FB
            $("#input_customer_social_social_url").attr("placeholder", "Nhập liên kết Facebook (https://www.facebook.com/....)")
            $("#input_customer_social_social_url").attr('type','url');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
        case 2: //Zalo
            $("#input_customer_social_social_url").attr('placeholder',"Nhập số điện thoại Zalo");
            $("#input_customer_social_social_url").attr('type','number');
             e.preventDefault();
            break
        case 3: //TIKTOK
            $("#input_customer_social_social_url").attr("placeholder", "Nhập tên người dùng của bạn (vd: _trilong_)")
            $("#input_customer_social_social_url").attr('type','text');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
        case 4: //INSTAGRAM
            $("#input_customer_social_social_url").attr("placeholder", "Nhập tên người dùng của bạn (vd: _trilong_)")
            $("#input_customer_social_social_url").attr('type','text');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
        case 5: //EMAIL
            $("#input_customer_social_social_url").attr("placeholder", "Nhập Email (xxx@gmail.com)")
            $("#input_customer_social_social_url").attr('type','text');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
        case 6: //TWITTER
            $("#input_customer_social_social_url").attr("placeholder", "Nhập liên kết Twitter (https://twitter.com/....)")
            $("#input_customer_social_social_url").attr('type','url');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
        case 7: //TELEGRAM
            $("#input_customer_social_social_url").attr("placeholder", "Nhập tên người dùng của bạn (vd: trilong0610)")
            $("#input_customer_social_social_url").attr('type','text');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
        case 8: //BLOGER
            $("#input_customer_social_social_url").attr("placeholder", "Nhập liên kết Blogspot (https://xxx.blogspot.com/....)")
            $("#input_customer_social_social_url").attr('type','url');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
        case 9: //LINKEDIN
            $("#input_customer_social_social_url").attr("placeholder", "Nhập liên kết LinkedIn (https://www.linkedin.com/in/....)")
            $("#input_customer_social_social_url").attr('type','url');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
    }
});

// submit form them social
$("#form_customer_social_add_social").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.
    $("#btn_customer_social_submit_modal_add").replaceWith(
        "<button type=\"submit\" id=\"btn_customer_social_submit_modal_add\" class=\"btn btn-primary\">\n" +
        "                                    <span class=\"spinner-border spinner-border-sm\" role=\"status\" aria-hidden=\"true\" style=\"margin-right: 5px\"></span>\n" +
        "                                    Đang Thêm...\n" +
        "                                </button>"

    )
    var form = $(this);
    var url = 'https://trilong0610.pythonanywhere.com/customer/add_social/'

    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
                showToastr(data);
                if (data.tag == "success"){
                    window.location.reload(true)
                }
                else {
                    //Nếu nhập không đúng định dạng thì chuyển button đang thêm thành thêm
                    $("#btn_customer_social_submit_modal_add").replaceWith("<button type=\"submit\" id=\"btn_customer_social_submit_modal_add\" class=\"btn btn-primary\">\n" +
                        "                                    <p>Thêm</p>\n" +
                        "                                </button>")
                }


           },
            error: function (data) {
                showToastr(data);

            },
         });


});

// submit form change url social

$('.btn-customer-social-change').click(function (e) {
    var id = $(this).data('id')
    e.preventDefault();

    var form = $('form#form-customer-social-'+id).serialize();
    console.log(form)
    var url = 'https://trilong0610.pythonanywhere.com/customer/change_social/'
    $.ajax({
        url: url,
        type: "POST",
        data: form ,
        success: function(data) {
           showToastr(data)
        },
        error:function (data){
            showToastr(data)
        }
    });
})

$('.btn-customer-social-delete').click(function (e) {
    var id = $(this).data('id')
    e.preventDefault();

    var form = $('form#form-customer-social-'+id).serialize();
    console.log(form)
    var url = 'https://trilong0610.pythonanywhere.com/customer/delete_social/'
    $.ajax({
        url: url,
        type: "POST",
        data: form ,
        success: function(data) {
           showToastr(data)
            window.location.reload(true)
        },
        error:function (data){
            showToastr(data)
        }
    });
})

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