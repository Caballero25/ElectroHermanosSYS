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
                        </tr>
                    </tbody>
                `;
    }).join('');

    searchResults.innerHTML = resultHTML;
}
