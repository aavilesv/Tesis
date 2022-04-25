
function todo()
{
    if (valruc()==false) {
        return false;
    }else {
        return true;
    }
}

function todocedula()
{
    if (valCedula()==false) {
        return false;
    }else {
        return true;
    }
}
function valCedula() {

    var cedula = document.getElementById("cedula").value;
    cedula=cedula.substring(0,10);
 
    //cedula=cedula.substring(0,10);

    
    
        //Obtenemos el digito de la region que sonlos dos primeros digitos
        var digito_region = cedula.substring(0,2);
        //Pregunto si la region existe ecuador se divide en 24 regiones
        if( digito_region >= 1 && digito_region <=24 ){
            var dig;
            var suma_total=0;
            for (var i=0;i<9;i++){
                dig = parseInt(cedula.substring(i,i+1));
                if (i%2==0){
                    dig = dig*2 ;
                    if ( dig > 9)
                        dig = dig - 9;
                }
                suma_total = suma_total + dig;
            }
            // Extraigo el ultimo digito
            var ultimo_digito   = parseInt(cedula.substring(9,10));
            //Obtenemos la decena inmediata
            var z = 0;
            while (suma_total % 10 != 0) {
                suma_total++;
                z++;
            }
            //Validamos que el digito validador sea igual al de la cedula
            if(z == ultimo_digito){
                // alert('la cedula:' + cedula + ' es correcta');
                //document.getElementById("cedula").reset();
                return true;
            }else{
                
                swal({
                    title: "Información!",
                    text: 'Cédula: ' + String(document.getElementById("cedula").value)  +' es incorrecta, por favor revisar digitos',
                    icon: "info",
                    buttons: {
                        confirm: {
                            text: "Confirmar",
                            value: true,
                            visible: true,
                            className: "btn btn-success",
                            closeModal: true
                        }
                    }
                });
        

                return false;
            }
        }else{
            // imprimimos en consola si la region no pertenece
            swal({
                title: "Información!",
                text: "Esta cedula no pertenece a ninguna region",
                icon: "info",
                buttons: {
                    confirm: {
                        text: "Confirm Me",
                        value: true,
                        visible: true,
                        className: "btn btn-success",
                        closeModal: true
                    }
                }
            });


            return false;
        }
    
    return false;
}

function valruc() {
    var cedula = document.getElementsByName("ruc").value;
    var ruc=cedula.substring(10,13);
    cedula=cedula.substring(0,10);
    //Obtenemos el digito de la region que sonlos dos primeros digitos
    var digito_region = cedula.substring(0,2);
    //Pregunto si la region existe ecuador se divide en 24 regiones
    if( digito_region >= 1 && digito_region <=24 ){
        var dig;
        var suma_total=0;
        for (var i=0;i<9;i++){
            dig = parseInt(cedula.substring(i,i+1));
            if (i%2==0){
                dig = dig*2 ;
                if ( dig > 9)
                    dig = dig - 9;
            }
            suma_total = suma_total + dig;
        }
        // Extraigo el ultimo digito
        var ultimo_digito   = parseInt(cedula.substring(9,10));
        //Obtenemos la decena inmediata
        var z = 0;
        while (suma_total % 10 != 0) {
            suma_total++;
            z++;
        }
        //Validamos que el digito validador sea igual al de la cedula
        if(z == ultimo_digito){
            // alert('la cedula:' + cedula + ' es correcta');
            return true;
        }else{
            Swal.fire({
                title: 'Información!',
                icon: 'info',
                text: 'Ruc:' + String(document.getElementById("ruc").value)  +' es incorrecto, por favor revisar digitos',
                html:'Ruc:' + String(document.getElementById("ruc").value) +' es incorrecto, por favor revisar digitos',
                showCloseButton: true,
                confirmButtonColor: "#33ECFF",
                confirmButtonText: 'OK',
                imageWidth: 400,
                imageHeight: 200,
                imageAlt: 'Custom image',
            });

            return false;
        }
    }else{
        // imprimimos en consola si la region no pertenece
     
        swal({
            title: "Información!",
            text: "Esta cedula no pertenece a ninguna region",
            icon: "info",
            buttons: {
                confirm: {
                    text: "Confirm Me",
                    value: true,
                    visible: true,
                    className: "btn btn-success",
                    closeModal: true
                }
            }
        });

        return false;
    }



}
function sololetrassin(e) {
    tecla = (document.all) ? e.keyCode : e.which; // 2
    if (tecla == 8)
        return true; // 3
    patron = /[A-Za-z]/; // 4
    te = String.fromCharCode(tecla); // 5
    return patron.test(te); // 6
}

function nadasindatos(e) {
    var key = window.Event ? e.which : e.keyCode;
    return (key >= 40 && key <= 47)
}
function soloNumeros(e) {
    var key = window.Event ? e.which : e.keyCode;
    return (key >= 48 && key <= 57)
}

function soloNumerospunto(e) {
    var key = window.Event ? e.which : e.keyCode;

    return ((key >= 48 && key <= 57) || key == 46)
}


function sololetras(e) {
    tecla = (document.all) ? e.keyCode : e.which; // 2
    if (tecla == 8)
        return true; // 3
    patron = /[A-Za-z\s]/; // 4
    te = String.fromCharCode(tecla); // 5
    return patron.test(te); // 6
}

function sololetrascoma(e) {
    key = e.keyCode || e.which;
    tecla = String.fromCharCode(key).toLowerCase();
    letras = " áéíóúabcdefghijklmnñopqrstuvwxyz";
    especiales = [8, 37, 39, 46];
    tecla_especial = false
    for (var i in especiales) {
     if (key == especiales[i]) {
      tecla_especial = true;
      break;
     }
    }
    if (letras.indexOf(tecla) == -1 && !tecla_especial)
     return false;
}



function sindatossd(e) {

    tecla = (document.all) ? e.keyCode : e.which; // 2
 if (tecla == 8)
     return true; // 3
 patron = /[\.]/; // 4
 te = String.fromCharCode(tecla); // 5
 return patron.test(te); // 6
 }

function sololetrasynumeros(e) {

       tecla = (document.all) ? e.keyCode : e.which; // 2
    if (tecla == 8)
        return true; // 3
    patron = /[A-Za-z\9123456780]/; // 4
    te = String.fromCharCode(tecla); // 5
    return patron.test(te); // 6
    }


function elimina()
{
    Swal.fire({
        title: "Usuario #123465",
        text: "¿Eliminar?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
    })
    .then(resultado => {
        if (resultado.value) {
            // Hicieron click en "Sí"
 return true;
        } else {
            // Dijeron que no
             return false;
        }
    });
}


function validar(e) {
    var key = window.Event ? e.which : e.keyCode;   
    //tecla = (document.all) ? e.keyCode : e.which;
    return false;
    //patron = /1/; //ver nota
    //te = String.fromCharCode(tecla);
    //return patron.test(te);
}