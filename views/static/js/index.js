/**
 * Criar novos elementos dentro do ouvinte de evento 'DOMContentLoaded'
 * Na declaração das variaveis que recebem o elemento, adicionar o operador de coalescência nula (??), pra caso o elemnto não exista na pagina, ser aplicado valor nulo 
 * Ao adicionar evento ao elemento, ou executar uma função aplicar dentro da condicional if(--elemento-- != null){}
 *
 */

document.addEventListener('DOMContentLoaded', function() {
  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // SIDEBAR
  const btnSidebarCollapse = document.querySelector(".sidebar-collapse") ?? null;
  const btnSidebarExpand = document.querySelector(".sidebar-expand") ?? null;
  const sidebarCollapsed = document.querySelector("#sidebar-collapsed") ?? null;
  const sidebarExpanded = document.querySelector("#sidebar-expanded") ?? null;
  
  btnSidebarCollapse.addEventListener('click', function () {
    toggleElements(sidebarCollapsed, sidebarExpanded);
  });

  btnSidebarExpand.addEventListener('click', function () {
      toggleElements(sidebarCollapsed, sidebarExpanded);
  });

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  
  const progressBar = document.querySelector('.progress') ?? null;
  if(progressBar!=null){
    updateProgressBar(progressBar);
  }
  
  const uploadPicture = document.getElementById("upload-picture") ?? null;
  if(uploadPicture!=null){
    uploadPicture.addEventListener("change", function(event) {
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
  }
});
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // TESTE PROGRESS BAR
// script.js

function updateProgressBar(progressBar) {
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

function toggleElements(...elements) {
  elements.forEach((element) => {
      element.classList.toggle('d-none');
  });
}