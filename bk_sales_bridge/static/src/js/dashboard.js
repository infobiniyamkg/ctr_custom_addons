/** @odoo-module **/
console.log("🔥 BK SALES BRIDGE dashboard.js LOADED");
import {
    Component,
    onWillStart,
    onMounted,
    onPatched,
    onWillUnmount,
    useState,
} from "@odoo/owl";

import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";


export class BkSalesBridgeDashboard extends Component {
    static template = "bk_sales_bridge.dashboard";

    setup() {
        this.chartInstances = {};

        this.state = useState({
            kpis: {},
            charts: {},
            tables: {},

            filters: {
                pos_sources: [],
                categories: [],
            },

            loading: true,
            error: null,

            startDate: this.getDateString(
                new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
            ),

            endDate: this.getDateString(new Date()),

            posSourceId: "",
            productCategory: "",
        });

        onWillStart(async () => {
            await this.loadDashboard();
        });

        onMounted(() => {
            this.initializeCharts();
        });

        onPatched(() => {
            if (!this.state.loading) {
                this.initializeCharts();
            }
        });

        onWillUnmount(() => {
            this.destroyAllCharts();
        });
    }


    // ============================================================
    // DATE HELPERS
    // ============================================================

    getDateString(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");

        return `${year}-${month}-${day}`;
    }


    // ============================================================
    // DASHBOARD DATA
    // ============================================================

    async loadDashboard() {
        this.state.loading = true;
        this.state.error = null;

        try {
            const data = await rpc(
                "/bk_sales_bridge/dashboard",
                {
                    start_date: this.state.startDate,
                    end_date: this.state.endDate,
                    pos_source_id: this.state.posSourceId || null,
                    product_category: this.state.productCategory || null,
                }
            );

            this.state.kpis = data.kpis || {};
            this.state.charts = data.charts || {};
            this.state.tables = data.tables || {};

            this.state.filters = {
                pos_sources: data.filters?.pos_sources || [],
                categories: data.filters?.categories || [],
            };
        } catch (error) {
            console.error(
                "BK Sales Bridge dashboard error:",
                error
            );

            this.state.error = "Failed to load dashboard data";
        } finally {
            this.state.loading = false;
        }
    }


    // ============================================================
    // FILTER EVENTS
    // ============================================================

    async onStartDateChange(event) {
        this.state.startDate = event.target.value;
        await this.loadDashboard();
    }

    async onEndDateChange(event) {
        this.state.endDate = event.target.value;
        await this.loadDashboard();
    }

    async onPosSourceChange(event) {
        this.state.posSourceId = event.target.value;
        await this.loadDashboard();
    }

    async onCategoryChange(event) {
        this.state.productCategory = event.target.value;
        await this.loadDashboard();
    }


    // ============================================================
    // CHART MANAGEMENT
    // ============================================================

    initializeCharts() {
        this.destroyAllCharts();

        requestAnimationFrame(() => {
            if (this.state.loading) {
                return;
            }

            if (typeof Chart === "undefined") {
                console.error(
                    "Chart.js is not loaded."
                );
                return;
            }

            this.initSalesTrendChart();
            this.initMarginByOutletChart();
            this.initFlagDistributionChart();
            this.initCategoryPerformanceChart();
            this.initProfitLossChart();
            this.initLowMarginChart();
        });
    }


    destroyAllCharts() {
        Object.values(this.chartInstances).forEach((chart) => {
            if (chart && typeof chart.destroy === "function") {
                chart.destroy();
            }
        });

        this.chartInstances = {};
    }


    // ============================================================
    // SALES TREND
    // ============================================================

    initSalesTrendChart() {
        const canvasEl = document.getElementById(
            "salesTrendChart"
        );

        if (!canvasEl || typeof Chart === "undefined") {
            return;
        }

        const data = this.state.charts.sales_trend || {};
        const ctx = canvasEl.getContext("2d");

        this.chartInstances.salesTrend = new Chart(ctx, {
            type: "line",

            data: {
                labels: data.dates || [],

                datasets: [
                    {
                        label: "Net Sales",
                        data: data.sales || [],

                        borderColor: "#4CAF50",
                        backgroundColor:
                            "rgba(76, 175, 80, 0.05)",

                        borderWidth: 2,
                        tension: 0.4,
                        fill: true,

                        pointRadius: 4,
                        pointBackgroundColor: "#4CAF50",
                    },

                    {
                        label: "Margin",
                        data: data.margin || [],

                        borderColor: "#2196F3",
                        backgroundColor:
                            "rgba(33, 150, 243, 0.05)",

                        borderWidth: 2,
                        tension: 0.4,
                        fill: true,

                        pointRadius: 4,
                        pointBackgroundColor: "#2196F3",
                    },
                ],
            },

            options: {
                responsive: true,
                maintainAspectRatio: true,

                interaction: {
                    mode: "index",
                    intersect: false,
                },

                plugins: {
                    legend: {
                        position: "bottom",

                        labels: {
                            padding: 15,

                            font: {
                                size: 12,
                            },
                        },
                    },

                    filler: {
                        propagate: true,
                    },
                },

                scales: {
                    y: {
                        beginAtZero: true,

                        ticks: {
                            font: {
                                size: 11,
                            },
                        },
                    },

                    x: {
                        ticks: {
                            font: {
                                size: 11,
                            },
                        },
                    },
                },
            },
        });
    }


