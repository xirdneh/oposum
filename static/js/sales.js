var $pi = $("#product_code");
var $prod;
var $total = 0;
$pi.blur(function() {
    if($pi.val().length > 3){
        $("#product_qty").prop('disabled', true);
        $("#product_price").prop('disabled', true);
        $("#product_code").prop('disabled', true);
        $.ajax({
            type:"get",
            url: "/products/get-product/" + $pi.val()
        }).done(function(data){
            $prod = data.product;
            if (data.status == 'ok' && data.message == "Existente"){
                $("#prod_info").html("<em>" + $prod.slug + "</em> <span>" +
                $prod.description + "</span> $" + $prod.price);
                $("#product_price").val($prod.price);
                $prod.qty = $("#product_qty").val();
                $("#product_qty").prop('disabled', false);
                $("#product_price").prop('disabled', false);
                $("#product_code").prop('disabled', false);
                $("#product_price").focus();
            }
            else if (data.status == "ok" && data.message == "Migrando"){
                var modal = $("#mensaje");
                modal.one('show.bs.modal', function(event){
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
                    frm_aceptar.one('submit', function(e){
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
                $("#product_qty").prop('disabled', false);
                $("#product_price").prop('disabled', false);
                $("#product_code").prop('disabled', false);
                $("#product_price").focus();

            }
            else if(data.status == "error"){
                $("#prod_info").text("Este articulo no existe, favor de verificar la clave.");  
                $("#product_qty").prop('disabled', false);
                $("#product_price").prop('disabled', false);
                $("#product_code").prop('disabled', false);
                $("#product_code").focus();
            }
        });
    }
});

var $pp = $("#product_price").keyup(function(e){
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
        'price': $("#product_price").val(), 'qty': $prod.qty});
        dataView.setItems($data);
        $("#product_code").val("");
        $("#product_code").focus();
        $("#product_price").val("");
        grid_get_total();
    }
});

var $mrs = $("#menu_reports_sales");
$mrs.click(function(e){
    e.preventDefault();
    var $branch = $("#select_branches")[0].options[$("#select_branches")[0].selectedIndex].value;
    var $now;
    $.ajax({
        dataType:"jsonp",
        url:"//www.timeapi.org/utc/now.json",
        success:function(d){
                var $utc = new Date(d.dateString);
                $now = new Date(d.dateString);
                $now.setHours($utc.getHours() - 5);
                $.ajax({
                    url:"/pos/report-sales/" + $branch + "/" + $now.getDate() + "-" + (+$now.getMonth() + 1) + "-" + $now.getFullYear() + "/",
                    success:function(d){
                        console.log("here");
                        if (!notReady()) {
                            qz.append($branch + "\n\r");
                            var $total = 0;
                            if (d.sales.length > 0){
                                qz.append(d.sales[0].date_time.split(" ")[0] + "\n\r");
                                qz.append("Folio   Total    Metodo\n\r");
                                for (var i = 0; i < d.sales.length; i++){
                                var $sale = d.sales[i];
                                qz.append($sale.folio_number + " " + $sale.total_amount + " " + $sale.payment_method + "\n\r");
                                $total += $sale.total_amount;
                                }
                            }
                        qz.append("Total del dia: " + $total + "\n\r");
                        qz.append("\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r");
                        qz.append(chr(27) + chr(105));
                        qz.append("\x1B\x69");
                        qz.print();
                        } else {
                            window.alert("Hay un error con la impresora. Presione la tecla F5 en el teclado y si aparece una ventana gris seleccione el recuadro que esta en la parte de abajo para que se aparezca una paloma y despues el boton que dice 'Run...'");
                        }
                    }
                });
            }
    }); 
});

var $mrsb = $("#menu_reports_sales_branch");
$mrsb.click(function(e){
    e.preventDefault();
    var modal = $("#mensaje");
    modal.one('show.bs.modal', function(e){
        var mod = $(this);
        var mod_body = mod.find("#mensaje-body");
        var mod_title = mod.find("#mensaje-title");
        mod_title.text("Seleccionar rango de fecha.");
        mod_body.html("<input type=\"text\" placeholder=\"Fecha Inicio\" name=\"datestart\" id=\"datestart\"/>"+
                      "<br />" + 
                      "<input type=\"text\" placeholder=\"Fecha Final\" name\"dateend\" id=\"dateend\"/>");
        var branches = $("#user_branch").clone();
        branches.attr("id", "filter_branch_wrap");
        branches.find("label").attr("for", "filter_branch");
        branches.find("select").attr("id", "filter_branch");
        branches.find("select").attr("name", "filter_branch");
        mod_body.prepend(branches);
        frm_aceptar = $("#mensaje-aceptar-form");
        mod.find("#datestart, #dateend").pickadate({
            monthsFull : ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Dicimbre'],
            weekdaysShort : ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom'],
            today: 'Hoy',
            clear: 'Borrar',
            selectMonths: true,
            selectYears: true,
            format: 'dd-mm-yyyy',
        });
        frm_aceptar.one('submit', function(e){
            e.preventDefault();
            var frm = $(this);
            var date_start = $("#datestart").val();
            var date_end = $("#dateend").val();
            var branch = $("#filter_branch").val();
            window.location = "/pos/report-sales-branch/" + branch + "/"  + date_start + "/" + date_end;
        });
    });
    modal.modal('show');
    modal.on('hidden.bs.modal', function(e){
        var mod = $(this);
        var frm_aceptar = mod.find("#mensaje-aceptar-form");
        frm_aceptar.unbind();
    });
});

function grid_get_total(){
    var $data = dataView.getItems();
    var $total = 0;
    for(var i = 0; i < $data.length; i++){
        var item = $data[i];
        $total = +$total + (+item.price * +item.qty);
    }
    $("#grid_totals").html("<strong>Total:</strong> <span id='nota_sub_total'>"  + $total + "</span>");
}

$("#nota").on('shown.bs.modal', function(e){
    $("#nota_pago").keyup(function(e){
        if(e.keyCode == 9 || e.keyCode == 13){
            var $cambio = $("#nota_pago").val() - $("#nota_total").val();
            $("#nota_cambio").val($cambio);
        }
    });

    $("#nota_pago").focus(function(){
        this.select();
    });
    $("#nota_pago").focus();
});

$("#btn_pagar").click(function(e){
    var $total = $("#nota_sub_total")[0].innerHTML;
    $("#nota_pago").val($total); 
    $("#nota_total").val($total);
    $("#nota_total").prop("disabled", true);
    $("#nota_cambio").prop("disabled", true);
});

$("#save_ticket").submit(function(e){
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
    $("#nota_btn_imprimir").prop("disabled", true);
    var $td = JSON.stringify(dataView.getItems());
    var $cp = $("#nota_pago").val();
    var $tp = $("#nota_tipo_pago").val();
    var $branch = $("#select_branches")[0].options[$("#select_branches")[0].selectedIndex].value;
    var $data = {data:"{\"user\":\"" + $user +"\", "+ 
                       "\"branch\":\"" + $branch + "\", "+ 
                       "\"details\":" + $td +", "+ 
                       "\"payment_type\": \"" + $tp + "\", "+ 
                       "\"payment_amount\":\"" + $cp +"\"}" };
    var csrftoken = balco.get_cookie('csrftoken');
    csrftoken = balco.get_cookie('csrftoken');
    $.ajax({
        crossDomain: false,
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        type:"post",
        url: "/pos/save-sale",
        data: $data,
        error: function(jqXHR, textStatus, errorThrown){
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        }
    }).done(function(data){
            var $folio = data.folio;
            var $total = 0;
            if (!notReady()) {
            qz.append(data.ticket_pre);
            qz.append("\n\r");
            if (!$now){
                $now = new Date();
            }
            qz.append('\n\r\t Fecha: ' + $now.getDate() + '/' 
                                       + (+$now.getMonth() + 1) + '/' 
                                       + $now.getFullYear() + '\n\r');
            qz.append('\n\r\t Folio: ' + $folio + '\n\r');
            for(var i =0; i < dataView.getItems().length; i++){
                var item = dataView.getItems()[i];
                $total += +item.price * +item.qty;
                qz.append("# \tCodigo\tPrecio\tCantidad\n\r\n\r");
                qz.append(item.id + " \t " + item.slug + " \t " + item.price + " \t " + item.qty + "\n\r");
                if (item.desc != ""){
                    qz.append("\t" + item.desc + "\n\r");
                } else {       
                    qz.append("\tArticulo de Venta\n\r");
                }
            }
            qz.append("Total: \t" + $total + "\n\t");
            qz.append("Su Pago: \t" + $cp + "\n\t");
            qz.append("Cambio: \t" + ($cp - $total).toFixed(2) + "\n\t");
            qz.append(data.ticket_post);
            qz.append("\n\r");
            qz.append("\n\r");
            qz.append("\n\r");
            qz.append("\n\r");
            qz.append("\n\r");
            qz.append("\n\r");
            qz.append("\n\r");
            qz.append(chr(27) + chr(105));
            qz.append("\x1B\x69");
            /** COPIA 8*/
            qz.append('\n\r\t***COPIA***\t\n\r');
            qz.append(data.ticket_pre);
            qz.append("\n\r");
            qz.append('\n\r\t Fecha: ' + $now.getDate() + '/' 
                                       + (+$now.getMonth() + 1) + '/' 
                                       + $now.getFullYear() + '\n\r');
            qz.append('\n\r\t Folio: ' + $folio + '\n\r');
            for(var i =0; i < dataView.getItems().length; i++){
                item = dataView.getItems()[i];
                qz.append("# \tCodigo\tPrecio\tCantidad \n\r\n\r");
                qz.append(item.id + " \t " + item.slug + " \t " + item.price + " \t " + item.qty + "\n\r");
                qz.append("\t" + item.desc + "\n\r");
            }
            qz.append("Total: \t" + $total + "\n\t");
            qz.append("Su Pago: \t" + $cp + "\n\t");
            qz.append("Cambio: \t" + ($cp - $total).toFixed(2) + "\n\t");
            qz.append(data.ticket_post);
            qz.append("\n\r");
            qz.append("\n\r");
            qz.append("\n\r");
            qz.append("\n\r");
            qz.append("\n\r");
            qz.append("\n\r");
            qz.append("\n\r");
            qz.append(chr(27) + chr(105));
            qz.append("\x1B\x69");
            qz.print();
            } else {
                window.alert("Hay un error con la impresora. Presione la tecla F5 en el teclado y si aparece una ventana gris seleccione el recuadro que esta en la parte de abajo para que se aparezca una paloma y despues el boton que dice 'Run...'");
            }
        var empty = [];
        dataView.setItems(empty);
        $("#nota").modal('hide');
        $("#product_code").focus();
        $("#grid_totals").html("<strong>Total:</strong> <span id='nota_sub_total'>0.0</span>");
        $("#nota_btn_imprimir").prop("disabled", false);
    });
});

