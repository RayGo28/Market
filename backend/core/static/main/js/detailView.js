import { getCoinDetailData } from "./api.js";

document.addEventListener('alpine:init', () => {
    Alpine.data('coinDetail', (coinId) => ({
        coin: {},
        loading: true,
        error: null,
        timerId: null,

        init() {
            console.log('coinDetail initialized with coinId:', coinId);
            this.fetchCoinData();
        },

        async fetchCoinData() {
            try {
                console.log('Fetching coin data for:', coinId);
                this.coin = await getCoinDetailData(coinId);
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
                    this.coin = await getCoinDetailData(coinId);
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
        destroy() {
            if (this.timerId) clearTimeout(this.timerId);
        }
    }));
});