    // ============================================================
    // MARGIN BY OUTLET
    // ============================================================

    initMarginByOutletChart() {
        const canvasEl = document.getElementById(
            "marginByOutletChart"
        );

        if (!canvasEl || typeof Chart === "undefined") {
            return;
        }

        const data =
            this.state.charts.margin_by_outlet || [];

        const ctx = canvasEl.getContext("2d");

        this.chartInstances.marginOutlet = new Chart(ctx, {
            type: "bar",

            data: {
                labels: data.map(
                    (item) => item.outlet
                ),

                datasets: [
                    {
                        label: "Margin %",
                        data: data.map(
                            (item) => item.margin_pct
                        ),

                        backgroundColor: [
                            "#4CAF50",
                            "#2196F3",
                            "#FF9800",
                            "#F44336",
                            "#9C27B0",
                        ],

                        borderRadius: 5,
                        borderSkipped: false,
                    },
                ],
            },

            options: {
                responsive: true,
                maintainAspectRatio: true,

                indexAxis: "y",

                plugins: {
                    legend: {
                        position: "bottom",

                        labels: {
                            padding: 15,

                            font: {
                                size: 12,
                            },
                        },
                    },
                },

                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,

                        ticks: {
                            font: {
                                size: 11,
                            },
                        },
                    },

                    y: {
                        ticks: {
                            font: {
                                size: 11,
                            },
                        },
                    },
                },
            },
        });
    }


    // ============================================================
    // QUALITY FLAGS
    // ============================================================

    initFlagDistributionChart() {
        const canvasEl = document.getElementById(
            "flagDistributionChart"
        );

        if (!canvasEl || typeof Chart === "undefined") {
            return;
        }

        const data =
            this.state.charts.flag_distribution || [];

        const ctx = canvasEl.getContext("2d");

        this.chartInstances.flagDist = new Chart(ctx, {
            type: "doughnut",

            data: {
                labels: data.map(
                    (item) => item.flag
                ),

                datasets: [
                    {
                        data: data.map(
                            (item) => item.count
                        ),

                        backgroundColor: [
                            "#4CAF50",
                            "#FF9800",
                            "#F44336",
                            "#9C27B0",
                            "#00BCD4",
                        ],

                        borderColor: "#fff",
                        borderWidth: 2,
                    },
                ],
            },

            options: {
                responsive: true,
                maintainAspectRatio: true,

                plugins: {
                    legend: {
                        position: "bottom",

                        labels: {
                            padding: 15,

                            font: {
                                size: 12,
                            },
                        },
                    },

                    tooltip: {
                        callbacks: {
                            label(context) {
                                const label =
                                    context.label || "";

                                const value =
                                    context.parsed;

                                return `${label}: ${value}`;
                            },
                        },
                    },
                },
            },
        });
    }


    // ============================================================
    // CATEGORY PERFORMANCE
    // ============================================================

    initCategoryPerformanceChart() {
        const canvasEl = document.getElementById(
            "categoryPerformanceChart"
        );

        if (!canvasEl || typeof Chart === "undefined") {
            return;
        }

        const data =
            this.state.charts.category_performance || [];

        const ctx = canvasEl.getContext("2d");

        this.chartInstances.categoryPerf = new Chart(
            ctx,
            {
                type: "bar",

                data: {
                    labels: data.map(
                        (item) => item.category
                    ),

                    datasets: [
                        {
                            label: "Sales (ETB)",
                            data: data.map(
                                (item) => item.sales
                            ),

                            backgroundColor: "#2196F3",
                            yAxisID: "y",

                            borderRadius: 4,
                        },

                        {
                            label: "Margin %",
                            data: data.map(
                                (item) => item.margin_pct
                            ),

                            backgroundColor: "#4CAF50",
                            yAxisID: "y1",

                            borderRadius: 4,
                        },
                    ],
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: true,

                    plugins: {
                        legend: {
                            position: "bottom",

                            labels: {
                                padding: 15,

                                font: {
                                    size: 12,
                                },
                            },
                        },
                    },

                    scales: {
                        y: {
                            type: "linear",
                            display: true,
                            position: "left",

                            ticks: {
                                font: {
                                    size: 11,
                                },
                            },
                        },

                        y1: {
                            type: "linear",
                            display: true,
                            position: "right",

                            max: 100,

                            grid: {
                                drawOnChartArea: false,
                            },
                        },

                        x: {
                            ticks: {
                                font: {
                                    size: 11,
                                },
                            },
                        },
                    },
                },
            }
        );
    }


    // ============================================================
    // PROFIT / LOSS
    // ============================================================

    initProfitLossChart() {
        const canvasEl = document.getElementById(
            "profitLossChart"
        );

        if (!canvasEl || typeof Chart === "undefined") {
            return;
        }

        const data =
            this.state.charts.profit_loss || {};

        const ctx = canvasEl.getContext("2d");

        this.chartInstances.profitLoss = new Chart(
            ctx,
            {
                type: "pie",

                data: {
                    labels: [
                        "Profitable",
                        "Loss",
                        "Break Even",
                    ],

                    datasets: [
                        {
                            data: [
                                data.profitable || 0,
                                data.loss || 0,
                                data.break_even || 0,
                            ],

                            backgroundColor: [
                                "#4CAF50",
                                "#F44336",
                                "#FFC107",
                            ],

                            borderColor: "#fff",
                            borderWidth: 2,
                        },
                    ],
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: true,

                    plugins: {
                        legend: {
                            position: "bottom",

                            labels: {
                                padding: 15,

                                font: {
                                    size: 12,
                                },
                            },
                        },
                    },
                },
            }
        );
    }


    // ============================================================
    // LOW MARGIN PRODUCTS
    // ============================================================

    initLowMarginChart() {
        const canvasEl = document.getElementById(
            "lowMarginChart"
        );

        if (!canvasEl || typeof Chart === "undefined") {
            return;
        }

        const data =
            this.state.charts.low_margin_items || [];

        const items = data.slice(0, 10);

        const ctx = canvasEl.getContext("2d");

        this.chartInstances.lowMargin = new Chart(
            ctx,
            {
                type: "bar",

                data: {
                    labels: items.map(
                        (item) => item.product
                    ),

                    datasets: [
                        {
                            label: "Margin %",
                            data: items.map(
                                (item) => item.margin_pct
                            ),

                            backgroundColor: "#FF9800",
                            borderRadius: 4,
                        },
                    ],
                },

                options: {
                    indexAxis: "y",

                    responsive: true,
                    maintainAspectRatio: true,

                    plugins: {
                        legend: {
                            position: "bottom",

                            labels: {
                                padding: 15,

                                font: {
                                    size: 12,
                                },
                            },
                        },

                        tooltip: {
                            callbacks: {
                                afterLabel(context) {
                                    const item =
                                        items[
                                            context.dataIndex
                                        ];

                                    return (
                                        "Price: " +
                                        item.unit_price +
                                        " | Cost: " +
                                        item.cost
                                    );
                                },
                            },
                        },
                    },

                    scales: {
                        x: {
                            max: 30,

                            ticks: {
                                font: {
                                    size: 11,
                                },
                            },
                        },

                        y: {
                            ticks: {
                                font: {
                                    size: 11,
                                },
                            },
                        },
                    },
                },
            }
        );
    }


    // ============================================================
    // FORMATTING
    // ============================================================

    formatCurrency(value) {
        return new Intl.NumberFormat("en-ET", {
            style: "currency",
            currency: "ETB",
        }).format(value || 0);
    }


    formatNumber(value) {
        return new Intl.NumberFormat("en-ET").format(
            value || 0
        );
    }


    getStatusColor(flag) {
        const colors = {
            ok: "#4CAF50",
            low_margin: "#FF9800",
            negative_margin: "#F44336",
            product_missing: "#9C27B0",
            price_anomaly: "#00BCD4",
        };

        return colors[flag] || "#999";
    }
}


// ============================================================
// CLIENT ACTION REGISTRATION
// ============================================================

registry
    .category("actions")
    .add(
        "bk_sales_bridge.dashboard",
        BkSalesBridgeDashboard
    );
