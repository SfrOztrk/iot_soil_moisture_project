// Event listener for button value changes.
$(document).ready(function() {
    // off-on button event listener
    $("input[type=checkbox].off-on").click(function() {   // if click off-on checkbox
        $("input[type=checkbox].auto").prop("checked", false)   // disable the auto mode

        if ($(this).prop("checked") == true) {    // if off-on checkbox is checked now
            payload = { 
                "level": 0
            }    
        }
        else {
            payload = { 
                "level": 1
            }  
        }

        postUpdate(payload);
    });


    // auto button event listener
    $("input[type=checkbox].auto").click(function() {   // if click auto button

        if ($(this).prop("checked") == true) {   // if auto button is checked now
         
        } 
        else {
       
        }

    });

    // Initialise slider value form state on server.
    getState() 
});

// GET request to server to retrieve water pump state.
function getState() {
    $.get("/pump", function(serverResponse) {          
    console.log(serverResponse)
    updateControls(serverResponse)                                   
    });
}


// POST Request to server to set water pump state.
function postUpdate(payload) {
    $.post("/pump", payload, function(serverResponse) {
        console.log(serverResponse);
        updateControls(serverResponse);
    });
}


function updateControls(data) {
    str = "";
    if (data.level == 1) {
        str = "Off"
        $("input[type=checkbox].off-on").prop("checked", false)
    }
    else {
        $("input[type=checkbox].off-on").prop("checked", true)
        str = "On"
    }
    $("#pumpState").html(str);
}