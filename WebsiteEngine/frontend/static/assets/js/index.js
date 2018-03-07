(function($){
    $.ajax({
        url: "backend-dot-rnacompute.appspot.com/posts?page=0",
        datatype: "html",
        crossDomain: true,
        success: function(data) {
            $("#posts").append(data);
        }
    });
})(jQuery);
