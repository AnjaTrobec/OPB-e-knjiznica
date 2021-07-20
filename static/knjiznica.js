// javascript

'use strict'
function isci(stolpci = [1]) {
  let vrednost = document.getElementById('isci').value;  //vpisana vrednost v iskalniku
  let tabela = document.getElementById('izpis');    //
  [...tabela.rows].forEach(vrstica => {           //lambda funkcija brez imena 
      if(stolpci.some(stolpec => seUjema(vrstica, stolpec, vrednost))) {
        vrstica.style.display = ''
      } 
      else {
        vrstica.style.display = 'none'
      }
  })
}  

function seUjema(vrstica, stolpec, vrednost) {
    let vsebina = vrstica.cells[stolpec].innerText
    return vsebina.toLocaleLowerCase().indexOf(vrednost.toLocaleLowerCase()) >= 0
}

//toLocaleLowerCase() vse spremeni v male črke, upošteva tudi šumnike