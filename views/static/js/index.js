const btnSidebarCollapse = document.querySelector(".sidebar-collapse");
const btnSidebarExpand = document.querySelector(".sidebar-expand");
const sidebarCollapsed = document.querySelector("#sidebar-collapsed");
const sidebarExpanded = document.querySelector("#sidebar-expanded");

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // TESTE PROGRESS BAR
// script.js
const progressBar = document.querySelector('.progress');

function updateProgressBar() {
  const currentPage = window.location.pathname.split('/').pop();
  let progress;

  if (currentPage === 'paciente-dados') {
      progress = 33.33;
  } else if (currentPage === 'paciente-diagnostico') {
      progress = 66.66;
  } else if (currentPage === 'paciente-familiar') {
      progress = 100;
  } else {
      progress = 100;
  }

  progressBar.style.width = `${progress}%`;

  console.log(currentPage)
}

updateProgressBar();

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

document.getElementById("upload-picture").addEventListener("change", function(event) {
    var input = event.target;
    var reader = new FileReader();
    
    reader.onload = function() {
      var dataURL = reader.result;
      var preview = document.getElementById("preview");
      preview.src = dataURL;
    };
    
    if(input.files && input.files[0]) {
      reader.readAsDataURL(input.files[0]);
    }
  });





