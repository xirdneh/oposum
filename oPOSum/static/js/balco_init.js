if (typeof balco == 'undefined'){
    balco = Object.create(null);
    balco.print_branches_selector = function(elem, branches){
        var $ub = document.getElementById(elem);
        var $select = document.createElement("select");
        $select.setAttribute("name", "select_branches");
        $select.setAttribute("id", "select_branches");
        var $def = document.createElement("option");
        $def.value = "def";
        $def.setAttribute("name", "def");
        $def.text = "----";
        $select.appendChild($def);
        for (var i = 0; i < branches.length; i++){
            var branch = branches[i];
            var $option = document.createElement("option");
            $option.value = branch.pk;
            $option.setAttribute("name", branch.pk);
            $option.text = branch.fields.name;
            $select.appendChild($option);
        }
        var $label = document.createElement("label");
        $label.setAttribute("for", "select_branches");
        $label.innerHTML = "Sucursal: ";
        $ub.appendChild($label);
        $ub.appendChild($select);
    };

    balco.select_init_branch = function(elem, branch){ 
        var $sel = document.getElementById(elem);
        var $sb = branch;
        for (var i = 0; i < $sel.options.length; i++){
            var $op = $sel.options[i];
            if ($op.value == $sb){
                $sel.selectedIndex = i ;
                $sel.setAttribute("disabled","");
                break;
            }
        }
    };

    balco.get_cookie = function(name){
    cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
   };

   balco.search = function(event){
        event.preventDefault();
        $('.main_container').prepend('<div class="success_message"><span class="glyphicon glyphicon-refresh spinning-icon" ></span> Buscando producto...</div>');
        $('body').scrollTop(0);
        $.ajax({
            type:"get",
            url: "/products/get-product/" + $(this['q']).val(),
            success: function(data){
                if(data.status == 'ok'){
                    window.location = "/products/show-transactions/" + data.product.slug;
                }else{
                    window.location = "/products/search?q=" + data.slug;
                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                if(!console){return;}
                console.log(jqXHR);
            }
        });
   };

   balco.checkLocalServerRunning = function(resolve, reject){
       $.ajax({
           url:"http://localhost:9099/api/v1/get-printers",
           success: function(data){
               console.log('Local server running: ', data);
               resolve(true);
           },
           error: function(err){
               console.log('Local server is not running: ', err);
               reject(false);
           }
       });
   };

   balco.sendToPrinter = function(tb){
       $.ajax({
           url:"http://localhost:9099/api/v1/print",
           method: 'POST',
           data:tb,
           success: function(data){
               console.log("success: ", data);
           },
           error: function(err){
               console.log("error: ", err);
           }
       });
   };

   balco.convertToDate = function(dateTime){
       dateTimeArr = dateTime.split(' ');
       if (dateTimeArr.length !== 2){
           console.log('Wrong date format: ', dateTimeArr.length);
           return '';
       }
       date = dateTimeArr[0];
       time = dateTimeArr[1];
       dateArr = date.split('-');
       timeArr = time.split(':');
       return new Date(dateArr[0], +dateArr[1] - 1, dateArr[2], timeArr[0], timeArr[1], timeArr[2]);
   };
}
(function($){
    $(".navbar .search-box form").submit(balco.search);
    console.log("done");
})(jQuery);
