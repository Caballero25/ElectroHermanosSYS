const getOptionChart = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/get_chart/");
        return await response.json();
    } catch (ex) {
        alert(ex);
    }
};

const getOptionChart2 = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/get_chart/");
        return await response.json();
    } catch (ex) {
        alert(ex);
    }
};

const initChart = async () => {
    const myChart = echarts.init(document.getElementById("chart"));
    const myChart2 = echarts.init(document.getElementById("chart2"));

    myChart.setOption(await getOptionChart());
    myChart2.setOption(await getOptionChart2());

    myChart.resize();
    myChart2.resize();
};

window.addEventListener("load", async () => {
    await initChart();
    setInterval(async () => {
        await initChart();
    }, 3600000);
});
