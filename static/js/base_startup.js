String.prototype.rsplit = function(sep, maxsplit) {
  var split = this.split(sep);
  return maxsplit ? [ split.slice(0, -maxsplit).join(sep) ].concat(split.slice(-maxsplit)) : split;
};

$(document).ready(function() {

$('#nav-menu').menu();
//$('#nav-menu').menu({position: {my: "top left", at: "bottom left"}});

$('.datetimepicker').datetimepicker({
  dateFormat: 'mm/dd/yy',
  timeFormat: 'hh:mm TT',
});

});
