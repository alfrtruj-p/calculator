
function disablePreservation() {
    if (document.getElementById("type").value == "digital")
    {
        document.getElementById("data").disabled=false;
        document.getElementById("visual").disabled=true;
        document.getElementById("page").disabled=true;
    }
    else if (document.getElementById("type").value == "visual")
    {
        document.getElementById("data").disabled=true;
        document.getElementById("visual").disabled=false;
        document.getElementById("page").disabled=false;
    }
    else (document.getElementById("type").value == "hybrid")
    {
        document.getElementById("digital").disabled=false;
        document.getElementById("visual").disabled=false;
        document.getElementById("page").disabled=false;
    }
}


function disableAwa() {
    if (document.getElementById("awa").value == "no")
    {
        document.getElementById("contribution").disabled=true;
        document.getElementById("storage").disabled=true;
    }
    else
    {
        document.getElementById("contribution").disabled=false;
        document.getElementById("storage").disabled=false;
    }
}

function disableReader() {
    if (document.getElementById("reader").value == "no")
    {
        document.getElementById("quantity").disabled=true;
        document.getElementById("service").disabled=true;
    }
    else
    {
        document.getElementById("quantity").disabled=false;
        document.getElementById("service").disabled=false;
    }
}

function disableProf_serv() {
    if (document.getElementById("prof").value == "no")
    {
        document.getElementById("days").disabled=true;
    }
    else
    {
        document.getElementById("days").disabled=false;
    }
}