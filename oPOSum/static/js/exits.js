var $pi = $("#product_code");
$("#product_price").prop('disabled', true);
var $prod;
var $total = 0;
$pi.blur(function() {
    if($pi.val().length > 3){
        $("#product_qty").prop('disabled', true);
        $("#product_code").prop('disabled', true);
        $.ajax({
            type:"get",
            url: "/products/get-product/" + $pi.val()
        }).done(function(data){
            $prod = data.product;
            if (data.status == 'ok' && data.message == 'Existente'){
                $("#prod_info").html("<em>" + $prod.slug + "</em> <span>" +
                $prod.description + "</span> $" + $prod.price);
                $("#product_price").val($prod.price);
                $prod.qty = $("#product_qty").val();
            } 
            $("#product_qty").prop('disabled', false);
            $("#product_code").prop('disabled', false);
            $("#product_qty").focus();
        });
    }
});

var $pp = $("#product_qty").keyup(function(e){
    if(e.keyCode == 13){
        var $data = dataView.getItems();
        var $id = 0;
        if ($data.length == 0){
            $id = 0;
        }
        else {
            $id = +$data[$data.length-1].id;
            $id++;
        }
        $prod.qty = $("#product_qty").val();
        $data.push({'id': $id, 'slug': $prod.slug, 'desc': $prod.description,
        'qty': $prod.qty});
        dataView.setItems($data);
        $("#product_code").val("");
        $("#product_code").focus();
        $("#product_price").val("");
        grid_get_total();
    }
});

function grid_get_total(){
    var $data = dataView.getItems();
    var $t_qty = 0, $total = 0;
    for(var i = 0; i < $data.length; i++){
        var item = $data[i];
        $total += (+item.price * +item.qty);
        $t_qty += (+item.qty);
    }
    $("#grid_totals").html("<strong>Total Piezas:</strong> <span id='nota_qty_total'>" + $t_qty + "</span>");
}

$("#btn_guardar").click(function(e){
    var modal = $("#mensaje");
    modal.one('show.bs.modal', function(event){
        var mod = $(this)
        var modal_body = mod.find("#mensaje-body");
        var body = "<p> Desea Guardar estos movimientos?" + 
                   "</p>";
        modal_body.html(body);
        var frm_aceptar = mod.find("#mensaje-aceptar-form");
        frm_aceptar.one('submit', function(e){
            e.preventDefault();
            modal_body.html("<h2>Guardando datos...</h2>"); 
            var $td = JSON.stringify(dataView.getItems());
            var $branch = $("#select_branches")[0].options[$("#select_branches")[0].selectedIndex].value;
            var $data = {data:"{\"user\":\"" + $user +"\", "+ 
                           "\"branch\":\"" + $branch + "\", "+ 
                           "\"details\":" + $td +"}" };
            var csrftoken = balco.get_cookie('csrftoken');
            $.ajax({
                crossDomain: false,
                beforeSend: function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                type:"post",
                url: "/inventory/save-exits",
                data: $data,
                error: function(jqXHR, textStatus, errorThrown){
                      alert("Se produjo un error al guardar los datos, favor the intentar de nuevo.\n" + errorThrown);
                },
                success:function(data){
                var $folio = data.folio;
                var $total = 0;
                var empty = [];
                if(data.status == 'ok'){
                    dataView.setItems(empty);
                    modal_body.html("<p style='color:#99ce2f;'> Entradas guardadas exitosamente. Desea imprimir el filio de entradas #" + $folio + "</p>");
                    $("#mensaje-aceptar").text("Imprimir");
                    $("#mensaje-aceptar").removeClass('btn-main');
                    $("#mensaje-aceptar").addClass('btn-success');
                    frm_aceptar.one('submit', function(e){
                        e.preventDefault();
                        window.location = "/inventory/print-exits-report/" + $folio;
                        $("#mensaje-aceptar").text("Aceptar");
                        $("#mensaje-aceptar").removeClass('btn-success');
                        $("#mensaje-aceptar").addClass('btn-main');
                        modal.modal('hide');
                   });
                }else{
                    var bhtml = "";
                    bhtml += "<p style='color:red'> No se guardaron todos los movimientos debido a que existen los siguientes errores: </p>";
                    if(data.products){
                        var error;
                        for(var i = 0; i < data.products.length; i++){
                            error = data.products[i];
                            if(error[1] == "qty"){
                                error[1] = "Cantidad inexistente. qty = " + error[2];
                            } else {
                                error[1] = "Art&iacute;culo inexistente.";
                            }
                            bhtml += "<div class='mensaje-modal-row'>" +
                                "<div class='mensaje-modal-cell'>Art&iacute;culo:</div>" +
                                "<div class='mensaje-modal-cell'>" + error[0] + "</div>"+
                                "<div class='mensaje-modal-cell'>Error:</div>" + 
                                "<div class='mensaje-modal-cell'>" + error[1] + "</div>"+
                                "</div>";
                        }
                    } else {
                        bhtml += "<p>Errores no especificados </p>";
                    }
                    modal_body.html(bhtml);
                    $("#mensaje-aceptar").text("Aceptar");
                    $("#mensaje-aceptar").removeClass('btn-success');
                    $("#mensaje-aceptar").addClass('btn-danger');
                    frm_aceptar.one('submit', function(e){
                        e.preventDefault();
                        modal.modal('hide');
                    });
                }
                $("#product_code").focus();
                $("#grid_totals").html("<strong>Total:</strong> <span id='nota_sub_total'>0.0</span>");
                $("#nota_btn_imprimir").prop("disabled", false);
            }
            });
        });
    });
    modal.one('hidden.bs.modal', function(event){
        $("#mensaje-aceptar").text("Aceptar");
        $("#mensaje-aceptar").removeClass('btn-success');
        $("#mensaje-aceptar").addClass('btn-main');
        var mod = $(this)
        var frm_aceptar = mod.find("#mensaje-aceptar-form");
    });
    modal.modal('show');
});


$("#historial-salidas").click(function(e){
    e.preventDefault();
    var modal = $("#mensaje");
    modal.one('show.bs.modal', function(event){
        var mod = $(this);
        var modal_body = mod.find("#mensaje-body");
        var body = "<input type='number' id='folio_num' name='folio_num' />";
        modal_body.html(body);
        var frm_aceptar = mod.find("#mensaje-aceptar-form");
        frm_aceptar.one('submit', function(e){
            e.preventDefault();
            var f = $("#folio_num").val();
            window.location = "/inventory/exitence-history/" + f;
        });
    });
    modal.modal('show');
});

function goodbye(e) {
    if(dataView.getLength() > 0){
        if (!e) e = window.event;
        //e.cancelBubble is supported by IE - this will kill the bubbling process.
        e.cancelBubble = true;
        e.returnValue = 'Esta pagina se va a cerrar y la informacion se perdera. Esta seguro de querer hacer esto?'; //This is displayed on the dialog
        //e.stopPropagation works in Firefox.
        if (e.stopPropagation) {
            e.stopPropagation();
            e.preventDefault();
        }
        return null;
    }
}
window.addEventListener("beforeunload", goodbye); 

