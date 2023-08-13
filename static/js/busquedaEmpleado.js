const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');

function formatFecha(fecha) {
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        timeZone: 'UTC'
    };

    const fechaFormateada = new Date(fecha).toLocaleString('es-US', options);
    return fechaFormateada;
}

searchInput.addEventListener('input', async (event) => {
    const searchTerm = event.target.value;

    if (searchTerm.trim() === '') {
        searchResults.innerHTML = '';
        return;
    }

    try {
        const response = await fetch(`/listaEmpleados/`);
        const dataText = await response.text();
        const data = JSON.parse(dataText);

        if (!Array.isArray(data)) {
            console.error('Data is not an array:', data);
            return;
        }

        const matchingEmployees = data.filter(employee => {
            const fullName = `${employee.fields.nombres} ${employee.fields.apellidos} ${employee.fields.cargo}`;
            return fullName.toLowerCase().includes(searchTerm.toLowerCase());
        });

        displayResults(matchingEmployees); // Llamamos a la función para mostrar los resultados
    } catch (error) {
        console.error('Error fetching or processing data:', error);
    }
});

function displayResults(employees) {
    if (employees.length === 0) {
        searchResults.innerHTML = '<p>No se encontraron empleados.</p>';
        return;
    }

    const resultHTML = employees.map(employee => {
        const formattedDate = formatFecha(employee.fields.fecha_ingreso);
        return `
                    <thead>
                        <tr>
                            <th scope="col"></th>
                            <th scope="col">#</th>
                            <th scope="col">Nombres</th>
                            <th scope="col">Apellidos</th>
                            <th scope="col">Cargo</th>
                            <th scope="col">Teléfono</th>
                            <th scope="col">Dirección</th>
                            <th scope="col">Salario</th>
                            <th scope="col">Ingreso</th>
                            <th scope="col">Activo</th>
                            <th scope="col">Nómina</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                        <th><p><a href="/administrar/empleado/${employee.pk}/" class="link-danger link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">Editar</a></p></th>
                        <th scope="row">${employee.pk}</th>
                        <td>${employee.fields.nombres}</td>
                        <td>${employee.fields.apellidos}</td>
                        <td>${employee.fields.cargo}</td>
                        <td>${employee.fields.telefono}</td>
                        <td>${employee.fields.direccion}</td>
                        <td>$${employee.fields.salario}</td>
                        <td>${formattedDate}</td>
                        <td>${employee.fields.activo}</td>
                        <td style="text-align: center;">
                            <a class="icon-link" href="/nomina/empleado/${employee.pk}" style="color: #0070BB;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-wallet2" viewBox="0 0 16 16">
                            <path d="M12.136.326A1.5 1.5 0 0 1 14 1.78V3h.5A1.5 1.5 0 0 1 16 4.5v9a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 13.5v-9a1.5 1.5 0 0 1 1.432-1.499L12.136.326zM5.562 3H13V1.78a.5.5 0 0 0-.621-.484L5.562 3zM1.5 4a.5.5 0 0 0-.5.5v9a.5.5 0 0 0 .5.5h13a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 0-.5-.5h-13z"/>
                            </svg>
                            </a>
                        </td>
                        </tr>
                    </tbody>
                `;
    }).join('');

    searchResults.innerHTML = resultHTML;
}
