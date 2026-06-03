document.getElementById("fecha").addEventListener("change", function () {
    const [year, month, day] = this.value.split("-").map(Number); //divide la fecha por los - y los pasa a numero
    const diaSemana = new Date(year, month - 1, day)
        .toLocaleDateString("es-AR", { weekday: "long" }); //es-AR para que sea en español (lunes, martes)
    const diaCapitalizado = diaSemana.charAt(0).toUpperCase() + diaSemana.slice(1);//primera mayus (el back tiene la lista asi)

    const franja = HORARIOS_DATA.find(h => h.dia === diaCapitalizado);
    const select = document.getElementById("horario");
    select.innerHTML = "";

    if (!franja) {
        select.innerHTML = "<option disabled selected value=''>Sin horarios disponibles este día</option>";
        return;
    }

    const [apertura] = franja.hora_apertura.split(":").map(Number);
    const [cierre]   = franja.hora_cierre.split(":").map(Number);

    for (let h = apertura; h < cierre; h++) { //separa en bloques de 1 hora entre la apertura y el cierre para reservar
        const opt = document.createElement("option");
        const horaStr = String(h).padStart(2, "0") + ":00"; //padStart para dos digitos
        opt.value = horaStr;
        opt.textContent = horaStr + " hs";
        select.appendChild(opt);
    }
});
