(function($) {

    function renumber_forms(forms) {
      var match = new RegExp('-\\d+-', 'g');
      forms.each(function (i, item) {
        $(item).find('input, label').each(function() {
          var name = $(this).attr('name');
          if (name) {
            $(this).attr('name', name.replace(match, '-' + i + '-'));
            $(this).attr('id', name.replace(match, '-' + i + '-'));
          }
        });
      });
    };


    function delete_form(item) {
      var form = $(item).closest('.quota-group');
      form.hide();
      form.find('input[id$="-DELETE"]').val(true);
      form.find('input.requested-quota').val(0);
    };


    function create_forms(opts, service_type) {
      var i = $('#quotas-' + service_type).find('.quota-group').length
      var prefix = String.fromCharCode('a'.charCodeAt() + i)

      var r = $('#empty-quotas-' + service_type).find('.quota-group').first().clone();

      r.find('input, label, select').each(function() {
        var name = $(this).attr('name');
        if (name) {
          $(this).attr('name', name.replace(/__prefix__/g, prefix));
          $(this).attr('id', name.replace(/__prefix__/g, prefix));
        }
      });

      r.find('.quota-group-delete').click(function() {
        delete_form($(this));
      });

      $('#quotas-' + service_type).append(r);
      r.show();
    }


    $.fn.formset = function(options) {
      var opts = $.extend({}, $.fn.formset.defaults, options);
      return this.each(function() {

        $('div[id^="quota-resource-"]').each(function() {
          var resource_id = $(this).attr('id').match(/[\d]+$/);
          if (resource_id == null) {
            return
          }
          var resource = opts['resources'][resource_id];
          // Set the labels for the resources
          $(this).find('.label-resource-name').text(resource['name']);
          $(this).find('.label-resource-unit').text(resource['unit']);

          if (resource['help_text']) {
            $(this).find('.label-resource-help').text(resource['help_text']);
          }
        });

        $('input:checkbox.toggle-quota').change(function() {
          var panel = $(this).closest('.panel');
          var enabled = this.checked;
          panel.find('.panel-collapse').collapse(this.checked ? 'show' : 'hide');

          // Set quotas to 0 if service is disabled
          if (!enabled) {
            panel.find('input.requested-quota').each(function() {
              $(this).val(0);
            });
          }

          // Set the value of hidden input field called enabled
          panel.find('input.quota-group-enabled').each(function() {
            $(this).val(enabled);
          });
        });


        $(this).find('div[id^="panel-quota-"]').each(function() {
          var service_type = $(this).attr('id').match(/[\w]+$/);
          var zones = opts['service_types'][service_type]['zones']

          /* If this is a multi-zone resource, show the 'Add more' button */
          if (zones.length > 1) {
            $('input[id^="add-quota-' + service_type + '"]').show();
          } else {
            $('input[id^="add-quota-' + service_type + '"]').hide();
          }

          var is_enabled = false;
          $(this).find('input.requested-quota').each(function() {
            if (this.value > 0) {
              is_enabled = true;
            }
          });

          var toggle = $(this).find('input:checkbox.toggle-quota');
          if (toggle.length) {
            $(this).find('div.panel-collapse').collapse(is_enabled ? 'show' : 'hide');
            toggle.prop('checked', is_enabled).change();
          }
        });

        $('input[id^="add-quota-"]').click(function() {
          var service_type = $(this).attr('id').match(/[\w]+$/);
          create_forms(opts, service_type);
        });

      });
    };

    // Plugin defaults – added as a property on our plugin function.
    $.fn.formset.defaults = {
       prefix: "",
       service_types: {},
       resources: {},
       zones: {},
    };
}(jQuery));


//help icon span click
$('.help-icon-sp').on('click', function(event){
    event.preventDefault();
    var help_icon_sp = $(this);
    var help_id = help_icon_sp.attr('id');
    var title = help_icon_sp.attr('title');
    var help_message = " ";
    var help_msg_div = $('div[id="'+ help_id +'"]');
    help_message = help_msg_div.html();
    show_help_message(help_icon_sp, title, help_message);
});

