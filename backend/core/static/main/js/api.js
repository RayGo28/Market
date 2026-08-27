export async function getCoins(){
    try{
        const response = await fetch('/api/coins/');

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

export async function getGlobalData(){
    try{
        const response = await fetch('/api/global/');
        if(!response.ok){
            throw new Error("")
        }

        return await response.json();
    }
    catch (error){
        console.error("Error of request",error)
        return null
    }
}