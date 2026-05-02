document.getElementById("form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        "Programa academico del que es egresado": document.getElementById("Programa").value,
        "Genero": document.getElementById("Genero").value,
        "Edad_Codificada": document.getElementById("Edad").value,
        "Estrato": document.getElementById("Estrato").value,
        "Estado civil": document.getElementById("EstadoCivil").value,
        "Numero de hijos": document.getElementById("Hijos").value,
        "Nivel de formacion actual": document.getElementById("Formacion").value,
        "Tiene Emprendimiento": document.getElementById("Emprendimiento").value,
        "Tipo de organizacion donde labora": document.getElementById("TipoOrg").value,
        "Area en la cual se desempena": document.getElementById("Area").value,
        "Tamano Organizacion": document.getElementById("Tamano").value,
        "Sector economico pertenece empresa": document.getElementById("Sector").value,
        "Ingreso Mensual": document.getElementById("Ingreso").value
    };

    console.log("DATOS ENVIADOS:", data);

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        console.log("RESPUESTA BACKEND:", result);

        if (result.error) {
            document.getElementById("resultado").innerText = "Error: " + result.error;
        } else {
            document.getElementById("resultado").innerText =
                "Larga: " + result.Larga + "% | Corta: " + result.Corta + "%";
        }

    } catch (error) {
        console.error(error);
        document.getElementById("resultado").innerText = "Error conectando con el backend";
    }
});