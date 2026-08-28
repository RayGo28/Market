export function renderCoinList(coins){
    try{
        const ListContainer = document.getElementById("coinList");
        if (!ListContainer) {
            throw new Error("ListContainer element not found");
        }
        const safeCoins = coins || [];
        ListContainer.innerHTML = safeCoins.map((coin, index) => {
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

export function RenderGlobalData(globalData){
    const usdFormatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        notation: 'compact',
        maximumFractionDigits: 2
        });

    const percentageFormatter = new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 4
        });

    const total_market_cap = usdFormatter.format(globalData.total_market_cap)
    const total_volume = usdFormatter.format(globalData.total_volume)
    const domination_btc = `${percentageFormatter.format(globalData.market_cap_percentage)}%`


    document.getElementById("total_market_cap").textContent = `${total_market_cap}` 
    document.getElementById("total_volume").textContent = `${total_volume}` 
    document.getElementById("active_coins_count").textContent = `${globalData.active_coins_count}`
    document.getElementById("domination_btc").textContent = domination_btc
    }