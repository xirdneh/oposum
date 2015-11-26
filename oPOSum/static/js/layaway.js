var add_layway_btn = $("#layaway_add");
if(add_layway_btn){
    add_layway_btn.click(function(){
        var modal = $("#mensaje");
        modal.one('show.bs.modal', function(event){
            var mod = $(this);
            var modal_body = mod.find("#mensaje-body");
            var modal_title = mod.find("#mensaje-title");
            modal_title.text("Agregar Separado");
            var body = "<div id=\"user_branch\"></div>" +
            "<label for=\"layaway-type\">Tipo de Separado:</label>" +
            "<select name=\"layaway-type\" id=\"layaway-type\">" +
                "<option value=\"one_month\">1 Mes</option>" +
                "<option value=\"two_month\">2 Mes</option>" +
                "<option value=\"three_month\">3 Mes</option>" +
            "</select>" +
            "<input type=\"text\" name=\"product_code\" id=\"product_code\" class=\"form-control\" />" +
            "<table class=\"table table-striped\" id=\"layaway-prods\">" +
                "<thead>" +
                    "<tr>" +
                        "<td>Id</td>" +
                        "<td>Code</td>" +
                        "<td>Descripción</td>" +
                        "<td>Cantidad</td>" + 
                        "<td>Precio</td>" +
                    "</tr>" + 
                "</thead>" +
                "<tbody></tbody>" +
            "</table><div class=\"layaway-totals\"></div>" + 
            "<div class='layaway-pay-form'>" +
                "<div id=\"layaway-form-msg\"></div>" +
                "<h3> Primer abono de Separado </h3>" + 
                "<label for=\"layaway-payment-type\">Tipo de Pago</label>" +
                "<select name=\"layaway-payment-type\" id=\"layaway-payment-type\">" +
                    "<option name=\"cash\" value=\"Cash\">Efectivo</option>"  +
                    "<option name=\"credit\" value=\"Credit\">Débito/Credito</option>" + 
                    "<option name=\"cheque\" value=\"Check\">Cheque</option>" + 
                    "<option name=\"layaway voucher\" value=\"Layaway Voucher\">Vale Separado</option>" + 
                    "<option name=\"sale voucher\" value=\"Sale Voucher\">Vale Venta</option>" +
                "</select><br />" +
                "<label for=\"layaway-payment\">Monto a Pagar:</label>" +
                "<input class='form-control' name='layaway-payment' id='layaway-payment' type='number' step='0.1'/>" +
                "<label for=\"layaway-pay\">Pago:</label>" +
                "<input class='form-control' name='layaway-pay' id='layaway-pay' type='number' step='0.1'/>" +
                "<label for=\"layaway-change\">Cambio: </label>" +
                "<input disabled class='form-control' name='layaway-change' id='layaway-change' type='number' step='0.1'/>" +
            "</div>";
            modal_body.html(body);
            $("#mensaje-aceptar").text("Guardar");
            var pi = modal_body.find("#product_code");
            pi.focus();
            balco.print_branches_selector("user_branch", balco.user_branches);
            balco.select_init_branch("select_branches", balco.user_branch_selected);
            setup_price_input(pi);
            $("#layaway-payment").keyup(function(event){
                var e = $(this).val();
                $("#layaway-pay").val(e);
                if(event.which == 13 ){
                    $("#layaway-pay").focus();
                    $("#layaway-pay").select();
                }
            });
            $("#layaway-pay").keyup(function(e){
                var el = $(this);
                var pm = $("#layaway-payment").val();
                $("#layaway-change").val(+parseFloat(el.val()) - +parseFloat(pm));
                if(e.which == 13){
                    $("#mensaje-aceptar").focus();
                }
            });
            $("#mensaje-aceptar").one('click', function(e){
                e.preventDefault();
                data = get_table_data($("#layaway-prods"), ["id", "code", "desc", "qty", "retail_price"]);
                if(console){
                    console.log("Layaway to save: " + data);
                }
                if(check_layaway_form()){
                    $("#mensaje-body input, #mensaje-body select, #mensaje-aceptar").prop('disabled', true);
                    save_layaway(data);
                }
            });
        });
        modal.modal('show');
        modal.one('hidden.bs.modal', function(e){
            var mod = $(this);
            mod.find("#mensaje-body").html("");
            $("mensaje-aceptar").text("Aceptar");
        });
    });
}

