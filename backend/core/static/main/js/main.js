import { getCoins } from "./api.js";
import { renderCoinList } from "./dom.js";


let timerId = null;

async function init(){
    if (timerId) {
            clearTimeout(timerId);
        }

    try{


        const coins = await getCoins();
        if(coins === undefined){
            throw new Error("Coins data is undefined");
        }
    
        renderCoinList(coins);

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