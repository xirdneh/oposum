var get_items = function(table){
    var $table = $(table);
    var rows = $table[0].rows;
    var items = [];
    for(var i=0; i<rows.length; i++){
        items.push({
            "test": "" 
        });
    }
};

$(".inv-edit").click(function(event){
    event.preventDefault();
    var mensaje = $("#mensaje");
    var mensaje_body = mensaje.find("#mensaje-body");
    var mensaje_title = mensaje.find("#mensaje-title");
    mensaje_title.text("Editar renglón");
    var tr = $(this).parent().parent();
    var mensaje_footer = mensaje.find(".modal-footer");
    var cancelar = $("<button type=\"button\" class=\"pull-left btn btn-default\" data-dismiss=\"modal\">Cancelar</button>");
    var aceptar_form = $("<form action=\"\" method=\"post\" id=\"mensaje-aceptar-form\" " + 
                         "name=\"mensaje-aceptar-form\">" + 
                         "<input type=\"hidden\" value=\"" + tr.attr('data-id') + "\" name=\"id\"/>" +
                         "<button type=\"submit\"" + 
                         " id=\"mensaje-aceptar\" class=\"btn btn-primary\">Aceptar</button>" +
                         "</form>");
    mensaje_footer.html("");
    var body = "<p>" + 
                "<span>" + tr[0].cells[0].textContent + "</span> <br/> " + 
                "<span>" + tr[0].cells[1].textContent + "</span> <br/>" +
                "<label for='existencia-cnt'>Existencia:</label>" +
                "<input id='existencia-cnt' name='existencia-cnt' type='number' form=\"mensaje-aceptar-form\"" + 
                "        value = '" + tr[0].cells[2].textContent +"' step='1' />" +
               "</p>";
    mensaje_body.html(body);
    aceptar_form.submit(function(e){
        e.preventDefault();
        var id = this.elements['id'].value;
        var qty = this.elements['existencia-cnt'].value;
        var csrftoken = balco.get_cookie('csrftoken');
        $.ajax({
            crossDomain: false,
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            type:"post",
            url: "/inventory/update-entry",
            data: {data: "{\"id\": \"" + id + "\"," +
                          "\"qty\": \"" + qty + "\"}"},
            error:function(jqXHR, textStatus, errorThrown){
                if(console){
                    console.log(textStatus);
                    console.log(jqXHR);
                }
            },
            success:function(data){
                var tr = $("#adjustments-table").find('tr[data-id=' + data.id + ']');
                tr[0].cells[2].textContent = data.qty;
                tr[0].cells[5].textContent = +tr[0].cells[3].textContent - +data.qty - +tr[0].cells[4].textContent;
                $("#mensaje").modal('hide');
                if(tr[0].cells[5].textContent == 0){
                    $(tr[0].cells[5]).removeClass('danger warning success').addClass('success');
                }else if(tr[0].cells[5].textContent > 0){
                    $(tr[0].cells[5]).removeClass('danger warning success').addClass('danger');
                }else if(tr[0].cells[5].textContent < 0){
                    $(tr[0].cells[5]).removeClass('danger warning success').addClass('warning');
                }
            }
        });
    });
    mensaje_footer.append(cancelar);
    mensaje_footer.append(aceptar_form);
    mensaje.modal('show');
});