function check_layaway_form(){
    var trn = $("#layaway-prods tbody tr");
    var txt = $("#layaway-form-msg").text();
    if(trn.length < 0){
        $("#layaway-form-msg").text(txt + ". No has agregado ningun articulo");
        return false;
    }
    if($("#layaway-payment").val() == "" || $("#layaway-payment").val() == "0"){
        $("#layaway-form-msg").text(txt + ". No se ha especificado un abono");
        return false;
    }
    var total = $(".tot-Total value").val();
    totla = parseFloat(total);
    var payment = $("#layaway-payment").val();
    payment = parseFloat(payment);
    if(total - payment < 0){
        $("#layaway-form-msg").text(txt + ". La cantidad del abono es invalida");
        return false;
    }
    return true;
}

function setup_price_input(pi){
    pi.keyup(function(e){
        if(e.keyCode == 13){
            var val = pi.val().split("*");
            var code, qty, price;
            if(val.length > 1){
                code = val[1];
                qty = +val[0];
            }else{
                code = val[0];
                qty = 1;
            }
            var cp = code.split(" ");
            if(cp.length > 1){
                code = cp[0];
                price = cp[1];
            }else{
                code = cp[0];
                price = 0;
            }
            $.ajax({
                method:"get",
                url: "/products/get-product/" + code,
                success:function(data){
                    $prod = data.product;
                    if(data.status == 'ok' && data.message == "Existente"){
                        add_prod_table($prod, qty, price);
                        pi.val("");
                        pi.focus();
                    }
                }
            });
        }
    });
}

function add_prod_table(p, q, pr){
    var t = $("#layaway-prods");
    var tbody = t.find("tbody");
    var trs = tbody.find("tr");
    var tr = $(trs[trs.length - 1]);
    var tds = tr.find("td");
    var td = $(tds[0]);
    var id = 0;
    if(td.text() != ""){
        id = +td.text();
    }
    id += 1;
    pr = pr == 0 ? p.retail_price : pr;
    var row = $("<tr>" +
        "<td>" + id + "</td>" +
        "<td>" + p.slug + "</td>" +
        "<td>" + p.description + "</td>" +
        "<td>" + q + "</td>" +
        "<td>" + pr + "</td>" +
    "</tr>");
    row.on('dblclick', delete_row);
    tbody.append(row);
    var tots = get_table_totals([{label:"Total", index:4, qty:3}], t);
    print_table_totals(tots, $(".layaway-totals"));
}

function delete_row(){
    var r = confirm("Desea borrar este articulo?");
    if(r){
        var row = $(this);
        var tbody = row.parent();
        row.remove();
        var id = 0;
        var trs = tbody.find("tr");
        var td;
        var tr;
        for(var i = 0; i < trs.length; i++){
            tr = $(trs[i]);
            td = $(tr.find("td")[0]);
            id++;
            td.text(id);
        }
        var tots = get_table_totals([{label:"Total", index:4, qty:3}], tbody.parent());
        print_table_totals(tots, $(".layaway-totals"));
    }
}

function get_table_totals(objs, table){
    var tbody = table.find("tbody");
    var trs = tbody.find("tr");
    var tds;
    var tr;
    var td;
    var tots = {};
    var val, qty;
    for(var j = 0; j < trs.length; j++){
        tr = $(trs[j]);
        tds = tr.find("td");
        for(var i = 0; i < objs.length; i++){
            o = objs[i];
            val = $(tds[o.index]).text();
            qty = $(tds[o.qty]).text();
            if(!isNaN(val)){
                val = +val;
            } else{
                val = 0;
            }
            if(tots[o.label]){
                tots[o.label] += val * +qty;
            }else{
                tots[o.label] = val * +qty;
            }
        }
    }
    return tots;
}

function print_table_totals(tots, el){
    el.html("");
    for(var o in tots){
        if(tots.hasOwnProperty(o)){
            el.append("<div class=\"tbl-tot tot-" + o + "\"><span class=\"tot-label\">" + o + ":</span><span class=\"value\"> " + tots[o] + "</span></div>");
        }
    }
}

function get_table_data(t, o){
    var tbody = t.find("tbody");
    var trs = tbody.find("tr");
    var tds, to, td;
    var ret = [];
    var i = 0;
    trs.each(function(index){
        tds = $(this).find("td");
        i = 0;
        to = {};
        tds.each(function(tdindex){
            td = $(this);
            to[o[i]] = $(td).text();
            i++;
        });
        ret.push(to);
    });
    return ret;
}

