/**
 * Criar novos elementos dentro do ouvinte de evento 'DOMContentLoaded'
 * Na declaração das variaveis que recebem o elemento, adicionar o operador de coalescência nula (??), pra caso o elemnto não exista na pagina, ser aplicado valor nulo 
 * Ao adicionar evento ao elemento, ou executar uma função aplicar dentro da condicional if(--elemento-- != null){}
 *
 */

document.addEventListener('DOMContentLoaded', function() {

  if(document.querySelector('.dashboard')){
    resizeDashboard();

    window.addEventListener('resize', function() {
      resizeDashboard();
    });
  }
  
  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // SIDEBAR
  let sidebar = document.querySelectorAll(".sidebar") ?? null;
  const btnSidebarCollapse = document.querySelector(".sidebar-collapse") ?? null;
  const btnSidebarExpand = document.querySelector(".sidebar-expand") ?? null;
  const sidebarCollapsed = document.querySelector("#sidebar-collapsed") ?? null;
  const sidebarExpanded = document.querySelector("#sidebar-expanded") ?? null;
  
  if(sidebar.length > 0){
      btnSidebarCollapse.addEventListener('click', function () {
          toggleElements(sidebarCollapsed, sidebarExpanded);
      });
  
      btnSidebarExpand.addEventListener('click', function () {
          toggleElements(sidebarCollapsed, sidebarExpanded);
      });
  }

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
  //add medicamento
  
  const add_medicamento = document.querySelector("#add-medicamento")  ?? null;
  const novo_medicamento = document.querySelector("#novo-medicamento") ?? null;
  
  if(add_medicamento!=null){
    add_medicamento.addEventListener("click", function() {
      novo_medicamento.innerHTML += "<div class='d-flex vertical-center mt-20'>" +
        "<div class='col mr-20'>" +
        "<label class='lbl-green fs-14 ml-10' for=''>Medicamento</label>" +
        "<input class='input_med' type='text' name='medicamento-prescrito[]'>" +
        "</div>" +
        "<div class='col'>" +
        "<label for='' class='lbl-green fs-14 ml-10'>Qtde</label>" +
        "<input class='input_n_med' type='number' name='qtde-medicamento[]'>" +
        "</div>" +
        "<img class='icon-add' onclick='removerParagrafo(this.parentNode)' src='static/imgs/icons/delete.svg' alt='Icone Deletar'>" +
        "</div>";
    });
  }
  
  // adicionando lembrete
  const add_lembrete = document.querySelector("#add-lembrete") ?? null; 
  const novo_lembrete = document.querySelector("#novo-lembrete") ?? null;
  
  if(add_lembrete!=null){
    add_lembrete.addEventListener("click", function() {
      novo_lembrete.innerHTML += "<div class='d-flex mt-20'>" +
        "<div class='col mr-20'>" +
        "<label class='lbl-green fs-14 ml-10' for=''>Hora</label>" +
        "<input class='hr' type='time' name='hora-lembrete[]'>" +
        "</div>" +
        "<div id='select-medicamento' class='col'>" +
        "<label class='lbl-green fs-14 ml-10' for=''> Medicamento </label>" +
        "<select id='' class='input_med lbl-white' name='lembrete-medicamento[]'>" +
        "<option class='lbl-green' value='op1'>Puxar remédio add acima</option>" +
        "<option class='lbl-green' value='op2'>Puxar remédio add acima</option>" +
        "<option class='lbl-green' value='op3'>Puxar remédio add acima</option>" +
        "</select>" +
        "</div>" +
        "<img class='icon-add' onclick='removerParagrafo(this.parentNode)' src='static/imgs/icons/delete.svg' alt='Icone Deletar'>" +
        "</div>";
    });  
  }
});

//PROGRESS BAR
function updateProgressBar(progressBar) {
  const currentPage = window.location.pathname.split('/').pop();
  let progress;

  if (currentPage === 'paciente-dados') {
      progress = 33.33;
  } else if (currentPage === 'paciente-diagnostico') {
      progress = 66.66;
  } else if (currentPage === 'paciente-familiar') {
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


function removerParagrafo(paragrafo) {
  paragrafo.remove();
}

//funcao para mostrar senha
$(document).ready(function() {
  var senha = $('#senha');
  var olho = $("#olho");

  olho.click(function() {
    if (senha.attr("type") === "password") {
      senha.attr("type", "text");
      olho.attr("src", "static/imgs/icons/eye-closed.svg");
    } else {
      senha.attr("type", "password");
      olho.attr("src", "static/imgs/icons/eye-open.svg");
    }
  });

  olho.mouseleave(function() {
    senha.attr("type", "password");
    olho.attr("src", "static/imgs/icons/eye-open.svg");
  });
});

function resizeDashboard(){
  let dashboard = document.querySelector('.dashboard') ?? null;
  let dashboardWidth = dashboard.offsetWidth ?? null;

  if(dashboardWidth <= 930){
    dashboard.classList.add('responsive');
  }else{
    dashboard.classList.remove('responsive');
  }
}

function submitForm(event, route, formID){
  event.preventDefault();
  
  // criar um objeto FormData
  var data = new FormData($(formID)[0]);
    
  $.ajax({
      url: route,
      type: 'POST',
      data: data,

      // definir o contentType e o processData como false
      contentType: false,
      processData: false,
      success: function(response) {
          if(route == '/valida-login' && response == 'success'){
            window.location.href = '/dashboard';
          }else{
            showAlert(response);
          }
      },
      error: function(jqXHR, textStatus, errorThrown) {
        var msg = 'Ocorreu um erro: ' + errorThrown;
        showAlert(msg);
      }
  });
}

function showAlert(msg){
  alert(msg);
}

$('form').on('submit', function(event) {
  var form = $(this);
  if (form.length > 0) {
      var route = form.attr('action');
      var formId = '#' + form.attr('id');
      submitForm(event, route, formId);
  }
});