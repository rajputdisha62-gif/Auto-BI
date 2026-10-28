
// RENDER INITIAL PLOTLY CHARTS


function renderInitialCharts() {

    const chartElements =
        document.querySelectorAll(
            ".plotly-chart"
        );


    chartElements.forEach(
        (element) => {

            try {

                const figure =
                    JSON.parse(
                        element.dataset.chart
                    );


                Plotly.newPlot(

                    element,

                    figure.data,

                    figure.layout,

                    {
                        responsive: true,
                        displaylogo: false
                    }

                );

            }

            catch (error) {

                console.error(
                    "Chart rendering error:",
                    error
                );

            }

        }
    );

}


renderInitialCharts();




// GET SELECTED FILTERS


function collectFilters() {

    const filters = {};

    const filterElements =
        document.querySelectorAll(
            ".dashboard-filter"
        );


    filterElements.forEach(
        (element) => {

            const column =
                element.dataset.column;


            const selectedValues =
                Array.from(
                    element.selectedOptions
                ).map(
                    option => option.value
                );


            if (
                selectedValues.length > 0
            ) {

                filters[column] =
                    selectedValues;

            }

        }
    );


    return filters;

}




// UPDATE KPI CARDS


function updateKPIs(kpis) {

    const container =
        document.getElementById(
            "kpi-container"
        );


    container.innerHTML = "";


    kpis.forEach(
        kpi => {

            const card =
                document.createElement(
                    "div"
                );

            card.className =
                "kpi-card";


            card.innerHTML = `

                <div class="kpi-icon">

                    <i class="bi ${kpi.icon}"></i>

                </div>

                <div>

                    <span>
                        ${kpi.title}
                    </span>

                    <h2>
                        ${kpi.value}
                    </h2>

                </div>

            `;


            container.appendChild(
                card
            );

        }
    );

}




// UPDATE CHARTS

function updateCharts(charts) {

    const container =
        document.getElementById(
            "charts-container"
        );


    container.innerHTML = "";


    charts.forEach(
        (chart, index) => {

            const card =
                document.createElement(
                    "div"
                );

            card.className =
                "chart-card";


            const chartDiv =
                document.createElement(
                    "div"
                );


            chartDiv.id =
                `dynamic-chart-${index}`;


            card.appendChild(
                chartDiv
            );


            container.appendChild(
                card
            );


            const figure =
                JSON.parse(
                    chart.figure
                );


            Plotly.newPlot(

                chartDiv,

                figure.data,

                figure.layout,

                {
                    responsive: true,
                    displaylogo: false
                }

            );

        }
    );

}




// APPLY FILTERS


async function refreshDashboard() {

    const filters =
        collectFilters();


    const sheetSelector =
        document.getElementById(
            "sheet-selector"
        );


    try {

        const response =
            await fetch(

                `/api/filter/${FILE_ID}`,

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        sheet:
                            sheetSelector.value,

                        filters:
                            filters

                    })

                }

            );


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                data.error ||
                "Unable to update dashboard."
            );

            return;

        }


        updateKPIs(
            data.kpis
        );


        updateCharts(
            data.charts
        );


        document.getElementById(
            "summary-rows"
        ).textContent =
            data.summary.rows.toLocaleString();


        document.getElementById(
            "summary-columns"
        ).textContent =
            data.summary.columns;


        document.getElementById(
            "summary-completeness"
        ).textContent =
            data.summary.completeness + "%";

    }

    catch (error) {

        console.error(error);

    }

}



// FILTER EVENT


document
    .querySelectorAll(
        ".dashboard-filter"
    )
    .forEach(
        element => {

            element.addEventListener(
                "change",
                refreshDashboard
            );

        }
    );




// CLEAR FILTERS


document
    .getElementById(
        "clear-filters"
    )
    ?.addEventListener(
        "click",
        function () {

            document
                .querySelectorAll(
                    ".dashboard-filter"
                )
                .forEach(
                    filter => {

                        Array
                            .from(
                                filter.options
                            )
                            .forEach(
                                option => {

                                    option.selected =
                                        false;

                                }
                            );

                    }
                );


            refreshDashboard();

        }
    );




// CHANGE WORKSHEET


document
    .getElementById(
        "sheet-selector"
    )
    ?.addEventListener(
        "change",
        function () {

            const sheet =
                encodeURIComponent(
                    this.value
                );


            window.location.href =
                `/dashboard/${FILE_ID}?sheet=${sheet}`;

        }
    );