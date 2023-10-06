const menuEmail = document.querySelector('.navbar__email');
const desktopMenu = document.querySelector('.desktop-menu');

menuEmail,addEventListener('click', toggleDesktopMenu);

function toggleDesktopMenu(){
    desktopMenu.classList.toggle('inactive');
}

console.log("js funcionando")


