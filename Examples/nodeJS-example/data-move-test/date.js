setInterval(()=>{
    let date_ob = new Date();   
    let hours = date_ob.getHours().toString();
    let mins = date_ob.getMinutes().toString();

    console.log(hours+mins);
}, 60*1000);