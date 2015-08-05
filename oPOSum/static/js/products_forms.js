(function($){
    $("#id_slug").focus();
    var form = document.forms.product_frm;
    var close_after = form.close_after.value;
    if (close_after == "True"){
        $(form).submit(function(e){
            e.preventDefault();
            var form_serialized = $(form).serialize()
            for(var i = 0; i < form.elements.category.options.length; i++){
                var o = form.elements.category[i];
                form_serialized += "&category=" + o.value;
            }
            $.ajax({
                type: "POST",
                url: form.getAttribute("action"),
                data: form_serialized,
                success: function(data){
                    if(data.status == 'ok'){
                        window.close();
                    } else {
                        $(".success_message").text("Error al guardar articulo, favor de intentar de nuevo");
                    }
                },
                error:function(jqXHR, textStatus, errorThrown){
                    if (console) console.log(errorThrown);
                    $(".success_message").text("Error al guardar articulo, favor de intentar de nuevo");
                }
            });
        });
    }
        
})(jQuery);
