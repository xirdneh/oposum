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
            } else if (data.status == 'ok' && data.message == 'Migrando'){
                var modal = $("#mensaje");
                modal.on('show.bs.modal', function(event){
                    var mod = $(this);
                    var modal_body = mod.find("#mensaje-body");
                    var body = "<div class='mensaje-modal-row'>" +
                       "<div class='mensaje-modal-cell'>Code</div>" + 
                       "<div class='mensaje-modal-cell'>" + $prod.code  + "</div>" + 
                       "</div><div class='mensaje-modal-row'>" + 
                       "<div class='mensaje-modal-cell'>Descripcion</div>" + 
                       "<div class='mensaje-modal-cell'>" + $prod.description  + "</div>" + 
                       "</div><div class='mensaje-modal-row'>" + 
                       "<div class='mensaje-modal-cell'>Linea</div>" + 
                       "<div class='mensaje-modal-cell'>" + $prod.linea  + "</div>" + 
                       "</div><div class='mensaje-modal-row'>" + 
                       "<div class='mensaje-modal-cell'>Proveedor</div>" + 
                       "<div class='mensaje-modal-cell'>" + $prod.prov  + "</div>" + 
                       "</div><div class='mensaje-modal-row'>" + 
                       "<div class='mensaje-modal-cell'>Bodega</div>" + 
                       "<div class='mensaje-modal-cell'>" + $prod.bodega  + "</div>" + 
                       "</div><div class='mensaje-modal-row'>" + 
                       "<div class='mensaje-modal-cell'>Area</div>" + 
                       "<div class='mensaje-modal-cell'>" + $prod.area  + "</div>" + 
                       "</div><div class='mensaje-modal-row'>" + 
                       "<div class='mensaje-modal-cell'>Precio</div>" + 
                       "<div class='mensaje-modal-cell'>" + $prod.price  + "</div>" + 
                       "</div><div class='mensaje-modal-row'>" + 
                       "<div class='mensaje-modal-cell'>Peso</div>" + 
                       "<div class='mensaje-modal-cell'>" + $prod.equivalency + "</div>" + 
                       "</div><div class='mensaje-modal-row'>" + 
                       "<div class='mensaje-modal-cell'>Linea Precio</div>" + 
                       "<div class='mensaje-modal-cell'>" + $prod.line  + "</div>" + 
                       "</div>";
                    modal_body.html(body);
                    var frm_aceptar = mod.find("#mensaje-aceptar-form");
                    frm_aceptar.submit(function(e){
                        e.preventDefault();
                        var json_prod = JSON.stringify($prod);
                        var csrftoken = balco.get_cookie('csrftoken');
                        var $branch = $("#select_branches")[0].options[$("#select_branches")[0].selectedIndex].value;
                        var data = {data: "{\"user\":\"" + $user + "\", " +
                                           "\"branch\":\"" + $branch + "\", " +
                                           "\"product\":" + json_prod + "} "
                                   };
                        $.ajax({
                            crossDomain: false,
                            beforeSend: function(xhr, settings){
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            },
                            type:"post",
                            url:"/products/migrate-prod",
                            data: data,
                            error: function(jqXHR, textStatus, errorThrown){
                                console.log(jqXHR);
                                console.log(textStatus);
                                console.log(errorThrown);
                            },
                            success:function(data){
                                if (data.status == 'ok'){
                                    $prod = data.product;
                                    $("#prod_info").html("<em>" + $prod.slug + "</em><span>" + $prod.description + "</span> $" + $prod.price);
                                    $("#product_price").val($prod.price);
                                    $prod.qty = $("#product_qty").val();
                                }
                                $("#product_code").prop('disabled', false);
                                modal.modal('hide');
                                $("#product_qty").focus();
                            }
                        });
                    });
                });
                modal.modal('show');
            }
            else if(data.status == 'error' && data.message == 'Producto no encontrado'){
                window.open("/products/add-products/" + $pi.val())
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

$("#btn_guardar").submit(function(e){
    e.preventDefault();
    var $now;
    $.ajax({
        dataType:"jsonp",
        url:"//www.timeapi.org/utc/now.json",
        success:function(d){
                var $utc = new Date(d.dateString);
                $now = new Date(d.dateString);
                $now.setHours($utc.getHours() - 6);
            }
    });
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
        url: "/inventory/save-entries",
        data: $data,
        error: function(jqXHR, textStatus, errorThrown){
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        }
    }).done(function(data){
            var $folio = data.folio;
            var $total = 0;
        var empty = [];
        dataView.setItems(empty);
        $("#nota").modal('hide');
        $("#product_code").focus();
        $("#grid_totals").html("<strong>Total:</strong> <span id='nota_sub_total'>0.0</span>");
        $("#nota_btn_imprimir").prop("disabled", false);
    });
});

