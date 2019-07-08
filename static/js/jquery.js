//Add aditional ingredient row
$(document).ready(function(){
	$('#addrow').click(function() {
		$('<input class="form-control is-invalid" id="ingredient" name="ingredient" required type="text" value="">').insertBefore('#addrow');	
		
	});	
	
	// Remove aditional row
	$('#removerow').click(function() {
		$('#ingredientList input:last').remove();
	});
	
	
	//Add aditional preparations step row
	$('#addrowSteps').click(function() {
		$('<input class="form-control is-invalid" id="step" name="step" required type="text" value="">').insertBefore('#addrowSteps');

	});	
	
	
		// Remove aditional preparation step row
	$('#removerowSteps').click(function() {
		$('#stepList input:last').remove();
	});
	
	
	// Hide allergens menu
	$('#allergens li').hide() 
	
	
	// Show allergens on click function 
	$('.fa-angle-down').click(function() {
	    $('#allergens li').slideDown(600)
	    	
	});
	
	
	// Love button
 
	$('.btn-counter').on('click', function() {
	  
	  
	  var $this = $(this),
	      count = $this.attr('data-count'),
	      multiple = $this.hasClass('multiple-count');
		 $this.attr('data-count', multiple ? ++ count : --count  );
	      
	  
		});
  
  
});	
  
  
  
	
	
	
	
	
	
	    
	
	

