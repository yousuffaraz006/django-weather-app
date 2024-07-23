var searchForm = document.querySelector('#searchForm');

searchForm.addEventListener("submit", (e) => {
    Searching();
    e.preventDefault();
});

function Searching() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('carddiv').style.display = 'none';
}