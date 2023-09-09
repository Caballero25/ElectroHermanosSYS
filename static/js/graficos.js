document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/get_chart/');
        const data = await response.json();
        
        const myChart = echarts.init(document.getElementById('mychart'));
        myChart.setOption(data);
    } catch (error) {
        console.error('Error al obtener los datos o inicializar el gráfico:', error);
    }
});
