export function renderCoinList(coins){
    try{
        const ListContainer = document.getElementById("coinList");
        ListContainer.innerHTML = coins.map((coin, index) => {
            const currentData = coin.current_data || {};
            const priceChange = currentData.price_change_percentage_24h ?? 0;
            const isPositive = priceChange >= 0;
            const badgeClass = isPositive ? 'badge badge--up' : 'badge badge--down';
            const priceSign = isPositive ? '+' : ''


            return `<tr>
                            <td class="muted">${index + 1}</td>
                            <td>
                                <div class="coin">
                                <span class="coin__icon" style="--c:#f7931a">₿</span>
                                <span class="coin__name">${coin.name}</span>
                                <span class="coin__symbol">${coin.symbol}</span>
                                </div>
                            </td>
                            <td class="table__right mono">${currentData.price}</td>
                            <td class="table__right">
                                    <span class="${badgeClass}">${priceSign}${priceChange}%</span>
                            </td>
                            <td class="table__right mono hide-sm">${currentData.market_cap}</td>
                            <td class="table__right mono hide-sm">${currentData.total_volume}</td>
                            <td class="table__right mono hide-md">${coin.max_supply}</td>
                        </tr>`;
        }).join('');
    }
    catch (error){
        console.error("Error of rendering coin list:", error);
    }
}