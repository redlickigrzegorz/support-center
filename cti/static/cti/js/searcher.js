$(document).ready(function(){
	$('#header').load('../header-ads.html');
$('#footer').load('../footer-ads.html');
    var data = [
{"id":"1","employee_name":"Tiger Nixon","employee_salary":"320800","employee_age":"61","profile_image":"default_profile.png"},{"id":"2","employee_name":"Garrett Winters","employee_salary":"434343","employee_age":"63","profile_image":"default_profile.png"},{"id":"3","employee_name":"Ashton Cox","employee_salary":"86000","employee_age":"66","profile_image":"default_profile.png"},{"id":"4","employee_name":"Cedric Kelly","employee_salary":"433060","employee_age":"22","profile_image":"default_profile.png"},{"id":"5","employee_name":"Airi Satou","employee_salary":"162700","employee_age":"33","profile_image":"default_profile.png"},{"id":"6","employee_name":"Brielle Williamson","employee_salary":"372000","employee_age":"61","profile_image":"default_profile.png"},{"id":"7","employee_name":"Herrod Chandler","employee_salary":"137500","employee_age":"59","profile_image":"default_profile.png"},{"id":"8","employee_name":"Rhona Davidson","employee_salary":"327900","employee_age":"55","profile_image":"default_profile.png"},{"id":"9","employee_name":"Colleen Hurst","employee_salary":"205500","employee_age":"39","profile_image":"default_profile.png"},{"id":"10","employee_name":"Sonya Frost","employee_salary":"103600","employee_age":"23","profile_image":"default_profile.png"}];

$('#searched_text').keyup(function(){
            var searchField = $(this).val();
			if(searchField === '')  {
				$('#filter-records').html('');
				return;
			}

            var regex = new RegExp(searchField, "i");
            var output = '<div class="row">';
            var count = 1;
			  $.each(data, function(key, val){
				if ((val.employee_salary.search(regex) != -1) || (val.employee_name.search(regex) != -1)) {
				  output += '<div class="col-md-6 well">';
				  output += '<div class="col-md-3"><img class="img-responsive" src="'+val.profile_image+'" alt="'+ val.employee_name +'" /></div>';
				  output += '<div class="col-md-7">';
				  output += '<h5>' + val.employee_name + '</h5>';
				  output += '<p>' + val.employee_salary + '</p>'
				  output += '</div>';
				  output += '</div>';
				  if(count%2 == 0){
					output += '</div><div class="row">'
				  }
				  count++;
				}
			  });
			  output += '</div>';
			  $('#filter-records').html(output);
        });
  });