function save_layaway(data){
    var csrftoken = balco.get_cookie('csrftoken');
    csrftoken = balco.get_cookie('csrftoken');
    var payment_type = $("#layaway-payment-type").val();
    var payment = $("#layaway-payment").val();
    var d = {
                products: data,
                payment_type: payment_type,
                payment: payment,
                client_id: balco.layaway.client_id,
                layaway_type: $("#layaway-type").val(),
                branch_slug: $("#select_branches").val()
            };
    
    $.ajax({
        crossDomain: false,
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        method:"POST",
        data:{data: JSON.stringify(d)},
        url: "/layaway/save-layaway/",
        success: function(data){
            if(data.status == 'ok'){
                print_layaway_ticket(data);
            }
            else if(data.status == 'error'){
                var modal = $("#mensaje");
                var mod_body = modal.find("#mensaje-body");
                var mod_title = modal.find("#mensaje-title");
                mod_title.text("Error guardando separado");
                var mbody = "";
                var m;
                for(var mi = 0; mi < data.message.length; mi++){
                    m = data.message[mi];
                    if(m == "LayawaySavesuccess"){
                        mbody += "<p> El separado fue guardado exitosamente! </p>";
                    }
                    else if(m == "LayawayPaymentError"){
                        mbody += "<p> El abono que se quizo guardar no es valido </p>";
                    }
                    else if(m == "LayawayUserDebtError") {
                        mbody += "<p> El cliente no tiene derecho a hacer otro separado </p>";
                    }
                    else if(m == "LayawayUserBranchAccessError"){
                        mbody += "<p> No tienes derecho a crear separados para esta sucursal</p>";
                    }
                }
                mod_body.html(mbody);
                $("#mensaje-aceptar").text("Aceptar");
                $("#mensaje-aceptar").prop('disabled', false);
            }
        },
        error:function( jqXHR, textStatus, errorThrown ){
            if(console){
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
            }
            $("#mensaje #mensaje-body").html("<p>Ocurrio un error, favor de intenter de nuevo<p>");
            $("#mensaje-aceptar").text("Aceptar");
            $("#mensaje-aceptar").prop('disabled', false);
        }
    });
}

