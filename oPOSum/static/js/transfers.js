var $prod;
var pci = $('#product_code');
if(pci){
    pci.keyup(function(e){
        if(e.keyCode == 13){
            var val = pci.val().split("*");
            var code, qty, price;
            if(val.length > 1){
                code = val[1];
                qty = +val[0];
            }else{
                code = val[0];
                qty = 1;
            }
            $.ajax({
                method: 'GET',
                url: '/products/get-product/' + code,
                success: function(data){
                    $prod = data.product;
                    if(data.status === 'ok' && data.message === 'Existente'){
                        add_prod_table($prod, qty, null);
                        pci.val('');
                        pci.focus();
                    }
                }
            });
        }
    });
}

function add_prod_table(p, q, pr){
    var t = $('#transfer-prods');
    var tbody = t.find('tbody');
    var trs = tbody.find('tr');
    var tr = $(trs[trs.length - 1]);
    var tds = tr.find('td');
    var td = $(tds[0]);
    var id = 0;
    if(td.text() !== ''){
        id = +td.text();
    }
    id += 1;
    var row = $('<tr>' +
        '<td>' + id + '</td>' + 
        '<td>' + p.slug + '</td>' +
        '<td>' + p.description + '</td>' + 
        '<td>' + q + '</td>' + 
        '</tr>' );
    row.on('dblclick', delete_row);
    tbody.append(row);
    var tots = get_table_totals([{label:'Total', index:4, qty:3}], t);
    print_table_totals(tots, $('.transfer-totals'));
}

function delete_row(){
    var r = confirm('Desea borrar este articulo?');
    if(!r){
        return;
    }
    var row = $(this);
    var tbody = row.parent();
    row.remove();
    var id = 0;
    var trs = tbody.find('tr');
    var td, tr;
    for(var i = 0; i < trs.length; i++){
        tr = $(trs[i]);
        td = $(tr.find('td')[0]);
        id++;
        td.text(id);
    }
    var tots = get_table_totals([{label:'Total', index:4, qty:3}], tbody.parent());
    print_table_totals(tots, $('.transfer-totals'));
}

function get_table_totals(objs, table){
    var tbody = table.find('tbody');
    var trs = tbody.find('tr');
    var tds, tr, td, tots = {}, val, qty;
    for(var j = 0; j < trs.length; j++){
        tr = $(trs[j]);
        tds = tr.find('td');
        for(var i = 0; i < objs.length; i++){
            o = objs[i];
            qty = $(tds[o.qty]).text();
            if(!isNaN(qty))
            if(tots[o.label]){
                tots[o.label] += qty;
            } else{
                tots[o.label] = qty;
            }
        }
    }
}

function print_table_totals(tots, el){
    el.html('');
    for(var o in tots){
        if(tots.hasOwnProperty(0)){
            el.append('<div class="tbl-tot tot-' + o + '"><span class="tot-label>' + o + ':</span> <span class="value"> ' + tots[o] + '</span></div>');
        }
    }
}

function get_table_data(t, o){
    var tbody = t.find('tbody');
    var trs = tbody.find('tr');
    var tds, to, td;
    var ret = [];
    var i = 0;
    trs.each(function(index){
        tds = $(this).find('td');
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

function save_transfer(data){
    var csrftoken = balco.get_cookie('csrftoken');
    csrftoken = balco.get_cookie('csrftoken');
    var d = {
        products: data,
        branch_from: $('#select_branches').val(),
        branch_to: $('#destiny_branch_select').val(),
    };

    $.ajax({
        crossDomain: false,
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        method: 'POST',
        data: {data: JSON.stringify(d)},
        url: '/inventory/transfers/save-transfer/',
        success: function(data){
            if(data.status === 'ok'){
                setTimeout(function(){window.location.reload();}, 250);
                //print_transfer_ticket(data);
            }
        }
    });
}

var form = $('#transfer-save');
form.submit(function(e){
    e.preventDefault();
    data = get_table_data($('#transfer-prods'), ['id', 'code', 'desc', 'qty']);
    $('#transfer-submit').prop('disabled', true);
    save_transfer(data);
});
