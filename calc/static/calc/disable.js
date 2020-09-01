
function disableState() {
    if (document.getElementById("type").value == "digital")
    {
        document.getElementById("digital").disabled=false;
        document.getElementById("visual").disabled=true;
    }
    else
    {
        document.getElementById("digital").disabled=true;
        document.getElementById("visual").disabled=false;
    }
}