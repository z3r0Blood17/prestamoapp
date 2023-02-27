window.addEventListener('load', () =>{
    const numempleado = document.getElementById('numempleado')
    const nombre = document.getElementById('nombre')
    const accesorio = document.getElementById('accesorio')
    const descripcion = document.getElementById('descripcion')
    const fechaR = document.getElementById('fechaR')
    const formulario = document.querySelector('#formulario')

    formulario.addEventListener('submit',function (e) {
        validaCampos()
        e.preventDefault();
        
        
        

    })


    function validaCampos() {
        const nombreValor = nombre.value
        const accesorioValor = accesorio.value
        const descripcionValor = descripcion.value
        const fechaRValor = fechaR.value
        const numempleadoValor = numempleado.value.trim()
        let regexNumeros = new RegExp("^[0-9]+$")

        if (!nombreValor) {
            validaFalla(nombre, 'Campo Vacio')
        } else {
            validaOk(nombre)
        }

        if (!numempleadoValor) {
            validaFalla(numempleado, 'Campo Vacio')

        }

        else if (!regexNumeros.test(numempleadoValor)) {
            validaFalla(numempleado, 'Solo Numeros')
        } else {
            validaOk(numempleado)
        }



    }

    function validarFechaMenorActual(date){
        var x=new Date();
        var fecha = date.split("/");
        x.setFullYear(fecha[2],fecha[1]-1,fecha[0]);
        var today = new Date();

        if (x >= today)
        return false;
        else
        return true;
    }

    const validaFalla = (input, msje) => {
        const formControl = input.parentElement
        const aviso = formControl.querySelector('p')
        aviso.innerText = msje
        formControl.className = 'form-control falla'
    }

    const validaOk = (input, msje) => {
        const formControl = input.parentElement
        formControl.className = 'form-contrl ok'

    }
    
    input.addEventListener('invalid', function(event){ 
        event.preventDefault(); 
        if ( ! event.target.validity.valid ){ 
            elem.textContent = 'Username should only contain lowercase letters e.g. john'; elem.className = 'error'; elem.style.display = 'block'; input.className = 'invalid animated shake'; 
        } 
    });
  




})    
    