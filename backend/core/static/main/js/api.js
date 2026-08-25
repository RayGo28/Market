export async function getCoins(){
    try{
        const response = await fetch('/api/coin_list/');

        if(!response.ok){
            throw new Error(`Error of the server: ${response.status}`)
        }

        return await response.json();
    }
    catch (error){
        console.error("Error of request",error)
        return null
    }
}
