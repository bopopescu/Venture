$(document).ready(function(){    
     $(function(){
        $('#menu').slicknav({
            'prependTo':'nav',
        });
    });
             
        
    $("#companyinterestcountry").click(function(){
        $("#companyinterestdropdown").slideToggle();
    });
    
    $(".partners-filter").click(function(){
        $("#filter-dropdown-item").slideToggle();
    });
    $( "#files" ).selectmenu();
    $('#choosenactive').chosen();
  


    
    
});