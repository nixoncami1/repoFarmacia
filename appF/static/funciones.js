function agregarMed(f){
  document.getElementById('agregarMed').style='display: blank';
  $("#agregarMed").load("/agregarMed");

}

function ponerhref(id,f){
  $("#hrefC").attr("href", "/eliminarM?id="+id+"&idf="+f);
}

function ponerhrefEM(m,f,e){
  $("#hrefelEM").attr("href", "/eliminarME?idm="+m+"&idf="+f+"&ide="+e);
}

function redireccione(f,m){
  window.location.href = "/agregarMedEnfFarmNuevo?idm="+m+"&idf="+f+"&ide="+$("#aux").attr("href");
//  $("a.hrff").attr("href", "/eliminarM?id="+e+"&idf=");
}

function ponerhrefAe(e){
  if ($("#aux").attr("href") == ""){
    $("#aux").attr("href",e);
  }else{
    $("#aux").attr("href",e);
  }
}
