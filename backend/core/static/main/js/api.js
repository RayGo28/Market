export async function getCoins(search = '') {
    const url = search
        ? `/api/coins/?search=${encodeURIComponent(search)}`
        : '/api/coins/';

    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    return await response.json();
}

export async function getCoinDetailData(str){

    const response = await fetch(`/api/coins/${str}/`);
    if(!response.ok){
        throw new Error(`Server error: ${response.status}`);
    }


    return await response.json();
}

export async function getGlobalData() {
    const response = await fetch('/api/global/');

    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    return await response.json();
}