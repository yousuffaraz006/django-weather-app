function checkData() {
    if (data == 'True') {
        console.log('Data came')
        document.querySelector('#weather-card').style.display = "block";
    } else {
        console.log('Not yet')
    }
}

function Searching() {
    document.getElementById('loading').style.display = 'block';
    document.getElementsByClassName("dis-inp").setAttribute("disabled", "true");
}