function print_layaway_ticket(data){
    var $now;
    var layaway = data.layaway;
    var payment = data.payment;
    var $folio = layaway.id;
    var tb = "";
    var tmptb = "";
    var $amt_to_pay = $("#layaway-payment").val();
    var $pay = $("#layaway-pay").val();
    var $pay_type = $("#layaway-type").val();
    var $change = $("#layaway-change").val();
    var print = true;
    if(balco.debug){
        print = true;
    }else if(balco.isLocalServerRunning){
        print = true;
    }else {
        print = !notReady();
    }
    if(print){
        $now = new Date(data.layaway.date_time);
        tb += data.branch.ticket_pre;
        tb += "\n\r";
        if(!$now){
            $now = new Date();
        }
        tb += "========== SEPARADO ==========";
        tb += '\n\r\t Fecha: ' + $now.getDate() + '/' 
                                   + (+$now.getMonth() + 1) + '/' 
                                   + $now.getFullYear() + '\n\r';
        tb += '\n\r\t Folio: ' + $folio + '\n\r';
        tb += "\n\r\t Nombre: " + layaway.client.first_name + " " + layaway.client.last_name + "\n\r";
        tb += "# \tCodigo\tPrecio\tCantidad\n\r\n\r";
        var id = 1;
        var p;
        for(var pi = 0; pi < layaway.products.length; pi++){
            p = layaway.products[pi];
            tb += id + " \t " + p.product.slug + " \t " + p.product.retail_price + " \t " + p.qty + "\n\r";
            id++;
        }
        tb += "Total del Separado: \t" + layaway.amount_to_pay + "\n\r";
        tb += "Saldo Total: \t" + layaway.total_debt_amount + "\n\r";
        tb += "\n\r\n\r\n\r";
        tb += "Los detalles listados en esta nota representan los articulos pertenecientes a un separado. Estos articulos no se entregaran hasta que no se cubra todo el saldo pendiente. Este separado sera valido por " + layaway.type + " dias apartir del " + layaway.date_time + ".\n\r";
        tb += data.branch.ticket_post;
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        if(balco.isLocalServerRunning){tb += " {{LF}} {{CR}} {{PAPERCUT}} ";}else{tb+= chr(27) + chr(105)+ "\x1B\x69";}
        tmptb = tb;
        tb += "\n\r\t**********COPIA**********\t\n\r";
        tb += tmptb;

        if(!balco.debug){ 
            if(!balco.isLocalServerRunning){
                qz.append(tb);
                qz.print();
            }else{
                balco.sendToPrinter(tb.replace(/[\n\r]/g, ' {{LF}} {{CR}} ').replace(/[\t]/g, ' {{TAB}} '));
            }
        }else{
                if(console){
                    console.log(tb);
                }
            }
        
        tb = "";
        tb += data.branch.ticket_pre;
        tb += "\n\r";
        if(!$now){
            $now = new Date();
        }
        tb += "============= Abono de Separado =============";
        tb += '\n\r\t Fecha: ' + $now.getDate() + '/' 
                                   + (+$now.getMonth() + 1) + '/' 
                                   + $now.getFullYear() + '\n\r';
        tb += '\n\r\t Folio: ' + payment.id + '\n\r';
        tb += '\n\r\t Folio de Separado: ' + layaway.id + '\n\r';
        tb += "\n\r\t Nombre: " + layaway.client.first_name + " " + layaway.client.last_name + "\n\r";
        tb += "\n\r Tipo de Pago: \t" + payment.payment_type ;
        tb += "\n\r Cantidad: \t" + payment.amount;
        tb += "\n\r Su Pago: \t $" + $("#layaway-pay").val() + "=";
        tb += "\n\r Cambio: \t $" + $("#layaway-change").val() + "=";
        tb += "\n\r Saldo Total: \t" + layaway.total_debt_amount ;
        tb += "\n\r Fecha de vencimiento: \t " + layaway.date_end;
        tb += "\n\r\n\r Este recibo representa un abono a un separado. El saldo total es la cantidad a pagar calculado al dia que se especifica en este ticket.\n\r\n\r";
        tb += data.branch.ticket_post;
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        if(balco.isLocalServerRunning){tb += " {{LF}} {{CR}} {{PAPERCUT}} ";}else{tb+= chr(27) + chr(105)+ "\x1B\x69";}
        tmptb = tb;
        tb += "\n\r\t**********COPIA**********\t\n\r";
        tb += tmptb;
        if(!balco.debug){ 
            if(!balco.isLocalServerRunning){
                qz.append(tb);
                qz.print();
            }else{
                balco.sendToPrinter(tb.replace(/[\n\r]/g, ' {{LF}} {{CR}} ').replace(/[\t]/g, ' {{TAB}} '));
            }
        }else{
                if(console){
                    console.log(tb);
                }
        }

        $("#mensaje button").prop('disabled', false);
        setTimeout(function(){
        window.location = '/clients/new/' + layaway.client.id;
        }, 500);
    }
}

var add_payment = $(".add-payment");
if(add_payment){
    add_payment.click(function(){
        var btn = $(this);
        var lid = +btn.attr('data-lid');
        var ldebt = parseFloat(btn.attr('data-ldebt'));
        var ltot = parseFloat(btn.attr('data-total'));
        var modal = $("#mensaje");
        var modal_body = modal.find("#mensaje-body");
        var modal_title = modal.find("#mensaje-title");
        modal_title.text("Abono");
        var body = "<div class='layaway-pay-form'>" +
                "<div id=\"layaway-form-msg\"></div>" +
                "<div id=\"user_branch\"></div>" +
                "<p><b>Saldo Pendiente: </b> " + ldebt + "</p>" +
                "<h3> Primer abono de Separado </h3>" + 
                "<label for=\"layaway-payment-type\">Tipo de Pago</label>" +
                "<select name=\"layaway-payment-type\" id=\"layaway-payment-type\">" +
                    "<option name=\"cash\" value=\"Cash\">Efectivo</option>"  +
                    "<option name=\"credit\" value=\"Credit\">Credito</option>" + 
                    "<option name=\"cheque\" value=\"Check\">Cheque</option>" + 
                    "<option name=\"layaway voucher\" value=\"Layaway Voucher\">Vale Separado</option>" + 
                    "<option name=\"sale voucher\" value=\"Sale Voucher\">Vale Venta</option>" + 
                "</select><br />" + 
                "<label for=\"layaway-payment\">Monto a Pagar:</label>" +
                "<input class='form-control' name='layaway-payment' id='layaway-payment' type='number' step='0.1'/>" +
                "<label for=\"layaway-pay\">Pago:</label>" +
                "<input class='form-control' name='layaway-pay' id='layaway-pay' type='number' step='0.1'/>" +
                "<label for=\"layaway-change\">Cambio: </label>" +
                "<input disabled class='form-control' name='layaway-change' id='layaway-change' type='number' step='0.1'/>" +
            "</div>";
       modal_body.html(body);
       balco.print_branches_selector("user_branch", balco.user_branches);
       balco.select_init_branch("select_branches", balco.user_branch_selected);
       $("#layaway-payment").keyup(function(event){
                var e = $(this).val();
                $("#layaway-pay").val(e);
                if(event.which == 13 ){
                    $("#layaway-pay").focus();
                    $("#layaway-pay").select();
                }
            });
            $("#layaway-pay").keyup(function(e){
                var el = $(this);
                var pm = $("#layaway-payment").val();
                $("#layaway-change").val(+parseFloat(el.val()) - +parseFloat(pm));
                if(e.which == 13){
                    $("#mensaje-aceptar").focus();
                }
            });
       $("#mensaje-aceptar").one('click', function(e){
            e.preventDefault();
            $("#mensaje input, #mensaje button, #mensaje select").prop('disabled', true);
           if(check_layaway_payment(ldebt)){
               save_payment(lid, ldebt, ltot, $("#layaway-payment").val());
           }
       });
       modal.modal('show');
    });
}

