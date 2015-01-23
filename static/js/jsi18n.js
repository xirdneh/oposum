

(function (globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function (n) {
    var v=(n != 1);
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  
  /* gettext library */

  django.catalog = {
    "%(sel)s of %(cnt)s selected": [
      "%(sel)s de %(cnt)s seleccionado", 
      "%(sel)s de  %(cnt)s seleccionados"
    ], 
    "6 a.m.": "6 a.m.", 
    "Available %s": "%s Disponibles", 
    "Calendar": "Calendario", 
    "Cancel": "Cancelar", 
    "Choose": "Elegir", 
    "Choose a time": "Elige una hora", 
    "Choose all": "Selecciona todos", 
    "Chosen %s": "%s Elegidos", 
    "Click to choose all %s at once.": "Haz clic para seleccionar todos los %s de una vez", 
    "Click to remove all chosen %s at once.": "Haz clic para eliminar todos los %s elegidos", 
    "Clock": "Reloj", 
    "Filter": "Filtro", 
    "Hide": "Esconder", 
    "January February March April May June July August September October November December": "Enero Febrero Marzo Abril Mayo Junio Julio Agosto Septiembre Octubre Noviembre Diciembre", 
    "Midnight": "Medianoche", 
    "Noon": "Mediod\u00eda", 
    "Now": "Ahora", 
    "Remove": "Remover", 
    "Remove all": "Eliminar todos", 
    "S M T W T F S": "D L M M J V S", 
    "Show": "Mostrar", 
    "This is the list of available %s. You may choose some by selecting them in the box below and then clicking the \"Choose\" arrow between the two boxes.": "Esta es la lista de %s disponibles. Puedes elegir algunos seleccion\u00e1ndolos en la caja inferior y luego haciendo clic en la flecha \"Elegir\" que hay entre las dos cajas.", 
    "This is the list of chosen %s. You may remove some by selecting them in the box below and then clicking the \"Remove\" arrow between the two boxes.": "Esta es la lista de los %s elegidos. Puedes elmininar algunos seleccion\u00e1ndolos en la caja inferior y luego haciendo click en la flecha \"Eliminar\" que hay entre las dos cajas.", 
    "Today": "Hoy", 
    "Tomorrow": "Ma\u00f1ana", 
    "Type into this box to filter down the list of available %s.": "Escribe en este cuadro para filtrar la lista de %s disponibles", 
    "Yesterday": "Ayer", 
    "You have selected an action, and you haven't made any changes on individual fields. You're probably looking for the Go button rather than the Save button.": "Has seleccionado una acci\u00f3n y no has hecho ning\u00fan cambio en campos individuales. Probablemente est\u00e9s buscando el bot\u00f3n Ejecutar en lugar del bot\u00f3n Guardar.", 
    "You have selected an action, but you haven't saved your changes to individual fields yet. Please click OK to save. You'll need to re-run the action.": "Has seleccionado una acci\u00f3n, pero no has guardado los cambios en los campos individuales todav\u00eda. Pulsa OK para guardar. Tendr\u00e1s que volver a ejecutar la acci\u00f3n.", 
    "You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost.": "Tienes cambios sin guardar en campos editables individuales. Si ejecutas una acci\u00f3n, los cambios no guardados se perder\u00e1n."
  };

  django.gettext = function (msgid) {
    var value = django.catalog[msgid];
    if (typeof(value) == 'undefined') {
      return msgid;
    } else {
      return (typeof(value) == 'string') ? value : value[0];
    }
  };

  django.ngettext = function (singular, plural, count) {
    var value = django.catalog[singular];
    if (typeof(value) == 'undefined') {
      return (count == 1) ? singular : plural;
    } else {
      return value[django.pluralidx(count)];
    }
  };

  django.gettext_noop = function (msgid) { return msgid; };

  django.pgettext = function (context, msgid) {
    var value = django.gettext(context + '\x04' + msgid);
    if (value.indexOf('\x04') != -1) {
      value = msgid;
    }
    return value;
  };

  django.npgettext = function (context, singular, plural, count) {
    var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
    if (value.indexOf('\x04') != -1) {
      value = django.ngettext(singular, plural, count);
    }
    return value;
  };
  

  django.interpolate = function (fmt, obj, named) {
    if (named) {
      return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
    } else {
      return fmt.replace(/%s/g, function(match){return String(obj.shift())});
    }
  };


  /* formatting library */

  django.formats = {
    "DATETIME_FORMAT": "j \\d\\e F \\d\\e Y \\a \\l\\a\\s H:i", 
    "DATETIME_INPUT_FORMATS": [
      "%d/%m/%Y %H:%M:%S", 
      "%d/%m/%Y %H:%M:%S.%f", 
      "%d/%m/%Y %H:%M", 
      "%d/%m/%y %H:%M:%S", 
      "%d/%m/%y %H:%M:%S.%f", 
      "%d/%m/%y %H:%M", 
      "%Y-%m-%d %H:%M:%S", 
      "%Y-%m-%d %H:%M:%S.%f", 
      "%Y-%m-%d %H:%M", 
      "%Y-%m-%d"
    ], 
    "DATE_FORMAT": "j \\d\\e F \\d\\e Y", 
    "DATE_INPUT_FORMATS": [
      "%d/%m/%Y", 
      "%d/%m/%y", 
      "%Y-%m-%d"
    ], 
    "DECIMAL_SEPARATOR": ",", 
    "FIRST_DAY_OF_WEEK": "1", 
    "MONTH_DAY_FORMAT": "j \\d\\e F", 
    "NUMBER_GROUPING": "3", 
    "SHORT_DATETIME_FORMAT": "d/m/Y H:i", 
    "SHORT_DATE_FORMAT": "d/m/Y", 
    "THOUSAND_SEPARATOR": ".", 
    "TIME_FORMAT": "H:i:s", 
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S", 
      "%H:%M:%S.%f", 
      "%H:%M"
    ], 
    "YEAR_MONTH_FORMAT": "F \\d\\e Y"
  };

  django.get_format = function (format_type) {
    var value = django.formats[format_type];
    if (typeof(value) == 'undefined') {
      return format_type;
    } else {
      return value;
    }
  };

  /* add to global namespace */
  globals.pluralidx = django.pluralidx;
  globals.gettext = django.gettext;
  globals.ngettext = django.ngettext;
  globals.gettext_noop = django.gettext_noop;
  globals.pgettext = django.pgettext;
  globals.npgettext = django.npgettext;
  globals.interpolate = django.interpolate;
  globals.get_format = django.get_format;

}(this));