$(".show-adjustments").click(function(event){
    event.preventDefault();
    var mensaje = $("#mensaje");
    var mensaje_body = mensaje.find("#mensaje-body");
    var mensaje_title = mensaje.find("#mensaje-title");
    mensaje_title.text("Ajustes");
    var tr = $(this).parent().parent();
    var mensaje_footer = mensaje.find(".modal-footer");
    var cancelar = $("<button type=\"button\" class=\"pull-left btn btn-default\" data-dismiss=\"modal\">Cancelar</button>");
    mensaje_footer.html("");
    mensaje_footer.append(cancelar);
    var body = "<h3>Cargando Ajustes...</h3>";
    mensaje_body.html(body);
    mensaje.modal('show');
    var id = tr.attr('data-id');
    $.ajax({
        type:"get",
        url: "/inventory/get-adjustments/" + id,
        error: function(jqXHR, textStatus, errorThrown){
            if(console){
                console.log(textStatus);
                console.log(jqXHR);
            }
        },
        success: function(data){
            var mensaje = $("#mensaje");
            var mensaje_body = mensaje.find("#mensaje-body");
            var body = "";
            var adj;
            for(var i = 0; i < data.adjustments.length; i++){
                adj = data.adjustments[i];
                body += "<tr>" +
                        "<td>" + adj.message + "</td>" + 
                        "<td>" + adj.quantity + "</td>" + 
                        "<td></td>" +
                        "</tr>";
            }
            mensaje_body.html("<table class='table table-striped' id='table-adjustments'>"+
                              "<thead>" + 
                                  "<tr>" +
                                      "<th>Detalles</th>" + 
                                      "<th>Cantidad</th>" +
                                      "<th></td>" + 
                                  "</tr>" +
                              "</thead>" +
                              "<tbody>" + 
                                body + 
                              "</tbody>");
            var add_adj_frm = $("<form id = 'add-adj-frm' name='add-adj-frm'>" + 
                                    "<input type='hidden' name='id' value='" + data.id + "' />" + 
                                    "<label for='adj-mensaje'>Detalles</label>" + 
                                    "<textarea name='adj-mensaje' cols='50' rows='3'></textarea>" + 
                                    "<label for='adj-quantity'>Cantidad</label>" + 
                                    "<input type='number' name='adj-quantity' value='1' step='1' />" +
                                    "<button type='submit' class='btn-warning btn'>Agregar</button>" +
                                "</form>");
            mensaje_body.append(add_adj_frm);
            add_adj_frm.submit(function(event){
                event.preventDefault();
                var id = this.elements['id'].value;
                var msg = this.elements['adj-mensaje'].value;
                var qty = this.elements['adj-quantity'].value;
                var csrftoken = balco.get_cookie('csrftoken');
                this.reset();
                $.ajax({
                    crossDomain: false,
                    beforeSend: function(xhr, settings){
                        xhr.setRequestHeader('X-CSRFToken', csrftoken);
                    },
                    type:"post",
                    url:"/inventory/save-adjustments/",
                    data: {data:"{"+
                            "\"id\": " + id + "," +
                            "\"qty\": " + qty + "," + 
                            "\"msg\": \"" + msg + "\"" +
                            "}"
                          },
                    error: function(jqXHR, textStatus, errorThrown){
                        if(console){
                            console.log(textStatus);
                            console.log(jqXHR);
                        }
                    },
                    success: function(data){
                        var mensaje = $("#mensaje");
                        var mensaje_body = mensaje.find("#mensaje-body");
                        var body = "";
                        var adj;
                        var cnt = 0;
                        for (var i =0; i < data.adjustments.length; i++){
                            adj = data.adjustments[i];
                            body += "<tr>" + 
                                    "<td>" + adj.message + "</td>" + 
                                    "<td>" + adj.quantity + "</td>" + 
                                    "<td></td>" + 
                                    "</tr>";
                            cnt += adj.quantity;
                        }
                        var tbody = mensaje_body.find("#table-adjustments tbody");
                        tbody.html(body);
                        var tr = $("#adjustments-table tbody tr[data-id=" + data.id + "]");
                        tr[0].cells[4].textContent = cnt;
                        tr[0].cells[5].textContent = +tr[0].cells[3].textContent - +tr[0].cells[2].textContent - +tr[0].cells[4].textContent;
                        if(tr[0].cells[5].textContent == 0){
                            $(tr[0].cells[5]).removeClass('danger warning success').addClass('success');
                        }else if(tr[0].cells[5].textContent > 0){
                            $(tr[0].cells[5]).removeClass('danger warning success').addClass('danger');
                        }else if(tr[0].cells[5].textContent < 0){
                            $(tr[0].cells[5]).removeClass('danger warning success').addClass('warning');
                        }
                    }
                });
            });
        }
    });
});

$("#filter-select").change(function(){
    var trs = $("#adjustments-table tbody tr");
    trs.show();
    var tr, q;
    var f = $(this).val();
    if(f == 'todo') return;
    for(var i = 0; i < trs.length; i++){
        tr = trs[i];
        q = +tr.cells[5].textContent;
        if(f == 'faltante'){
            if(q <= 0){
                $(tr).hide();
            }
        }else if (f == 'sobrante'){
            if(q >= 0){
                $(tr).hide();
            }
        }
    }
});