function check_layaway_payment(ldebt){
    if($("#layaway-payment").val() == "" || $("#layaway-payment").val() == "0"){
        $("#layaway-form-msg").text(txt + ". No se ha especificado un abono");
        return false;
    }
    var payment = $("#layaway-payment").val();
    payment = +payment;
    if(ldebt - payment < 0){
        $("#layaway-form-msg").text(txt + ". La cantidad del abono es invalida");
        return false;
    }
    return true;
}

function save_payment(lid, ldebt, ltot, payment){
    payment = +payment;
    var csrftoken = balco.get_cookie('csrftoken');
    csrftoken = balco.get_cookie('csrftoken');
    var payment_type = $("#layaway-payment-type").val();
    var d = {
                lid: lid, 
                ldebt: ldebt, 
                ltot: ltot, 
                payment_type: payment_type,
                payment: payment,
                branch_slug: $("#select_branches").val(),
                client_id: balco.layaway.client_id
            };
    $.ajax({
        crossDomain: false,
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        method:"POST",
        data:{data: JSON.stringify(d)},
        url: "/layaway/save-payment/",
        success: function(data){
            if(data.status == 'ok'){
                print_payment_ticket(data);
            }
            else if(data.status == 'error'){
                var modal = $("#mensaje");
                var mod_body = modal.find("#mensaje-body");
                var mod_title = modal.find("#mensaje-title");
                mod_title.text("Error guardando separado");
                var mbody = "";
                var m;
                for(var mi = 0; mi < data.message.length; mi++){
                    m = data.message[mi];
                    if(m == "LayawaySaveSuccess"){
                        mbody += "<p> El separado fue guardado exitosamente! </p>";
                    }
                    else if(m == "LayawayPaymentError"){
                        mbody += "<p> El abono que se quizo guardar no es valido </p>";
                    }
                    else if(m == "LayawayUserDebtError") {
                        mbody += "<p> El cliente no tiene derecho a hacer otro separado </p>";
                    }
                    else if(m == "LayawayUserBranchAccessError"){
                        mbody += "<p> No tienes derecho a crear separados para esta sucursal</p>";
                    }
                }
                mod_body.html(mbody);
                $("#mensaje-aceptar").text("Aceptar");
                $("#mensaje-aceptar").prop('disabled', false);
            }
        },
        error:function( jqXHR, textStatus, errorThrown ){
            if(console){
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
            }
            $("#mensaje #mensaje-body").html("<p>Ocurrio un error, favor de intenter de nuevo<p>");
            $("#mensaje-aceptar").text("Aceptar");
            $("#mensaje-aceptar").prop('disabled', false);
        }
    });
}

