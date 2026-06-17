document.getElementById("fecha").addEventListener("change", function () {
    const [year, month, day] = this.value.split("-").map(Number);
    const diaSemana = new Date(year, month - 1, day)
        .toLocaleDateString("es-AR", { weekday: "long" });

    // Capitaliza la primera letra usando localeCompare-safe approach
    // (funciona bien con tildes: miércoles -> Miércoles, sábado -> Sábado)
    const diaCapitalizado = diaSemana[0].toLocaleUpperCase("es-AR") + diaSemana.slice(1);

    const franja = HORARIOS_DATA.find(
        h => h.dia.toLowerCase() === diaSemana.toLowerCase()  // comparamos en minúscula para evitar problemas
    );
    const select = document.getElementById("horario");
    select.innerHTML = "";

    if (!franja) {
        select.innerHTML = "<option disabled selected value=''>Sin horarios disponibles este día</option>";
        return;
    }

    const [apertura] = franja.hora_apertura.split(":").map(Number);
    const [cierre]   = franja.hora_cierre.split(":").map(Number);

    for (let h = apertura; h < cierre; h++) {
        const opt = document.createElement("option");
        const horaStr = String(h).padStart(2, "0") + ":00";
        opt.value = horaStr;
        opt.textContent = horaStr + " hs";
        select.appendChild(opt);
    }
});