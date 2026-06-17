document.querySelectorAll('.agregar-franja').forEach(btn => {
    btn.addEventListener('click', () => {
        const container = btn.previousElementSibling;
        const nueva = document.createElement('div');
        nueva.className = 'franja';
        nueva.innerHTML = `
            <label>Apertura</label>
            <input type="time" name="hora_apertura" required>
            <label>Cierre</label>
            <input type="time" name="hora_cierre" required>
            <button type="button" class="quitar-franja boton-cancelar franja-quitar">-</button>
        `;
        container.appendChild(nueva);
    });
});

document.addEventListener('click', e => {
    if (e.target.classList.contains('quitar-franja')) {
        e.target.closest('.franja').remove();
    }
});

document.getElementById('form-franjas').addEventListener('submit', () => { //recorre todas las franjas y guarda los valores
    const franjas = [];
    document.querySelectorAll('.dia-config').forEach(diaDiv => {
        const dia = parseInt(diaDiv.dataset.dia);
        diaDiv.querySelectorAll('.franja').forEach(franjaDiv => {
            franjas.push({
                dia_semana: dia,
                hora_apertura: franjaDiv.querySelector('[name="hora_apertura"]').value,
                hora_cierre: franjaDiv.querySelector('[name="hora_cierre"]').value,
            });
        });
    });
    document.getElementById('franjas_json').value = JSON.stringify(franjas);
});
