const btnSidebarCollapse = document.querySelector(".sidebar-collapse");
const btnSidebarExpand = document.querySelector(".sidebar-expand");
const sidebarCollapsed = document.querySelector("#sidebar-collapsed");
const sidebarExpanded = document.querySelector("#sidebar-expanded");


btnSidebarCollapse.addEventListener('click', function(){
   toggleElements(sidebarCollapsed, sidebarExpanded);
});

btnSidebarExpand.addEventListener('click', function(){
    toggleElements(sidebarCollapsed, sidebarExpanded);
});

function toggleElements(...elements) {
    elements.forEach((element) => {
        element.classList.toggle('d-none');
    });
}

window.addEventListener('resize', function() {
    const mainWrapper = document.querySelector('.dashboard');
    const sidebar = document.querySelector('.sidebar');
    mainWrapper.style.width = `calc(100% - ${sidebar.offsetWidth}px)`;
});
  