//show help message
function show_help_message(el, help_title, help_message) {
    $(el).mDialog({
        title:help_title,
        content:help_message,
        close_on_body_click:true,
        width:450
    });
    return false;
}

(function($) {

    function create_form_row(formset, opts) {
        if(opts.show_label == true){
            show_label_div(opts);
        }
        var total_rows = $('div.'+ opts.formset_class_id + ' table > tbody > tr').length;
        var form_new_row = create_row(opts.prefix, total_rows, opts);
        $('div.'+ opts.formset_class_id + ' table > tbody:last').append(form_new_row);
        total_rows +=1;
        var total_forms_input = $('#id_' + opts.prefix + '-TOTAL_FORMS');
        total_forms_input.val(total_rows);
    };

    function show_label_div(opts){
        var label_div = $('div.'+ opts.formset_class_id + ' div.label_header');
        label_div.attr('class','label_header');
    }

    function hide_label_div(opts){
        var label_div = $('div.'+ opts.formset_class_id + ' div.label_header');
        label_div.attr('class','label_header hidden');
    }

    function create_row(prefix, count, opts){
        var new_row = "<tr>";
        new_row += "<td>";
        new_row += "<input id='id_" + prefix + "-" + count + "-id' name='" + prefix + "-" + count + "-id' type='hidden'>";
        new_row += "<input id='id_" + prefix + "-" + count + "-DELETE' type='hidden' value='False' name='" + prefix + "-" + count + "-DELETE'>";
        new_row += "</td>";
        new_row += "<td>";
        new_row += "<div class='form-group'>";
        new_row += "<div class='controls'>";
        var input_style_css = opts.input_style_css;
        if (input_style_css != ''){
            new_row += "<div class='input-group " + input_style_css +"'>";
        }else{
            new_row += "<div class='input-group'>";
        }
        new_row += "<input class='form-control' id='id_" + prefix + "-" + count + "-" + opts.field_name + "' maxlength='255' name='" + prefix + "-" + count + "-" + opts.field_name + "' type='text'>";
        new_row += "</div> </div></div>";
        new_row += "</td>";
        new_row += "<td>" ;
        new_row += "<span title='remove' id='id_" + prefix + "-" + count + "-" + opts.field_name +"' class='delete-icon-sp'> &nbsp; &nbsp;<img class='delete-icon' src='/static/rcportal/img/delete.png'> &nbsp; &nbsp; </span>"
        new_row += "</td>";
        new_row += "</tr>";
        return new_row;
    };

    function delete_form_row(formset, opts, span){
        var span_id = span.attr('id');
        var current_tr = span.closest('tr');
        //check the input id field is empty or not
        var id_input = current_tr.find('input[id$=-id]');

        var id_value = id_input.attr('value');
        if (id_value == null || id_value == ''){
            //just remove the current row as it's a new row.
            // and resort the whole table rows
            current_tr.remove();
            resort_form_rows(formset, opts);
        } else{
            //check the input delete field
            var del_input_field = current_tr.find('input[id$=-DELETE]');
            //set the delete flag to true
            del_input_field.attr('value', 'True');
            current_tr.toggleClass('hidden');
        }

        //reset the total_forms_input value
        var total_rows = $('div.'+ opts.formset_class_id + ' table > tbody > tr').length;
        var total_hidden_rows = $('div.'+ opts.formset_class_id + ' table > tbody > tr.hidden').length;
        var total_forms_input = $('#id_' + opts.prefix + '-TOTAL_FORMS');
        total_forms_input.val(total_rows);
        if ((total_rows == 0 || total_rows == total_hidden_rows ) && opts.show_label == true){
            hide_label_div(opts);
        }
    };

    function resort_form_rows(formset, opts){
        $('div.'+ opts.formset_class_id + ' table > tbody > tr').each(function(){
            var current_index = this.rowIndex;

            //reindex the id input field
            var id_input = $(this).find('input[id$=-id]');
            id_input.attr('id','id_' + opts.prefix + '-' + current_index + '-id' );
            id_input.attr('name', opts.prefix + '-' + current_index + '-id');

            //reindex the delete input field
            var id_input = $(this).find('input[id$=-DELETE]');
            id_input.attr('id','id_' + opts.prefix + '-' + current_index + '-DELETE' );
            id_input.attr('name', opts.prefix + '-' + current_index + '-DELETE');

            //reindex the name input field
            var name_input = $(this).find('input[id$=-' + opts.field_name + ']');
            var new_id = 'id_' + opts.prefix + '-' + current_index + '-' + opts.field_name;
            name_input.attr('id', new_id);
            name_input.attr('name', opts.prefix + '-' + current_index + '-' + opts.field_name);

            //reindex the span
            var span_del = $(this).find('span[id$=-' + opts.field_name +']');
            span_del.attr('id',new_id );
        });
    };

    $.fn.mformset = function(options) {
        var opts = $.extend( {}, $.fn.mformset.defaults, options );

         return this.each(function() {
             //set current formset
             var formset = this;
             $('div.' + options.formset_class_id).on('click', '#add_another', function (event) {
                 event.preventDefault();
                 create_form_row(formset, opts);
             });

             $('div.'+ options.formset_class_id).on('click', '.delete-icon-sp', function (event){
                 event.preventDefault();
                 var clicked_span = $(this);
                 delete_form_row(formset, opts, clicked_span);
             });
         });
    };

    $.fn.mformset.defaults = {
        form_prefix: "",
        formset_class_id: "",
        field_name:"",
        input_style_css:"",
        show_label: false
    };

}(jQuery));
(function($) {
    function create_form_row(formset, opts) {
        var total_rows = $('div.'+ opts.formset_class_id + ' table > tbody > tr').length;
        var form_new_row = create_row(opts.prefix, total_rows, opts);
        $('div.'+ opts.formset_class_id + ' table > tbody:last').append(form_new_row);
        total_rows += 1;
        var total_forms_input = $('#id_' + opts.prefix + '-TOTAL_FORMS');
        total_forms_input.val(total_rows);
    };

    function create_row(prefix, row_index, opts){
        var new_row = "<tr>";
        new_row += "<td>";
        new_row += "<input type='hidden' name='" + opts.prefix + "-" + row_index + "-id' id='id_" + opts.prefix + "-" + row_index + "-id'>";
        new_row += "<input type='hidden' name='" + opts.prefix + "-" + row_index + "-DELETE' id='id_" + opts.prefix + "-" + row_index + "-DELETE'>";
        new_row += "</td>";
        new_row += "<td>";
        new_row += "<div class='grant_div'>";
        //type
        new_row += "<div class='form-group '>";
        new_row += create_input_field_label(opts, 'grant_type', 'Type', row_index, true);
        new_row += "<div class='controls'>";
        new_row += "<div class='input-group'>";
        new_row += create_type_options(opts, 'grant_type', row_index);
        new_row += "</div>";
        new_row += "</div>";
        new_row += "</div>";
        new_row += create_help_span(opts, 'grant_type', row_index, 'Choose the grant type from the dropdown options.');
        //funding body_scheme
        new_row += "<div class='form-group '>";
        new_row += create_input_field_label(opts, 'funding_body_scheme', 'Funding body and scheme', row_index, true);
        new_row += "<div class='controls'>";
        new_row += "<div class='input-group'>";
        new_row += create_input_field(opts, 'funding_body_scheme', 'Funding body and scheme', row_index);
        new_row += "</div>";
        new_row += "</div>";
        new_row += "</div>";
        new_row += create_help_span(opts, 'funding_body_scheme', row_index, 'For example, ARC Discovery Project.');
        //first_year_funded
        new_row += "<div class='form-group '>";
        new_row += create_input_field_label(opts, 'first_year_funded', 'First year funded', row_index, true);
        new_row += "<div class='controls'>";
        new_row += "<div class='input-group'>";
        new_row += create_year_input_field(opts, 'first_year_funded', row_index);
        new_row += "</div>";
        new_row += "</div>";
        new_row += "</div>";
        new_row += create_help_span(opts, 'first_year_funded', row_index, 'Specify the first year funded');
        //last_year_funded
        new_row += "<div class='form-group '>";
        new_row += create_input_field_label(opts, 'last_year_funded', 'Last year funded', row_index, true);
        new_row += "<div class='controls'>";
        new_row += "<div class='input-group'>";
        new_row += create_year_input_field(opts, 'last_year_funded', row_index);
        new_row += "</div>";
        new_row += "</div>";
        new_row += "</div>";
        new_row += create_help_span(opts, 'last_year_funded', row_index, 'Specify the last year funded');
        //total funding
        new_row += "<div class='form-group '>";
        new_row += create_input_field_label(opts, 'total_funding', 'Total funding (AUD)', row_index, true);
        new_row += "<div class='controls'>";
        new_row += "<div class='input-group'>";
        new_row += create_number_input_field(opts, 'total_funding', '0', row_index);
        new_row += "</div>";
        new_row += "</div>";
        new_row += "</div>";
        new_row += create_help_span(opts, 'total_funding', row_index, 'Total funding amount in AUD.');
        //grant id
        new_row += "<div class='form-group '>";
        new_row += create_input_field_label(opts, 'grant_id', 'Grant ID', row_index, false);
        new_row += "<div class='controls'>";
        new_row += "<div class='input-group'>";
        new_row += create_input_field(opts, 'grant_id', 'Grant ID', row_index);
        new_row += "</div>";
        new_row += "</div>";
        new_row += "</div>";
        new_row += create_help_span(opts, 'grant_id', row_index, 'Specify the grant id.');
        // closed grant_div
        new_row += "</div>"
        new_row += "</td>";
        new_row += "<td>";
        new_row += "<button type='button' id='delete-grant' class='btn btn-danger'>";
        new_row += "Delete";
        new_row += "</button>";
        new_row += "</td>";
        new_row += "</tr>";
        return new_row;
    };

    function create_input_field_label(opts, field_name, field_label, row_index, required){
        label_section = "<label for='id_"+ opts.prefix + "-" + row_index + "-" + field_name +"'>";
        label_section += field_label;
        if(required == true){
            label_section += "<span class='glyphicon glyphicon-asterisk text-danger'></span>";
        }
        label_section += "&nbsp;&nbsp;&nbsp;<span class='help-icon-sp' id='id_" + opts.prefix + "-" + row_index + "-" + field_name + "' title='" + field_label + "'>";
        label_section += "<img src='/static/rcportal/img/help.png' class='help-icon'>";
        label_section += "</span>";
        label_section += "</label>";
        return label_section;
    };

    function create_type_options(opts, field_name, row_index){
        var select = "<select name='"+ opts.prefix + "-" + row_index + "-" + field_name + "' id='id_" + opts.prefix + "-" + row_index + "-" + field_name +"' class='form-control'>";
        select += "<option selected='selected' value='comp'>Australian competitive research grant</option>";
        select += "<option value='ncris'>NCRIS funding</option>";
        select += "<option value='ands_nectar_rds'>ANDS, Nectar, RDS funding</option>";
        select += "<option value='nhmrc'>NHMRC</option>";
        select += "<option value='govt'>Other Australian government grant</option>";
        select += "<option value='industry'>Industry funding</option>";
        select += "<option value='ext'>Other external funding</option>";
        select += "<option value='inst'>Institutional research grant</option>";
        select += "</select>";
        return select;
    };

    function create_help_span(opts, field_name, row_index, help_txt){
        var help_span = "<span class='help-block'>";
        help_span += "<div class='help-text-div' id='id_" + opts.prefix + "-" + row_index +"-" + field_name + "'>";
        help_span += help_txt;
        help_span += "</div>";
        help_span += "</span>";
        return help_span;
    };

    function create_input_field(opts, field_name, field_label, row_index){
        return "<input type='text' name='" + opts.prefix + "-" + row_index + "-" + field_name + "' maxlength='200' id='id_" + opts.prefix + "-" + row_index + "-" + field_name + "' class='form-control'>";
    };

    function create_number_input_field(opts, field_name, defalut_value, row_index){
        return "<input type='number' name='" + opts.prefix + "-" + row_index + "-" + field_name
            + "' maxlength='200' id='id_" + opts.prefix + "-" + row_index + "-" + field_name
            + "' class='form-control' " + "value='" + defalut_value + "' min='0'>";
    };

    function create_year_input_field(opts, field_name, row_index){
       return "<input type='number' name='" + opts.prefix + "-" + row_index
           + "-" + field_name + "' value='' id='id_" + opts.prefix + "-"
           + row_index + "-" + field_name + "' min='1970' max='3000' class='form-control'>"
    };

    function delete_form_row(formset, opts, span){
        var span_id = span.attr('id');
        var current_tr = span.closest('tr');
        //check the input id field is empty or not
        var id_input = current_tr.find('input[id$=-id]');

        var id_value = id_input.attr('value');
        if (id_value == null || id_value == ''){
            //just remove the current row as it's a new row.
            // and resort the whole table rows
            current_tr.remove();
            resort_form_rows(formset, opts);
        } else{
            //check the input delete field
            var del_input_field = current_tr.find('input[id$=-DELETE]');
            //set the delete flag to true
            del_input_field.attr('value', 'True');
            current_tr.toggleClass('hidden');
        }
        //reset the total_forms_input value
        var total_rows = $('div.'+ opts.formset_class_id + ' table > tbody > tr').length;
        var total_forms_input = $('#id_' + opts.prefix + '-TOTAL_FORMS');
        total_forms_input.val(total_rows);
    };

    function resort_form_rows(formset, opts){
        var match = new RegExp(opts.prefix + '-\\d+-', 'g');

        $('div.'+ opts.formset_class_id + ' table > tbody > tr').each(function() {
            var current_index = this.rowIndex;
            //reindex the id input field
            var id_input = $(this).find('input[id$=-id]');
            id_input.attr('id', 'id_' + opts.prefix + '-' + current_index + '-id');
            id_input.attr('name', opts.prefix + '-' + current_index + '-id');
            //reindex the delete input field
            var id_input = $(this).find('input[id$=-DELETE]');
            id_input.attr('id', 'id_' + opts.prefix + '-' + current_index + '-DELETE');
            id_input.attr('name', opts.prefix + '-' + current_index + '-DELETE');

            //reindex the label for
            $(this).find("label[for^='id_" + opts.prefix + "-']").each(function(){
                var labelFor = $(this).attr('for').replace(match, opts.prefix +'-' + current_index + '-');
                $(this).attr('for', labelFor);
            });

            //reindex help icon span id
            $(this).find("span.help-icon-sp").each(function(){
               var newHelpSpanId = $(this).attr('id').replace(match, opts.prefix + '-' + current_index + '-');
                $(this).attr('id', newHelpSpanId);
            });

            //reindex select id and name
            $(this).find("select.form-control").each(function(){
                var selectId = $(this).attr('id').replace(match, opts.prefix + '-' + current_index + '-');
                var selectName = $(this).attr('name').replace(match, opts.prefix + '-' + current_index + '-');
                $(this).attr('id', selectId);
                $(this).attr('name', selectName);
            });

            //reindex the input id and name
            $(this).find("input.form-control").each(function(){
                var inputId = $(this).attr('id').replace(match, opts.prefix + '-' + current_index + '-');
                var inputName = $(this).attr('name').replace(match, opts.prefix + '-' + current_index + '-');
                $(this).attr('id', inputId);
                $(this).attr('name', inputName);
            });

            //reindex help text div help-text-div
            $(this).find("div.help-text-div").each(function(){
               var newHelpTextDivId = $(this).attr('id').replace(match, opts.prefix + '-' + current_index + '-');
                $(this).attr('id', newHelpTextDivId);
            })
        });
    };

    $.fn.gformset = function(options) {
        var opts = $.extend( {}, $.fn.gformset.defaults, options );
         return this.each(function() {
             //set current formset
             var formset = this;
             $('div.' + options.formset_class_id).on('click', '#add_another', function (event) {
                 event.preventDefault();
                 create_form_row(formset, opts);
             });

             $('div.'+ options.formset_class_id).on('click', '#delete-grant', function (event){
                 event.preventDefault();
                 var clicked_span = $(this);
                 delete_form_row(formset, opts, clicked_span);
             });

            $('div.'+ options.formset_class_id).on('click', '.help-icon-sp', function (event){
                event.preventDefault();
                var clicked_span = $(this);
                var help_id = clicked_span.attr('id');
                var title = clicked_span.attr('title');
                var help_msg_div = $('div[id="'+ help_id +'"]');
                var help_message = " ";
                help_message = help_msg_div.html();
                show_help_message(clicked_span, title, help_message);
            });
         });
    };

    $.fn.gformset.defaults = {
        form_prefix: "",
        formset_class_id: ""
    };

}(jQuery));