function print_payment_ticket(data){
    var $now;
    var payment = data.payment;
    var layaway = data.layaway;
    var $now = new Date(payment.date_time);
    var $amt_to_pay = $("#layaway-payment").val();
    var $pay = $("#layaway-pay").val();
    var $pay_type = $("#layaway-type").val();
    var $change = $("#layaway-change").val();
    var print = true;
    var tb = "";
    var tmptb = "";
    if(balco.debug){
        print = true;
    }else if(balco.isLocalServerRunning){
        print = true;
    }else {
        print = !notReady();
    }
    if(print){
        tb += data.branch.ticket_pre;
        tb += "\n\r";
        if(!$now){
            $now = new Date();
        }
        tb += "============= Abono de Separado =============";
        tb += '\n\r\t Fecha: ' + $now.getDate() + '/' 
                                   + (+$now.getMonth() + 1) + '/' 
                                   + $now.getFullYear() + '\n\r';
        tb += '\n\r\t Folio: ' + payment.id;
        tb += '\n\r\t Folio de Separado: ' + layaway.id + '\n\r';
        tb += "\n\r\t Nombre: " + layaway.client.first_name + " " + layaway.client.last_name + "\n\r";
        tb += "\n\r Tipo de Pago: \t" + payment.payment_type ;
        tb += "\n\r Cantidad: \t" + payment.amount;
        tb += "\n\r Su Pago: \t $" + $("#layaway-pay").val() + "=";
        tb += "\n\r Cambio: \t $" + $("#layaway-change").val() + "=";
        tb += "\n\r Saldo Total: \t" + layaway.total_debt_amount ;
        tb += "\n\r Fecha de vencimiento: \t " + layaway.date_end;
        tb += "\n\r\n\r Este recibo representa un abono a un separado. El saldo total es la cantidad a pagar calculado al dia que se especifica en este ticket.\n\r\n\r";
        tb += data.branch.ticket_post;
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        tb += "\n\r";
        if(balco.isLocalServerRunning){tb += " {{LF}} {{CR}} {{PAPERCUT}} ";}else{tb+= chr(27) + chr(105)+ "\x1B\x69";}
        tmptb = tb;
        tb += "\n\r\t**********COPIA**********\t\n\r";
        tb += tmptb;
        if(!balco.debug){
            if(!balco.isLocalServerRunning){
                qz.append(tb);
                qz.print();
            }else{
                balco.sendToPrinter(tb.replace(/[\n\r]/g, ' {{LF}} {{CR}} ').replace(/[\t]/g, ' {{TAB}} '));
            }
        }else{
            if(console){
                console.log(tb);
            }
        }
        if(layaway.total_debt_amount == "$0.00="){
            tb = "";
            tmptb = "";

            tb += data.branch.ticket_pre;
            tb += "\n\r";
            if(!$now){
                $now = new Date();
            }
            tb += "============= Resumen de Separado =============";
            tb += '\n\r\t Fecha: ' + $now.getDate() + '/' 
                                       + (+$now.getMonth() + 1) + '/' 
                                       + $now.getFullYear() + '\n\r';
            tb += '\n\r\t Folio de Separado: ' + layaway.id + '\n\r';
            tb += "\n\r\t Nombre: " + layaway.client.first_name + " " + layaway.client.last_name + "\n\r";
            tb += "\n\r Saldo Total: \t" + layaway.total_debt_amount ;

            tb += "\n\tCodigo\tPrecio\tCantidad\n\r\n\r";
            var id = 1;
            var p;
            for(var pi = 0; pi < layaway.products.length; pi++){
                p = layaway.products[pi];
                tb += id + " \t " + p.product.slug + " \t " + p.product.retail_price + " \t " + p.qty + "\n\r";
                id++;
            }
            tb += "Total del Separado: \t" + layaway.amount_to_pay + "\n\r";
            tb += "\n\r\n\r\n\r";
            tb += "Los detalles listados en esta nota representan los articulos pertenecientes a un separado. Estos articulos no se entregaran hasta que no se cubra todo el saldo pendiente. Este separado sera valido por " + layaway.type + " dias apartir del " + layaway.date_time + ".\n\r";

            tb += data.branch.ticket_post;
            tb += "\n\r";
            tb += "\n\r";
            tb += "\n\r";
            tb += "\n\r";
            tb += "\n\r";
            tb += "\n\r";
            tb += "\n\r";
            tmptb = tb;
            if(balco.isLocalServerRunning){tb += " {{LF}} {{CR}} {{PAPERCUT}} ";}else{tb+= chr(27) + chr(105)+ "\x1B\x69";}
            tb += "\n\r\t**********COPIA**********\t\n\r";
            tb += tmptb;
            if(!balco.debug){ 
                if(!balco.isLocalServerRunning){
                    qz.append(tb);
                    qz.print();
                }else{
                    balco.sendToPrinter(tb.replace(/[\n\r]/g, ' {{LF}} {{CR}} ').replace(/[\t]/g, ' {{TAB}} '));
                }
            }else{
                if(console){
                    console.log(tb);
                }
            }
        }

        $("#mensaje button").prop('disabled', false);
        setTimeout(function(){
        window.location = '/clients/new/' + layaway.client.id;
        }, 500);
    }
}

