let logoutModalDisplay = false;

const profileButton = document.getElementById('profile_btn');

profileButton.addEventListener('click', (e) => {
    e.preventDefault();
    logoutModalDisplay = !logoutModalDisplay;
    if (!logoutModalDisplay) {
        document.getElementById('logout_menu').style.display = 'none';
    } else {
        document.getElementById('logout_menu').style.display = 'block';
    }

});