//date picker
$(function() {
    $(".datepicker2").datepicker({
        autoclose: true,
        changeMonth: true,
        changeYear: true,
        format: 'yyyy-mm-dd',
        todayHighlight: true,
    });
});

$("form#new-allocation").on("change","#id_start_date", function() {
    var input_start_date = $(this).val();
    // get the duration in months
    var duration = $("select#id_estimated_project_duration").val();
    //convert diff hours between start date and duration in months
    var diff_hours = convert_diff_days(input_start_date, duration);
    // find number of cores
    var input_number_cores = $("input#id_cores");
    var number_cores = parseInt(input_number_cores.val());
    change_core_hours(number_cores, diff_hours);
});

$("form#new-allocation").on("change","#id_estimated_project_duration", function() {
    // get the duration in months
    var duration = $(this).val();
    // get the start date
    var input_start_date = $("input#id_start_date").val();
    //convert diff hours between start date and duration in months
    var diff_hours = convert_diff_days(input_start_date, duration);
    // find number of cores
    var input_number_cores = $("input#id_cores");
    var number_cores = parseInt(input_number_cores.val());
    // change the core hours
    change_core_hours(number_cores, diff_hours);
});

$("form#new-allocation").on("change","#id_cores", function() {
    // get the cores
    var number_cores = parseInt($(this).val());
    // get the start date
    var input_start_date = $("input#id_start_date").val();
    // get the duration in months
    var duration = $("select#id_estimated_project_duration").val();
    //convert diff hours between start date and duration in months
    var diff_hours = convert_diff_days(input_start_date, duration);
    // change the core hours
    change_core_hours(number_cores, diff_hours);
});

