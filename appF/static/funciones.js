function agregarMed(f){
  document.getElementById('agregarMed').style='display: blank';
  $("#agregarMed").load("/agregarMed");
}

function ponerhref(id,f){
  $("#hrefC").attr("href", "/eliminarM?id="+id+"&idf="+f)
}
