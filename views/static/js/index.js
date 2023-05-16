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

document.getElementById("upload").addEventListener("change", function(event) {
    var input = event.target;
    var reader = new FileReader();
    
    reader.onload = function() {
      var dataURL = reader.result;
      var preview = document.getElementById("preview");
      preview.src = dataURL;
    };
    
    if (input.files && input.files[0]) {
      reader.readAsDataURL(input.files[0]);
    }
  });