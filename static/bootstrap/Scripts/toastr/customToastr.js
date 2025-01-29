/// <reference path="toastr.js" />

// this will be used to call the toastr js library by customizing the apperance of it.


toastr.options.positionClass = 'toast-bottom-right';
toastr.options.tapToDismiss = false;

var yToastr = function () {
    return {
        Info: function (message) {
            this.ClearToastr();
            toastr.info(message);
        },
        Success: function (message) {
            this.ClearToastr();
            toastr.success(message);
        },
        Warning: function (message) {
            this.ClearToastr();
            toastr.warning(message);
        },
        Error: function (message) {
            this.ClearToastr();
            toastr.error(message, "Error");
        },
        ClearToastr: function () {
            //toastr.clear();
            var toast = $("div#toast-container");
            if (toast != null) {
                $(toast).html("");
            }
        },
        Sticky: function (message) {
            
            this.ClearToastr();             
            toastr.options.timeOut = 20000;
            toastr.options.closeButton = true;
            toastr.info(message);
        }
    };
} ();