$("form#new-allocation").on("change","#id_requester_is_ci", function() {
    // Get the current value
    var currentValue = $("select#id_requester_is_ci").val();
    // If the value has changed to "Yes"
    if (currentValue == "yes") {
      // Get current requester details
      var title = $("input#id_requester_title").val();
      var given_name = $("input#id_requester_given_name").val();
      var surname = $("input#id_requester_surname").val();
      var contact_email = $("input#id_contact_email").val();
      // Set CI details to be the same
      $("input#id_investigators-0-title").val(title);
      $("input#id_investigators-0-given_name").val(given_name);
      $("input#id_investigators-0-surname").val(surname);
      $("input#id_investigators-0-email").val(contact_email);
    }
});

function convert_diff_days(input_start_date, duration_in_month){
    var one_hour_time =1000*60*60;
    var start_date =  new Date(input_start_date);
    var end_date = new Date(input_start_date);
    end_date.setMonth(end_date.getMonth() + parseInt(duration_in_month));
    var hours_diff = Math.round((end_date.getTime() - start_date.getTime()) / one_hour_time);
    return hours_diff;
}

function change_core_hours(number_of_cores, hours_diff){
    var estimated_core_hours =Math.round(number_of_cores * hours_diff * 0.5);
    var input_number_core_hours = $("input#id_core_hours");
    input_number_core_hours.val(estimated_core_hours);
}
