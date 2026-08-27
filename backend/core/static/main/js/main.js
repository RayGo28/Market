import { getCoins, getGlobalData } from "./api.js";
import { renderCoinList, RenderGlobalData } from "./dom.js";


let timerId = null;

async function init(){
    if (timerId) {
            clearTimeout(timerId);
        }

    try{


        const coins = await getCoins();
        if (coins && Array.isArray(coins)) {
            renderCoinList(coins);
        } else {
            console.warn("Invalid coins data received:", coins);
        }

        const globalData = await getGlobalData();
        if(globalData){
            RenderGlobalData(globalData);
        }
        else {
            console.warn("Invalid global data received:", globalData);
        }

    }
    catch (error){
        console.error("Error of initialization:", error);
    }
    finally{
        timerId = setTimeout(init, 5000)
    }
    
}

document.addEventListener("DOMContentLoaded", () => {
    init();

});