
function disablePreservation() {
    if (document.getElementById("id_type").value == "digital")
    {
        document.getElementById("id_offline_data").disabled=false;
        document.getElementById("id_pages").disabled=true;
        document.getElementById("id_layout").disabled=true;
    }
    else if (document.getElementById("id_type").value == "visual")
    {
        document.getElementById("id_offline_data").disabled=true;
        document.getElementById("id_pages").disabled=false;
        document.getElementById("id_layout").disabled=false;
    }
    else (document.getElementById("id_type").value == "hybrid")
    {
        document.getElementById("id_offline_data").disabled=false;
        document.getElementById("id_pages").disabled=false;
        document.getElementById("id_layout").disabled=false;
    }
}


function disableAwa() {
    if (document.getElementById("id_awa").value == "no")
    {
        document.getElementById("id_awa_contribution").disabled=true;
        document.getElementById("id_awa_storage").disabled=true;
    }
    else
    {
        document.getElementById("id_awa_contribution").disabled=false;
        document.getElementById("id_awa_storage").disabled=false;
    }
}

function disableReader() {
    if (document.getElementById("id_piqlreader").value == "no")
    {
        document.getElementById("id_quantity").disabled=true;
        document.getElementById("id_service").disabled=true;
    }
    else
    {
        document.getElementById("id_quantity").disabled=false;
        document.getElementById("id_service").disabled=false;
    }
}

function disableProf_serv() {
    if (document.getElementById("id_consultancy").value == "no")
    {
        document.getElementById("id_days").disabled=true;
    }
    else
    {
        document.getElementById("id_days").disabled=false;
    }
}