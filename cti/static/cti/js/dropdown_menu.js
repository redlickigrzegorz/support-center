window.onclick = function(event) {
    if (!event.target.matches('.dropdown-button')) {
        let dropdown_content = document.getElementsByClassName("dropdown-content");

        for (let i = 0; i < dropdown_content.length; i++) {
            let open_dropdown = dropdown_content[i];

            if (open_dropdown.classList.contains('show')) {
                open_dropdown.classList.remove('show');
            }
        }
    }
};

function dropdownFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}