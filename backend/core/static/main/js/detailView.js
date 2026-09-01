import { getCoinDetailData, getCoins } from "./api.js";

document.addEventListener('alpine:init', () => {
    Alpine.data('coinDetail', (coinId) => ({
        coin: {},
        loading: true,
        error: null,
        timerId: null,
        searchQuery: '',
        searchResults: [],
        showDropdown: false,
        chart: null,

        init() {
            console.log('coinDetail initialized with coinId:', coinId);
            this.fetchCoinData();
        },

        async fetchSearchResults() {
            const query = this.searchQuery.trim();
            if (!query) {
                this.searchResults = [];
                this.showDropdown = false;
                return;
            }

            try {
                const data = await getCoins(query);
                this.searchResults = data.slice(0, 6);
                this.showDropdown = this.searchResults.length > 0;
            } catch (error) {
                console.error('Помилка пошуку на детальній сторінці:', error);
                this.searchResults = [];
                this.showDropdown = false;
            }
        },

        async fetchCoinData() {
            try {
                console.log('Fetching coin data for:', coinId);
                this.coin = await getCoinDetailData(coinId);
                this.$nextTick(() => {
                    this.renderChart(this.coin?.history_data ?? []);
                });
                console.log('Coin data loaded:', this.coin);
                this.loading = false;
                this.scheduleNextFetch();
            } catch (error) {
                console.error('Error loading coin detail:', error);
                this.error = `Помилка завантаження: ${error.message}`;
                this.loading = false;
            }
        },

        scheduleNextFetch() {
            this.timerId = setTimeout(async () => {
                try {
                    const updatedCoin = await getCoinDetailData(coinId);
                    this.coin = updatedCoin;

                    if (!this.chart && Array.isArray(updatedCoin?.history_data) && updatedCoin.history_data.length > 0) {
                        this.$nextTick(() => {
                            this.renderChart(updatedCoin.history_data);
                        });
                    }
                } catch (error) {
                    console.error('Error updating coin data:', error);
                }
                this.scheduleNextFetch();
            }, 5000);
        },

        priceFormat(val) {
            if (val == null) return '$0.00';
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 2,
                maximumFractionDigits: val < 1 ? 8 : 2
            }).format(val);
        },

        usdFormat(val) {
            if (val == null) return '$0';
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                notation: 'compact',
                maximumFractionDigits: 2
            }).format(val);
        },

        percentFormat(val) {
            if (val == null) return '0.00%';
            const prefix = val >= 0 ? '+' : '';
            return prefix + new Intl.NumberFormat('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }).format(val) + '%';
        },

        numberFormat(val) {
            if (val == null) return '0';
            return new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 }).format(val);
        },

        dateFormat(val) {
            if (!val) return '—';
            const date = new Date(val);
            if (isNaN(date)) return '—';

            return new Intl.DateTimeFormat('uk-UA', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            }).format(date);
        },
        renderChart(history = []) {
            const canvas = this.$refs.priceChart;

            if (!canvas || !Array.isArray(history) || history.length === 0) {
                if (this.chart) {
                    this.chart.destroy();
                    this.chart = null;
                }
                return;
            }

            if (this.chart) {
                this.chart.destroy();
            }

            const sortedHistory = [...history].reverse();

            this.chart = new Chart(canvas, {
                type: 'line',
                data: {
                    labels: sortedHistory.map(item =>
                        new Intl.DateTimeFormat('uk-UA', {
                            day: '2-digit',
                            month: '2-digit',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                        }).format(new Date(item.timestamp))
                    ),
                    datasets: [{
                        label: 'Price',
                        data: sortedHistory.map(item => Number(item.price) || 0),
                        borderColor: '#4f8cff',
                        backgroundColor: 'rgba(79, 140, 255, 0.15)',
                        borderWidth: 2,
                        pointRadius: 3,
                        pointHoverRadius: 6,
                        pointHitRadius: 10,
                        tension: 0.25
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        mode: 'nearest',
                        intersect: false
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                maxTicksLimit: 7
                            }
                        },
                        y: {
                            ticks: {
                                callback: value => `$${Number(value).toFixed(2)}`
                            }
                        }
                    }
                }
            });
        },

        destroy() {
            if (this.timerId) clearTimeout(this.timerId);
            if (this.chart) {
                this.chart.destroy();
            }
        }
    }));
});